from controller.json_parser_by_category import JSONParserByCategory
from controller.scraper_by_category import ScraperByCategory
from controller.scraper_by_url import ScraperByUrl
from controller.scraper_html_parsing import HTMLParsing, Navigator
from controller.utils import get_sku_from_url, get_price
from view import output


def get_developer_scraper_class(store):
    '''
    Mapping Store / Class.
    Enter the class of your custom scraper here. Use as key the name of the
    store exactly as registered in the system.
    
    Args:
        store (str): The name of store
    
    Returns:
        scraper_class (type): The name of class of scraper
    '''

    store_class_dict = {
        'store_example': StoreExampleScraper,
        'worldtenis': WorldTenisScraper, # not needed, just example
        'renner': RennerScraper,
        'Hering': HeringScraper,
    }
    return store_class_dict[store]


class StoreExampleHTMLParsing(HTMLParsing):
    '''
    Example of class inheriting HTML Parsing and overwriting with a
    customization directly in source code.
    '''

    def get_product_info(self, scraper, product_node):
        '''
        Example of method overwriting.
        Update a dict with all info for a product from its node.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
        Returns:
            product_info (dict): Product with info
        '''
        
        product_info = {}
        # TO DO
        return product_info

        
class StoreExampleScraper(ScraperByCategory):
    '''
    Example of class inheriting ScraperByCategory class and overwriting with a
    customization directly in source code.

    Attributes:
        parsing_class (StoreExampleHTMLParsing): The provided example
                                                customization class
    '''

    parsing_class = StoreExampleHTMLParsing

    def get_url_with_paging(self, category, page):
        '''
        Example of method overwriting.
        Formats the URL based on defined parameters.

        Args:
            category (str): Name of category
            page (int): Number of page

        Returns:
            url_with_paging (str): URL with paging
        '''

        # TO DO
        return "formated_url"
    
    def iterate_in_category(self, category):
        '''
        Example of method overwriting.
        Iterate in categories and update the global dict with products info.

        Args:
            category (list): List of categories
        '''

        # TO DO
        self.all_products_by_sku.update({'sku': {'name': 'example_sku'}})


class WorldTenisHTMLParsing(HTMLParsing):
    '''
    Example of class inheriting HTML Parsing and overwriting with a
    customization directly in source code.
    The customization here works, but it is not necessary because the
    configuration performed on screen already works fully. The 2 forms were left
    as an example for World Tennis.
    '''
    
    def get_product_info(self, scraper, product_node):
        '''
        Example of method overwriting for World Tennis store. Getting all data
        directly in this method.
        Update a dict with all info for a product from its node.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
        Returns:
            product_info (dict): Product with info
        '''
        
        product_info = {}

        product_info['name'] = product_node.select_one(
            ".product-name"
        ).get_text()
        
        original_price_node = product_node.select_one(".old-price")
        if original_price_node:
            product_info['old_price'] = get_price(
                original_price_node.select_one(".price").get_text()
            )
            product_info['sale_price'] = get_price(
                product_node.select_one(".special-price .price").get_text()
            )
        else:
            product_info['sale_price'] = get_price(
                product_node.select_one(".regular-price .price").get_text()
            )

        product_info['image'] = product_node.select_one(
            ".product-image").get("src"
        )

        product_info['url'] = product_node.select_one(
            ".product-name a").get("href"
        )

        product_info['sku'] = get_sku_from_url(
            product_info['url'], [r".com.br/(.+)?"]
        )

        return product_info


class WorldTenisScraper(ScraperByCategory):
    '''
    Example of class inheriting ScraperByCategory class and overwriting with a
    customization directly in source code.
    The customization here works, but it is not necessary because the
    configuration performed on screen already works fully. The 2 forms were left
    as an example for World Tennis.

    Attributes:
        parsing_class (WorldTenisHTMLParsing): The customizated parsing class
    '''

    parsing_class = WorldTenisHTMLParsing


class RennerScraper(JSONParserByCategory):
    '''
    Class inheriting JSONParserByCategory class and overwriting with a
    customization directly in source code.
    This class is necessary for the correct functioning of the Renner Scraper.
    '''

    def get_url_with_paging(self, category, page):
        '''
        The API URL is complex, so specifically the formatting of the URL is
        being performed by overriding this method.

        Args:
            category (str): Name of category
            page (int): Number of page

        Returns:
            url_with_paging (str): URL with paging
        '''

        extra1 = 'rest/model/lrsa/api/CatalogActor/resultsList?pushSite=rennerBrasilDesktop'
        extra2 = '&Nf=&isAjax=true&Ntt=&No='

        return u'{base}/{extra1}&{category}{extra2}{offset}'.format(
            base=self.store_config.url_base,
            extra1=extra1,
            category=category,
            extra2=extra2,
            offset=self.get_offset(page)
        )

class HeringHTMLParsing(HTMLParsing):
    '''
    Class inheriting HTML Parsing and overwriting with a customization directly
    in source code.
    This class is necessary for the correct functioning of the Hering Scraper.
    '''

    def get_old_price(self, scraper, product_node, name):
        '''
        Overwrite of the method that takes the old_price. In this case, it
        already comes in the node itself.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            old_price (float): Product old price
        '''

        try:

            """ could just do:
            old_price = get_price(product_node.get_text())
            but I decided to preserve the Navigator to allow using the others
            settings coming from the screen if the site makes any updates to the
            future
            """

            navigator = Navigator()
            navigator.get = scraper.store_config.old_price_get
            navigator.get_str = scraper.store_config.old_price_get_str
            navigator.get_price = scraper.store_config.old_price_get_price

            if navigator.get == 'get_text':
                old_price = product_node.get_text()
            elif navigator.get == 'get':
                old_price = product_node.get(navigator.get_str)

            if navigator.get_price:
                old_price = get_price(old_price)

        except Exception as e:
            output.parsing_error(scraper, "preço 'de'", e, name)
            raise
        
        return old_price

                
class HeringScraper(ScraperByUrl):
    '''
    Class inheriting ScraperByUrl class and overwriting with a customization
    directly in source code.
    This class is necessary for the correct functioning of the Hering Scraper.

    Attributes:
        parsing_class (HeringHTMLParsing): The customizated parsing class
    '''
    
    parsing_class = HeringHTMLParsing
