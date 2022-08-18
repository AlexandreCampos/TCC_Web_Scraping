from multiprocessing import Process, Queue, Manager
from queue import Empty, Full

from controller.scraper_html_parsing import HTMLParsing
from controller.scraper_store_config import ScraperStoreConfig


class Scraper(object):
    '''
    The Scraper and its features.

    Args:
        store_config (StoreConfig): Configuration for the store
        
    Attributes:
        headers (dict): General url headers
        scraper_headers (dict): Store additional url headers
        max_attempts_per_url (int): Attempts for case of unavailable page
        retry_attempt_delay (dict): Delay time between each request
        retry_delay (dict): Delay time for next attempt for page unavailable
                            case
        parsing_class (HTMLParsing): Parsing class
        ssc (ScraperStoreConfig): Store custom settings handler
        store_config (StoreConfig): Configuration for the store
        categories (list): List of categories to be scraped
        number_of_processes (int): Number of processes in multiprocessing
        queue (Queue): Queue object
        all_products_by_sku (DictProxy): global dict with all products with info
        output_GUI (ListProxy): global list with info from execution for the
                                output GUI
        is_test (boolean): Indicates if the execution is in test mode
    '''

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
    }

    scraper_headers = {}

    # default delay configs
    max_attempts_per_url = 5
    retry_attempt_delay = 0
    retry_delay = None

    parsing_class = HTMLParsing
    
    def __init__(self, store_config):

        # General configuration
        self.ssc = ScraperStoreConfig()
        self.ssc.set_scraper_config(self, store_config)       
        self.ssc.set_delay_config(self, store_config)
    
        self.html_parsing = self.parsing_class()

        # Threads configuration
        self.queue = Queue()
        manager = Manager()
        self.all_products_by_sku = manager.dict()
        
        if self.scraper_headers:
            self.headers.update(self.scraper_headers)

        if self.is_test:
            self.output_GUI = manager.list()            

    # Inicio do componente Varredor de Páginas de Catálogo / Multiprocessamento
    # (é como se fosse o "motor" do scraper)

    def produce(self):
        raise NotImplementedError

    def consume(self):
        raise NotImplementedError

    def put_in_queue(self, category):
        '''
        Queue categories.

        Args:
            category (list): List of categories
        '''

        try:
            self.queue.put(category, True, 2)
        except Full:
            print("Fila cheia!")
            raise Full

    def get_from_queue(self):
        ''' Returned something from the queue.'''

        try:
            # need timeout if you don't get stuck waiting
            return self.queue.get(timeout=2)
        except Empty:
            print("Consumidor finalizado")
            return None

    def get_web_info(self):
        '''
        Run scraper and return the info.

        Returns:
            output_GUI (list): Information from execution for the output GUI
            all_products_by_sku (dict): All products taken from scraping
        '''

        self.ssc.print_config(self)
        print("Iniciando scraper")

        self.produce()

        if self.number_of_processes > 1:
            consumers = []
            for x in range(0, self.number_of_processes):
                consumer = Process(target=self.consume)
                consumers.append(consumer)
                consumer.start()

            for consumer in consumers:
                consumer.join()
        else:
            self.consume()

        if self.is_test:
            return list(self.output_GUI), dict(self.all_products_by_sku)
        else:
            return None, dict(self.all_products_by_sku)

    # Fim do componente Varredor de Páginas de Catálogo / Multiprocessamento    

    # Varredor de produtos no nó da lista de produtos (nodes)
    def get_product_infos(self, nodes, error_url=''):
        '''
        Get product infos from product nodes.

        Args:
            nodes (ResultSet): BeautifulSoup object representing a list of
                               product nodes
            error_url (str): URL in case there is an error

        Returns:
            products_by_sku (dict): Products with info taken from scraping
        '''

        products_by_sku = {}

        if not nodes:
            return {}

        for product_node in nodes:
            
            try:
                product_info = self.html_parsing.get_product_info(self, product_node)

                if not product_info:
                    continue

                sku = product_info.get('sku')
                if sku:
                    product_by_sku = {sku: product_info}
                else:
                    print(f"Não foi possível obter o sku em: {product_info.get('url')} - {error_url}")
                    continue

                products_by_sku.update(product_by_sku)

            except(KeyboardInterrupt, SystemExit) as e:
                raise e
            except(Exception) as e:
                print(f"Não foi possível obter informações do produto em: {error_url}")
                print(f"Erro: {e}")
                
                """ o KeyboardInterrupt não é captado no pdb
                inserir raise aqui manualmente caso utilize pdb
                ainda não encontrei solução melhor para este problema no debug
                """
                
                if self.is_test:
                    raise

        return products_by_sku  

    