from bs4 import BeautifulSoup

from controller.scraper_site_access import SiteAccess
from controller.utils import get_sku_from_url, get_price
from view import output


# Componente HTML Parsing (Oxford)
class HTMLParsing(object):
    '''
    Responsible for extracting the content of interest from an HTML page.

    If in Developer Mode it is necessary to use JSON and HTML just instantiate
    JSONParsing. As JSONParsing extends from HTMLParsing, it is you can use
    either get_soup() or get_json().
        
    Attributes:
        site_access (SiteAccess): Object responsible for communication and
                                  access to the website
    '''

    def __init__(self):
        self.site_access = SiteAccess()
        
    # Componente Parsing (Tavenner)
    
    def get_soup(self, scraper, url):
        '''
        It reads the HTML and transforms it into readable information to be
        worked on. At this point, the "letter soup" makes a DOM shaped object
        possible to manipulate.

        Args:
            scraper (Scraper): Scraper object
            url (str): URL of the page to be read

        Returns:
            soup (BeautifulSoup): Object representing an HTML page
        '''

        response = self.site_access.get_response(scraper, url)
        if response:
            try:
                return BeautifulSoup(response, 'html.parser')
            except(KeyboardInterrupt, SystemExit) as e:
                raise e
            except(Exception) as e:
                print(f"Erro ao parsear o html: {e}")
                print(f"Url: {url}")
                
        return None

    # Componente Extractiom / Transformation (Tavenner)
    
    def get_product_info(self, scraper, product_node):
        '''
        Update a dict with all info for a product from its node.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
        Returns:
            product_info (dict): Product with info
        '''
        
        product_info = {}
        product_info['name'] = self.get_name(scraper, product_node)

        # product identifier for error messages
        name = product_info['name']

        product_info['image'] = self.get_image(scraper, product_node, name)
        product_info['url'] = self.get_url(scraper, product_node, name)
        product_info['brand'] = self.get_brand(scraper, product_node, name)
        product_info['category'] = self.get_category(scraper, product_node, name)
        product_info['sku'] = self.get_sku(
            scraper, name, product_node=product_node, url=product_info['url']
        )           

        original_price_node = self.get_old_price_node(
            scraper, product_node, name
        )
        if original_price_node:
            product_info['old_price'] = self.get_old_price(
                scraper, original_price_node, name
            )
            product_info['sale_price'] = self.get_new_price(
                scraper, product_node, name
            )
        else:
            product_info['old_price'] = None
            product_info['sale_price'] = self.get_sale_price(
                scraper, product_node, name
            )

        return product_info
        
    def get_info_from_node(self, product_node, navigator):
        '''
        Gets info from node using the methods referring to a predefined
        configuration.

        Args:
            product_node (Tag): BeautifulSoup object representing a node element
            navigator (Navigator): Object that navigates the node from
                                predefined settings
        Returns:
            info (str/float): Info from node
        '''
        
        info = ''

        if navigator.select == 'select_one':
            product_node = product_node.select_one(navigator.select_str)

        if navigator.get == 'get_text':
            info = product_node.get_text()
        elif navigator.get == 'get':
            info = product_node.get(navigator.get_str)

        if navigator.get_price:
            info = get_price(info)

        return info

    def get_node_from_node(self, product_node, navigator):
        '''
        Gets a "subnode" from node using the methods referring to a predefined
        configuration.

        Args:
            product_node (Tag): BeautifulSoup object representing a node element
            navigator (Navigator): Object that navigates the node from
                                predefined settings
        Returns:
            node (Tag): BeautifulSoup object representing a node element
        '''
        
        node = None

        if navigator.select == 'select_one':
            node = product_node.select_one(navigator.select_str)

        return node

    def get_name(self, scraper, product_node):
        '''
        Gets the name from node using the methods referring to a predefined
        configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
        
        Returns:
            name (str): Product name
        '''
        
        try:
            navigator = Navigator()
            navigator.select = scraper.store_config.name_select
            navigator.select_str = scraper.store_config.name_select_str
            navigator.get = scraper.store_config.name_get
            navigator.get_str = scraper.store_config.name_get_str
            name = self.get_info_from_node(product_node, navigator)
            self.check_empty(name)
            name = name.strip()
        except Exception as e:
            output.parsing_error(scraper, 'nome', e)
            raise
        return name
            
    def get_image(self, scraper, product_node, name):
        '''
        Gets the image from node using the methods referring to a predefined
        configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            image (str): Product image URL
        '''

        try:
            navigator = Navigator()
            navigator.select = scraper.store_config.image_select
            navigator.select_str = scraper.store_config.image_select_str
            navigator.get = scraper.store_config.image_get
            navigator.get_str = scraper.store_config.image_get_str
            image = self.get_info_from_node(product_node, navigator)
            self.check_empty(image)
        except Exception as e:
            output.parsing_error(scraper, 'imagem', e, name)
            raise
        return image

    def check_empty(self, str):
        '''
        Validates if a string is empty.

        Args:
            str (str): String to be checked
        '''

        if not str or not str.strip():
            raise ValueError('Retornou vazio.')
        
    def get_url(self, scraper, product_node, name):
        '''
        Gets the URL from node using the methods referring to a predefined
        configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            URL (str): Product URL
        '''

        try:
            navigator = Navigator()
            navigator.select = scraper.store_config.url_select
            navigator.select_str = scraper.store_config.url_select_str
            navigator.get = scraper.store_config.url_get
            navigator.get_str = scraper.store_config.url_get_str
            url = self.get_info_from_node(product_node, navigator)
            self.check_empty(url)
        except Exception as e:
            output.parsing_error(scraper, 'url', e, name)
            raise
        return url
    
    def get_sku(self, scraper, name, product_node=None, url=None):
        '''
        Gets the SKU from product url using the configured regexes.

        Args:
            scraper (Scraper): Scraper object
            name (str): Product name, for error log
            product_node (Tag): BeautifulSoup object representing a node element
            url (str): Product URL
        
        Returns:
            SKU (str): Product SKU
        '''

        try:
            sku = get_sku_from_url(url, scraper.store_config.sku_regexes)
            self.check_empty(sku)
        except Exception as e:
            output.parsing_error(scraper, 'sku', e, name)
            raise
        return sku
    
    def get_brand(self, scraper, product_node, name):
        '''
        Gets the brand from node using the methods referring to a predefined
        configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            brand (str): Product brand
        '''

        try:
            if scraper.store_config.get_brand:
                navigator = Navigator()
                navigator.select = scraper.store_config.brand_select
                navigator.select_str = scraper.store_config.brand_select_str
                navigator.get = scraper.store_config.brand_get
                navigator.get_str = scraper.store_config.brand_get_str
                brand = self.get_info_from_node(product_node, navigator)
                self.check_empty(brand)
            else:
                brand = None
        except Exception as e:
            output.parsing_error(scraper, 'marca', e, name)
            raise
        return brand
    
    def get_category(self, scraper, product_node, name):
        '''
        Gets the category from node using the methods referring to a predefined
        configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            category (str): Product category
        '''

        try:
            if scraper.store_config.get_category:
                if scraper.store_config.get_category_by_first_name:
                    category = name.split()[0]
                else:
                    navigator = Navigator()
                    navigator.select = scraper.store_config.category_select
                    navigator.select_str = scraper.store_config.category_select_str
                    navigator.get = scraper.store_config.category_get
                    navigator.get_str = scraper.store_config.category_get_str
                    category = self.get_info_from_node(product_node, navigator)
                    self.check_empty(category)
            else:
                category = None
        except Exception as e:
            output.parsing_error(scraper, 'categoria', e, name)
            raise
        return category
    
    def get_old_price_node(self, scraper, product_node, name):
        '''
        Gets the old price node from node using the methods referring to a
        predefined configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            old_price_node (Tag): Product old price node
        '''

        try:
            navigator = Navigator()
            navigator.select = scraper.store_config.old_price_node_select
            navigator.select_str = scraper.store_config.old_price_node_select_str
            if navigator.select_str:
                old_price_node = self.get_node_from_node(product_node, navigator)
            else:
                old_price_node = None
        except Exception as e:
            output.parsing_error(scraper, "nó do preço", e, name)
            raise
        return old_price_node
        
    def get_old_price(self, scraper, product_node, name):
        '''
        Gets the old price from node using the methods referring to a predefined
        configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            old_price (float): Product old price
        '''

        try:
            navigator = Navigator()
            navigator.select = scraper.store_config.old_price_select
            navigator.select_str = scraper.store_config.old_price_select_str
            navigator.get = scraper.store_config.old_price_get
            navigator.get_str = scraper.store_config.old_price_get_str
            navigator.get_price = scraper.store_config.old_price_get_price
            old_price = self.get_info_from_node(product_node, navigator)
        except Exception as e:
            output.parsing_error(scraper, "preço 'de'", e, name)
            raise
        return old_price

    def get_new_price(self, scraper, product_node, name):
        '''
        Gets the new price from node using the methods referring to a predefined
        configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            new_price (float): Product new price
        '''

        try:
            navigator = Navigator()
            navigator.select = scraper.store_config.new_price_select
            navigator.select_str = scraper.store_config.new_price_select_str
            navigator.get = scraper.store_config.new_price_get
            navigator.get_str = scraper.store_config.new_price_get_str
            navigator.get_price = scraper.store_config.new_price_get_price
            new_price = self.get_info_from_node(product_node, navigator)
        except Exception as e:
            output.parsing_error(scraper, "preço 'por'", e, name)
            raise
        return new_price

    def get_sale_price(self, scraper, product_node, name):
        '''
        Gets the sale price from node using the methods referring to a
        predefined configuration.

        Args:
            scraper (Scraper): Scraper object
            product_node (Tag): BeautifulSoup object representing a node element
            name (str): Product name, for error log
        
        Returns:
            sale_price (float): Product sale price
        '''

        try:
            navigator = Navigator()
            navigator.select = scraper.store_config.sale_price_select
            navigator.select_str = scraper.store_config.sale_price_select_str
            navigator.get = scraper.store_config.sale_price_get
            navigator.get_str = scraper.store_config.sale_price_get_str
            navigator.get_price = scraper.store_config.sale_price_get_price
            sale_price = self.get_info_from_node(product_node, navigator)
        except Exception as e:
            output.parsing_error(scraper, 'preço único', e, name)
            raise
        return sale_price


class Navigator(object):
    '''
    The Navigator object contains the predefined navigation settings for DOM
    tree.
    '''

    select = None
    select_str = None
    get = None
    get_str = None
    get_price = None

    second_select = None
    second_select_str = None
    second_get = None
    second_get_str = None