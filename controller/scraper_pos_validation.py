

class ScraperPosValidation(object):
    ''' Pos validation for the scraper.'''

    def format_url(self, url, url_base):
        '''
        URL formatter.

        Args:
            url (str): URL to be formatted
            url_base (str): URL base from the store (https://www.store.com.br)

        Returns:
            url (str): URL formatted
        '''
        
        # if it starts with //, the browser may crash
        if url[:2] == '//':
            url = url[2:]
        elif url[:1] == '/':
            url = url_base + url

        return url

    def validate_products(self, products_by_sku, store_config):
        '''
        Validate info from products.

        Many things can be added here as new needs.

        Args:
            products_by_sku (dict): Products with info taken from scraping
            store_config (StoreConfig): Configuration for the store
        '''

        for product in products_by_sku.values():

            product['url'] = self.format_url(
                product['url'], store_config.url_base
            )

            product['image'] = self.format_url(
                product['image'], store_config.url_base
            )
