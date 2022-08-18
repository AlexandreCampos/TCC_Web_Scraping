import sys
import time

from controller.scraper_pre_validation import ScraperPreValidation
from controller.scraper_pos_validation import ScraperPosValidation
from model.store_config import StoreConfig
from model.product import Product


class InitScraper(object):
    ''' Init the scraper here.'''

    def main(self, store_id=None, test=False):
        '''
        You can start the scraper directly or inside the program.

        Args:
            store_id (int): The store id
            test (boolean): Defines if it is in test mode
        '''

        debug = 0
        # test = 1
        
        store_config = StoreConfig()
        
        if not store_id:            
            # it only gets here if it is executed directly
            store_id = self.get_store_id(store_config)

        sp = ScraperPreValidation()
        store_config = sp.set_configs(store_config, store_id, debug, test)
        
        if sp.error:
            if test:
                return [sp.error]
            else:
                store_config.update_scraper_status(store_id, 'config_error')
                return
                    
        scraper_class = sp.get_scraper_class(store_config)

        if sp.error:
            if test:
                return [sp.error]
            else:
                store_config.update_scraper_status(store_id, 'config_error')
                return      

        scraper = scraper_class(store_config)

        products_by_sku = {}

        start = time.time()

        try:
            if not test:
                store_config.update_scraper_status(store_id, 'executing')
            output_GUI, products_by_sku = scraper.get_web_info()
        except(KeyboardInterrupt, SystemExit) as e:
            raise
        except(Exception) as e:
            print(e)
            # import pdb;pdb.set_trace()
            if test:
                return scraper.output_GUI
            else:
                store_config.update_scraper_status(store_id, 'error')
                raise

        end = time.time()
        print(end - start)

        # DEBUG
        # products_by_sku = {
        #   'meia-fem-under-armour-essentials-ns-kit-c-3-tam-m-casual-ag-13-1020137?ai=134&oi=1088': {
        #       'name': 'Meia Fem. Under Armour Essentials Ns Kit C/3 Tam M Casual',
        #       'category': 'Meia',
        #       'sale_price': 59.9,
        #       'image': 'https://mediacdn.wtennis.com.br/catalog/product/cache/2/image/252x252/9df78eab33525d08d6e5fb8d27136e95/u/n/under_armour_essentials_ns_ag_13_1020137_28017_1_30817_3_1.jpg',
        #       'url': 'https://www.wtennis.com.br/meia-fem-under-armour-essentials-ns-kit-c-3-tam-m-casual-ag-13-1020137?ai=134&oi=1088',
        #       'sku': 'meia-fem-under-armour-essentials-ns-kit-c-3-tam-m-casual-ag-13-1020137?ai=134&oi=1088'
        #   },
        #   'meia-fem-under-armour-athletic-solo-kit-c-3-tam-m-casual-ag-13-1020145?ai=134&oi=163': {
        #       'name': 'Meia Fem. Under Armour Athletic Solo Kit C/3 Tam M Casual',
        #       'category': 'Meia',
        #       'sale_price': 39.9,
        #       'image': 'https://mediacdn.wtennis.com.br/catalog/product/cache/2/image/252x252/9df78eab33525d08d6e5fb8d27136e95/u/n/under_armour_athleti_solo_ag_13_1020145_28041_1_30841_3_1.jpg',
        #       'url': 'https://www.wtennis.com.br/meia-fem-under-armour-athletic-solo-kit-c-3-tam-m-casual-ag-13-1020145?ai=134&oi=163',
        #       'sku': 'meia-fem-under-armour-athletic-solo-kit-c-3-tam-m-casual-ag-13-1020145?ai=134&oi=163'
        #   },
        #   'chinelo-under-armour-ignite-feminino-casual-ag-13-1017180?ai=134&oi=214': {
        #       'name': 'Chinelo Under Armour Ignite Feminino Casual',
        #       'category': 'Chinelo',
        #       'sale_price': 129.9,
        #       'image': 'https://mediacdn.wtennis.com.br/catalog/product/cache/2/image/252x252/9df78eab33525d08d6e5fb8d27136e95/u/n/under_armour_ignite_ag_13_1017180_26575_44_29415_3.jpg',
        #       'url': 'https://www.wtennis.com.br/chinelo-under-armour-ignite-feminino-casual-ag-13-1017180?ai=134&oi=214',
        #       'sku': 'chinelo-under-armour-ignite-feminino-casual-ag-13-1017180?ai=134&oi=214'
        #   },
        #   'chinelo-under-armour-core-feminino-casual-ag-13-1017263?ai=134&oi=1610': {
        #       'name': 'Chinelo Under Armour Core Feminino Casual',
        #       'category': 'Chinelo',
        #       'old_price': 89.9,
        #       'sale_price': 79.9,
        #       'image': 'https://mediacdn.wtennis.com.br/catalog/product/cache/2/image/252x252/9df78eab33525d08d6e5fb8d27136e95/u/n/under_armour_core_ag_13_1017263_26782_44_29611_3.jpg',
        #       'url': 'https://www.wtennis.com.br/chinelo-under-armour-core-feminino-casual-ag-13-1017263?ai=134&oi=1610',
        #       'sku': 'chinelo-under-armour-core-feminino-casual-ag-13-1017263?ai=134&oi=1610'
        #   }
        # }

        if test:
            return output_GUI
        elif products_by_sku:
            scrapped_product_quantity = len(products_by_sku)
            pos = ScraperPosValidation()
            pos.validate_products(products_by_sku, store_config)
            saved = Product().save_products(products_by_sku, store_id)
            if saved:
                store_config.update_scraper_status(
                    store_id, 'ok', products_quantity=scrapped_product_quantity
                )
            else:
                store_config.update_scraper_status(store_id, 'error')
            # import pdb; pdb.set_trace()
        else:
            store_config.update_scraper_status(store_id, 'error')
            raise Exception("Scraper nao pegou nenhum produto!")
            
    def get_store_id(self, store_config):
        received_args = sys.argv
        store_name = received_args[1]
        store = store_config.get_store_by_name(store_name)
        if store:
            store_id = store['id']
        else:
            raise Exception("Loja não encontrada.")

        return store_id

    
if __name__ == "__main__":
    InitScraper().main()