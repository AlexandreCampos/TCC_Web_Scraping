from controller.scraper import Scraper
from view import output


class ScraperByCategory(Scraper):
    '''
    The Scraper By Category and its features. This class scraping predefined
    categories.
    '''

    def produce(self):
        '''
        The Producer in the multiprocessing paradigm. Puts a list of categories
        in the queue.
        '''

        if self.is_test:
            self.put_in_queue(self.categories[0])
        else:
            for x in self.categories:
                self.put_in_queue(x)

    def consume(self):
        '''
        The Consumer in the multiprocessing paradigm. Consumes the list of
        categories from the queue.
        '''

        while True:
            category = self.get_from_queue()

            if category:
                self.iterate_in_category(category)
            else:
                return

    def get_url_with_paging(self, category, page):
        '''
        Formats the URL based on defined parameters.

        Args:
            category (str): Name of category
            page (int): Number of page

        Returns:
            url_with_paging (str): URL with paging
        '''

        return u'{base}/{category}{extras}{offset}'.format(
            base=self.store_config.url_base,
            category=category,
            extras=self.store_config.url_paging_extras,
            offset=self.get_offset(page)
        )

    def get_offset(self, page):
        '''
        Calculate the page offset.
        https://stackoverflow.com/questions/3520996/calculating-item-offset-for-pagination
        examples:
        page 1 = 1
        page 2 = 2
        page 1 and items_per_page 25: (1-1) * 25 = 0
        page 2 and items_per_page 25: (2-1) * 25 = 25
        page 3 and items_per_page 25: (3-1) * 25 = 50

        Args:
            page (int): Number of page

        Returns:
            page (int): Resulting offset
        '''

        if self.store_config.items_per_page:
            return (page - 1) * self.store_config.items_per_page
        else:
            return page

    def get_catalog_page(self, url_with_paging):
        '''
        Get catalog page.

        Args:
            url_with_paging (str): Catalog url 

        Returns:
            catalog_page (BeautifulSoup): Object representing an HTML page
        '''
        
        return self.html_parsing.get_soup(self, url_with_paging)

    def get_product_nodes(self, catalog_page):
        '''
        Get all nodes where there are products in the catalog.

        Args:
            catalog_page (BeautifulSoup): Object representing an HTML page

        Returns:
            product_nodes (ResultSet): BeautifulSoup object representing a list
                                      of product nodes
        '''
        
        return catalog_page.select(self.store_config.product_nodes_tag)

    def update_products_by_sku(self, url_with_paging, products_by_sku):
        '''
        Update the dict with product info from catalog page.

        Args:
            url_with_paging (str): URL to scraping
            products_by_sku (dict): products with info

        Returns:
            continue_to_iterate(boolean): Indicates whether the iteration should
                                          continue
        '''

        output.url(self, url_with_paging)
                    
        catalog_page = self.get_catalog_page(url_with_paging)

        if not catalog_page:
            output.not_catalog(self)
            return False

        print(url_with_paging)
        
        try:
            product_nodes = self.get_product_nodes(catalog_page)
        except Exception as e:
            output.parsing_error(self, 'nó do produto', e)
            raise

        output.len_products(self, len(product_nodes))

        # lista vazia de produtos
        if not product_nodes:
            return False
        
        count_before = len(products_by_sku)
        products_by_sku.update(
            self.get_product_infos(product_nodes, error_url=url_with_paging)
        )
        count_after = len(products_by_sku)

        # fim do catálogo
        if count_before == count_after:
            return False

        if self.is_test:
            output.detail_products(self, products_by_sku)
            return False

        return True
        
    def iterate_in_category(self, category):
        '''
        Iterate in categories and update the global dict with products info.

        Args:
            category (list): List of categories
        '''

        page = 1
        products_by_sku = {}

        while True:
            if self.is_test and self.store_config.url_test:
                url_with_paging = self.store_config.url_test
            else:
                url_with_paging = self.get_url_with_paging(category, page)

            continue_to_iterate = self.update_products_by_sku(
                url_with_paging, products_by_sku
            )

            if not continue_to_iterate:
                break
            
            # DEBUG
            # if page == 3:
            #   break

            page += 1

        self.all_products_by_sku.update(products_by_sku)

