from controller.scraper_by_category import ScraperByCategory
from view import output


class ScraperByUrl(ScraperByCategory):
    '''
    The Scraper By URL and its features. This class scraping all pages from a
    specific URL.
    '''

    def produce(self):
        '''
        The Producer in the multiprocessing paradigm. Creates a list of pages
        based on the number of processes and queues.
        '''

        if self.is_test:
            self.put_in_queue('1')
        else:
            for x in range(1, self.number_of_processes + 1):
                self.put_in_queue(x)

    def get_url_with_paging(self, page):
        '''
        Formats the URL based on defined parameters.

        Args:
            page (int): Number of page

        Returns:
            url_with_paging (str): URL with paging
        '''

        return u'{base}/{extras}{offset}'.format(
            base=self.store_config.url_base,
            extras=self.store_config.url_paging_extras,
            offset=self.get_offset(page)
        )

    def iterate_in_category(self, page):
        '''
        Iterate in pages and update the global dict with products info.

        Args:
            page (int): Number of page
        '''

        products_by_sku = {}
        
        while True:
            if self.is_test and self.store_config.url_test:
                url_with_paging = self.store_config.url_test
            else:
                url_with_paging = self.get_url_with_paging(page)

            continue_to_iterate = self.update_products_by_sku(
                url_with_paging, products_by_sku
            )

            if not continue_to_iterate:
                break

            # DEBUG
            # if page == 3:
            #   break

            page += self.number_of_processes

        self.all_products_by_sku.update(products_by_sku)

