

STATUS_OPTIONS = {
    None: '',
    'to_execute': 'Agendado para Executar',
    'executing': 'Executando',
    'ok': 'Executado com Sucesso',
    'error': 'Executado com Erro',
    'config_error': 'Erro nas Configurações'
}


CSV_ALL_PRODUCTS = {
    'name': 'nome',
    'image': 'imagem',
    'brand': 'marca',
    'category': 'categoria',
    'old_price': 'preço antigo',
    'sale_price': 'preço atual',
    'store': 'loja'
}


CSV_PRODUCTS_BY_CATEGORY = {
    'category': 'categoria',
    'quantity': 'quantidade',
    'avg_old_price': 'média do preço antigo',
    'avg_sale_price': 'média do preço atual',
    'min_old_price': 'menor preço antigo',
    'max_old_price': 'maior preço antigo',
    'min_sale_price': 'menor preço atual',
    'max_sale_price': 'maior preço atual',
}


class StoreConfigValidation(object):
    ''' StoreConfig validation.'''

    def is_empty(self, config, exceptions=[]):
        '''
        Validate if the config is empty.

        Args:
            config (Config): Config object
            exceptions (list): List of config to discard from validation

        Returns:
            is_empty (boolean): The result of validation
        '''
        
        for attribute, value in vars(config).items():
            if value is None or value == '':
                if not exceptions or attribute not in exceptions:
                    return True
        return False

    def validate_initial_config(self, config):
        '''
        Validate initial config.

        Not being used. No cases so far.

        Args:
            config (Config): Config object
        '''
        
        config.is_valid = True
        config.error_message = ""       

    def set_extra_config(self, config):
        '''
        Set extra config.

        Args:
            config (Config): Config object
        '''
        
        config.categories = config.categories.split()
    

class StoreScrapingValidation(object):
    ''' StoreScrapingConfig validation.'''

    def set_extra_config(self, config):
        '''
        Set extra config.

        Args:
            config (Config): Config object
        '''
        
        config.regexes = config.regexes.split()

        # if it is empty it will try to save as '' 
        if not config.items_per_page:
            config.items_per_page = 0


class StoreJSONParserValidation(object):
    ''' StoreJSONParserConfig validation.'''

    def set_extra_config(self, config):
        '''
        Set extra config.

        Args:
            config (Config): Config object
        '''
        
        config.categories_json = config.categories_json.split()

        # if it is empty it will try to save as '' 
        if not config.items_per_page_json:
            config.items_per_page_json = 0


class PriceComparisonValidation(object):
    ''' PriceComparison validation.'''

    def group_products_by_sku(self, products):
        '''
        Group products by SKU.

        Args:
            products (list): List of products

        Returns:
            products (list): List of products grouped by SKU
        '''
        
        products_by_sku = {}

        try:
            for product in products:
                store = product['store']
                if product['sku'] not in products_by_sku:
                    new_product = {}
                    new_product['sku'] = product['sku']
                    new_product[f'{store}_preço'] = product['sale_price']
                    new_product[f'{store}_url'] = product['url']
                    products_by_sku[product['sku']] = new_product
                else:
                    products_by_sku[product['sku']][f'{store}_preço'] = product[
                        'sale_price'
                    ]
                    products_by_sku[product['sku']][f'{store}_url'] = product[
                        'url'
                    ]
        except Exception as e:
            print("Erro ao agrupar produtos por sku")
            return []
        
        return list(products_by_sku.values())
