from controller.utils import get_current_day
from model import database


""" The parameter 'values' in cursor.execute() is used to avoid SQL INJECTION,
except when it is the 'id' field (user cannot insert).
"""


class StoreConfig(object):
    ''' Model StoreConfig.'''

    def dict_to_object(self, dict):
        '''
        Convert dict in object.

        Args:
            dict (dict): Dict to be converted
        '''
        
        for attribute, value in dict.items():
            setattr(self, attribute, value)

    def select_store_list(self):
        '''
        Select all stores.

        Returns:
            store_list(list): List of stores
        '''
        
        query = """
            SELECT
                id,
                name,
                status,
                last_execution,
                products_quantity
            FROM store_config
        """
        return database.SimpleQuery().select(query)

    def get_store_by_name(self, store_name):
        '''
        Get store id by name.

        Args:
            store_name (str): Name of store

        Returns:
            store_id (int): The store id
        '''
        
        query = """
            SELECT
                id
            FROM store_config 
            WHERE name = %s
        """

        values = (store_name, )
        store = database.SimpleQuery().select(query, values)
        return store[0] if store else None

    def get_stores_by_name(self, store_name_list):
        '''
        Select list of store ids by store names.

        Args:
            store_name_list (list): List with store name

        Returns:
            stores (list): List of store ids.
        '''
    
        if store_name_list:
            # https://stackoverflow.com/questions/5766230/select-from-sqlite-table-where-rowid-in-list-using-python-sqlite3-db-api-2-0
            query = f"""
                SELECT
                    id
                FROM store_config 
                WHERE name in ({','.join(['%s']*len(store_name_list))})
            """

            stores = database.SimpleQuery().select(query, store_name_list)
        else:
            query = """
                SELECT
                    id
                FROM store_config 
            """

            stores = database.SimpleQuery().select(query)

        return stores
        
    def get_parser_type(self, store_id):
        '''
        Get parser type from store.

        Args:
            store_id (int): Store id

        Returns:
            parser_type (str): The parser type
        '''
        
        query = """
            SELECT
                parser_type
            FROM store_config 
            WHERE id = {id}
        """.format(id=store_id)

        store = database.SimpleQuery().select(query)

        if store and store[0].get('parser_type'):
            return store[0]['parser_type']
        else:
            return None

    def get_store_config(self, store_id):
        '''
        Get store config.

        Args:
            store_id (int): Store id

        Returns:
            store_config (StoreConfig): Initial configuration for the store
        '''
        
        query = """
            SELECT
                sc.name,
                number_of_processes,
                developer_scraper,
                parser_type,
                scraper_type,
                url_base,
                max_attempts_per_url,
                retry_delay,
                retry_attempt_delay,
                GROUP_CONCAT(DISTINCT ct.name SEPARATOR ' ') AS categories
            FROM store_config sc
            LEFT JOIN category ct
            ON sc.id = ct.store_config_id
            WHERE sc.id = {id}
        """.format(id=store_id)

        store_config = database.SimpleQuery().select(query)
        return store_config[0] if store_config else None

    def get_store_scraping_config(self, store_id):
        '''
        Get store scraping config.

        Args:
            store_id (int): Store id

        Returns:
            store_config (StoreConfig): Scraping configuration for the store
        '''
        
        query = """
            SELECT
                sc.url_paging_extras,
                sc.url_test,
                sc.items_per_page,
                sc.product_nodes_tag,
                GROUP_CONCAT(DISTINCT rg.sequence SEPARATOR ' ') AS regexes,
                sc.get_brand,
                sc.get_category,
                sc.get_category_by_first_name,
                sc.name_select_str,
                sc.name_get,
                sc.name_get_str,
                sc.image_select_str,
                sc.image_get,
                sc.image_get_str,
                sc.url_select_str,
                sc.url_get,
                sc.url_get_str,
                sc.brand_select_str,
                sc.brand_get,
                sc.brand_get_str,
                sc.category_select_str,
                sc.category_get,
                sc.category_get_str,
                sc.old_price_node_select_str,
                sc.old_price_select_str,
                sc.old_price_get,
                sc.old_price_get_str,
                sc.old_price_get_price,
                sc.new_price_select_str,
                sc.new_price_get,
                sc.new_price_get_str,
                sc.new_price_get_price,
                sc.sale_price_select_str,
                sc.sale_price_get,
                sc.sale_price_get_str,
                sc.sale_price_get_price
            FROM store_config sc
            LEFT JOIN regex rg
            ON sc.id = rg.store_config_id
            WHERE sc.id = {id}
        """.format(id=store_id)

        store_config = database.SimpleQuery().select(query)
        return store_config[0] if store_config else None

    def get_store_json_parser_config(self, store_id):
        '''
        Get store json parser config.

        Args:
            store_id (int): Store id

        Returns:
            store_config (StoreConfig): JSON parser configuration for the store
        '''
        
        query = """
            SELECT
                sc.url_api,
                sc.url_json_paging_extras,
                sc.url_json_test,
                sc.items_per_page_json,
                GROUP_CONCAT(DISTINCT ct.name SEPARATOR ' ') AS categories_json,
                sc.product_nodes_keys,
                sc.get_brand_json,
                sc.get_category_json,
                sc.get_category_by_first_name_json,
                sc.name_keys,
                sc.image_keys,
                sc.sku_keys,
                sc.url_keys,
                sc.brand_keys,
                sc.category_keys,
                sc.old_price_node_keys,
                sc.old_price_keys,
                sc.old_price_get_price_json,
                sc.new_price_keys,
                sc.new_price_get_price_json,
                sc.sale_price_keys,
                sc.sale_price_get_price_json
            FROM store_config sc
            LEFT JOIN category_json ct
            ON sc.id = ct.store_config_id
            WHERE sc.id = {id}
        """.format(id=store_id)

        store_config = database.SimpleQuery().select(query)
        return store_config[0] if store_config else None
    
    def get_all_config_to_scraping(self, store_id):
        '''
        Get all config to scraping.

        Args:
            store_id (int): Store id

        Returns:
            store_config (StoreConfig): All config to scraping
        '''
        
        query = """
            SELECT
                sc.name,
                sc.number_of_processes,
                sc.scraper_type,
                sc.url_base,
                sc.items_per_page,
                sc.max_attempts_per_url,
                sc.retry_delay,
                sc.retry_attempt_delay,
                GROUP_CONCAT(DISTINCT ct.name SEPARATOR ' ') AS categories,
                sc.developer_scraper,
                sc.url_paging_extras,
                sc.url_test,
                sc.product_nodes_tag,
                GROUP_CONCAT(DISTINCT rg.sequence SEPARATOR ' ') AS sku_regexes,
                sc.get_brand,
                sc.get_category,
                sc.get_category_by_first_name,
                sc.name_select,
                sc.name_select_str,
                sc.name_get,
                sc.name_get_str,
                sc.image_select,
                sc.image_select_str,
                sc.image_get,
                sc.image_get_str,
                sc.url_select,
                sc.url_select_str,
                sc.url_get,
                sc.url_get_str,
                sc.brand_select,
                sc.brand_select_str,
                sc.brand_get,
                sc.brand_get_str,
                sc.category_select,
                sc.category_select_str,
                sc.category_get,
                sc.category_get_str,
                sc.old_price_node_select,
                sc.old_price_node_select_str,
                sc.old_price_select,
                sc.old_price_select_str,
                sc.old_price_get,
                sc.old_price_get_str,
                sc.old_price_get_price,
                sc.new_price_select,
                sc.new_price_select_str,
                sc.new_price_get,
                sc.new_price_get_str,
                sc.new_price_get_price,
                sc.sale_price_select,
                sc.sale_price_select_str,
                sc.sale_price_get,
                sc.sale_price_get_str,
                sc.sale_price_get_price
            FROM store_config sc
            LEFT JOIN category ct
            ON sc.id = ct.store_config_id
            LEFT JOIN regex rg
            ON sc.id = rg.store_config_id
            WHERE sc.id = {id}
        """.format(id=store_id)

        store_config = database.SimpleQuery().select(query)
        return store_config[0] if store_config else None

    def get_all_config_to_parser_json(self, store_id):
        '''
        Get all config to parser JSON.

        Args:
            store_id (int): Store id

        Returns:
            store_config (StoreConfig): All config to parser JSON
        '''
        
        query = """
            SELECT
                sc.name,
                sc.number_of_processes,
                sc.scraper_type,
                sc.url_base,
                sc.url_api,
                sc.max_attempts_per_url,
                sc.retry_delay,
                sc.retry_attempt_delay,
                sc.items_per_page_json AS items_per_page,
                GROUP_CONCAT(DISTINCT ct.name SEPARATOR ' ') AS categories,
                sc.developer_scraper,
                sc.url_json_paging_extras AS url_paging_extras,
                sc.url_json_test AS url_test,
                sc.product_nodes_keys,
                sc.get_brand_json AS get_brand,
                sc.get_category_json AS get_category,
                sc.get_category_by_first_name_json AS get_category_by_first_name,
                sc.name_keys,
                sc.image_keys,
                sc.url_keys,
                sc.sku_keys,
                sc.brand_keys,
                sc.category_keys,
                sc.old_price_node_keys,
                sc.old_price_keys,
                sc.old_price_get_price_json AS old_price_get_price,
                sc.new_price_keys,
                sc.new_price_get_price_json AS new_price_get_price,
                sc.sale_price_keys,
                sc.sale_price_get_price_json AS sale_price_get_price 
            FROM store_config sc
            LEFT JOIN category_json ct
            ON sc.id = ct.store_config_id
            WHERE sc.id = {id}
        """.format(id=store_id)

        store_config = database.SimpleQuery().select(query)
        return store_config[0] if store_config else None

    def scraper_is_executing(self, store_id):
        '''
        Check if scraper is executing.

        Args:
            store_id (int): Store id

        Returns:
            scraper_is_executing (boolean): The result of validation
        '''

        query = """
            SELECT
                status
            FROM store_config
            WHERE id = {id}

        """.format(id=store_id)

        selected = database.SimpleQuery().select(query)
        if not selected:
            return -1
        elif selected[0]['status'] == 'executing':
            return 1
        else:
            return 0

    def update_scraper_status(self, store_id, status, products_quantity=None):
        '''
        Update scraper status.

        Args:
            store_id (int): Store id
            status (str): Scraper status
            products_quantity (int): Number of products stored in the database

        Returns:
            updated (boolean): The result of update
        '''

        if products_quantity is not None:
            optional = f"products_quantity = {products_quantity},"
        else:
            optional = ''

        query = """
            UPDATE store_config
            SET
                {optional}
                last_execution = '{date}',
                status = '{status}'
            WHERE id = {id}
        """.format(
            optional=optional,
            date=get_current_day(),
            id=store_id,
            status=status
        )
        
        updated = database.SimpleQuery().update(query)
        return updated

    def get_scraper_to_execute(self):
        '''
        Get scraper from store to execute.

        Returns:
            store_id (int): The store id
        '''
        
        query = """
            SELECT
                id
            FROM store_config
            WHERE status = 'to_execute'
            LIMIT 1
        """

        selected = database.SimpleQuery().select(query)
        if selected:
            return selected[0]['id']
        else:
            return None

        updated = database.SimpleQuery().update(query, values)
        return updated

    def create_store_config(self, config):
        '''
        Create store config.

        Args:
            config (Config): Config object

        Returns:
            created (boolean): The result of create
        '''
        
        t = StoreCreationTransaction(config)
        created = t.execute_transaction()
        return created

    def update_store_config(self, config, store_id):
        '''
        Update store config.

        Args:
            config (Config): Config object
            store_id (int): Store id

        Returns:
            updated (boolean): The result of update
        '''
        
        t = StoreUpdateTransaction(config, store_id)
        updated = t.execute_transaction()
        return updated

    def delete_store_config(self, store_id):
        '''
        Delete store config.

        Args:
            store_id (int): Store id

        Returns:
            Deleted (boolean): The result of delete
        '''
        
        t = StoreDeletionTransaction(store_id)
        deleted = t.execute_transaction()
        return deleted

    def update_store_scraping_config(self, config, store_id):
        '''
        Update store scraping config.

        Args:
            config (Config): Config object
            store_id (int): Store id

        Returns:
            updated (boolean): The result of update
        '''
        
        t = StoreUpdateScrapingTransaction(config, store_id)
        updated = t.execute_transaction()
        return updated

    def update_store_json_parser_config(self, config, store_id):
        '''
        Update store JSON parser config.

        Args:
            config (Config): Config object
            store_id (int): Store id

        Returns:
            updated (boolean): The result of update
        '''
        
        t = StoreUpdateJSONParserTransaction(config, store_id)
        updated = t.execute_transaction()
        return updated

class StoreCreationTransaction(database.TransactionQuery):
    ''' StoreCreation using Transaction.

    Args:
        config (Config): Config object

    Attributes:
        config (Config): Config object
    '''

    def __init__(self, config):
        self.config = config

    def execute_queries(self, cursor):
        '''
        Execute queries with transaction.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor
        '''        

        store_config_query = """
            INSERT INTO store_config
                (
                    name,
                    number_of_processes,
                    developer_scraper,
                    parser_type,
                    scraper_type,
                    max_attempts_per_url,
                    retry_delay,
                    retry_attempt_delay,
                    products_quantity,
                    url_base
                )
            VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s, %s, 0, %s
                )
        """

        store_config_values = (
            self.config.name,
            self.config.number_of_processes,
            self.config.developer_scraper,
            self.config.parser_type,
            self.config.scraper_type,
            self.config.max_attempts_per_url,
            self.config.retry_delay,
            self.config.retry_attempt_delay,
            self.config.url_base
        )

        category_query = """
            INSERT INTO category
                (
                    name,
                    store_config_id
                )
            VALUES
                (
                    %s, %s
                )
        """
        
        # inserting store_config
        cursor.execute(store_config_query, store_config_values)

        # getting id from inserted store
        store_id = cursor.lastrowid
        category_values = list((c, store_id) for c in self.config.categories)

        # inserting related category
        cursor.executemany(category_query, category_values)


class StoreUpdateTransaction(database.TransactionQuery):
    ''' StoreUpdate using Transaction.

    Args:
        config (Config): Config object
        store_id (int): Store id

    Attributes:
        config (Config): Config object
        store_id (int): Store id
    '''

    def __init__(self, config, store_id):
        self.config = config
        self.store_id = store_id

    def execute_queries(self, cursor):
        '''
        Execute queries with transaction.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor
        '''        

        store_config_query = """
            UPDATE store_config
            SET
                name = %s,
                number_of_processes = %s,
                developer_scraper = %s,
                parser_type = %s,
                scraper_type = %s,
                max_attempts_per_url = %s,
                retry_delay = %s,
                retry_attempt_delay = %s,
                url_base = %s
            WHERE id = %s
        """

        store_config_values = (
            self.config.name,
            self.config.number_of_processes,
            self.config.developer_scraper,
            self.config.parser_type,
            self.config.scraper_type,
            self.config.max_attempts_per_url,
            self.config.retry_delay,
            self.config.retry_attempt_delay,
            self.config.url_base,
            self.store_id
        )

        delete_category_query = """
            DELETE FROM category
            WHERE store_config_id = %s
        """

        category_query = """
            INSERT INTO category
                (
                    name,
                    store_config_id
                )
            VALUES
                (
                    %s, %s
                )
        """

        category_values = list(
            (c, self.store_id) for c in self.config.categories
        )

        # updating store_config
        cursor.execute(store_config_query, store_config_values)

        # deleting related category
        cursor.execute(delete_category_query, (self.store_id, ))

        # inserting related category
        cursor.executemany(category_query, category_values)


class StoreUpdateScrapingTransaction(database.TransactionQuery):
    ''' StoreUpdateScraping using Transaction.

    Args:
        config (Config): Config object
        store_id (int): Store id

    Attributes:
        config (Config): Config object
        store_id (int): Store id
    '''

    def __init__(self, config, store_id):
        self.config = config
        self.store_id = store_id

    def execute_queries(self, cursor):
        '''
        Execute queries with transaction.

        99% of 'select' are 'select_one', this option can be left for one future
        version.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor
        '''        

        store_config_query = """
            UPDATE store_config
            SET
                url_paging_extras = %s,
                url_test = %s,
                items_per_page = %s,
                product_nodes_tag = %s,
                get_brand = %s,
                get_category = %s,
                get_category_by_first_name = %s,
                name_select = 'select_one',
                name_select_str = %s,
                name_get = %s,
                name_get_str = %s,
                image_select = 'select_one',
                image_select_str = %s,
                image_get = %s,
                image_get_str = %s,
                url_select = 'select_one',
                url_select_str = %s,
                url_get = %s,
                url_get_str = %s,
                brand_select = 'select_one',
                brand_select_str = %s,
                brand_get = %s,
                brand_get_str = %s,
                category_select = 'select_one',
                category_select_str = %s,
                category_get = %s,
                category_get_str = %s,
                old_price_node_select = 'select_one',
                old_price_node_select_str = %s,
                old_price_select = 'select_one',
                old_price_select_str = %s,
                old_price_get = %s,
                old_price_get_str = %s,
                old_price_get_price = %s,
                new_price_select = 'select_one',
                new_price_select_str = %s,
                new_price_get = %s,
                new_price_get_str = %s,
                new_price_get_price = %s,
                sale_price_select = 'select_one',
                sale_price_select_str = %s,
                sale_price_get = %s,
                sale_price_get_str = %s,                
                sale_price_get_price = %s
            WHERE id = %s
        """

        store_config_values = (
            self.config.url_paging_extras,
            self.config.url_test,
            self.config.items_per_page,
            self.config.product_nodes_tag,
            self.config.get_brand,
            self.config.get_category,
            self.config.get_category_by_first_name,
            self.config.name_select_str,
            self.config.name_get,
            self.config.name_get_str,
            self.config.image_select_str,
            self.config.image_get,
            self.config.image_get_str,
            self.config.url_select_str,
            self.config.url_get,
            self.config.url_get_str,
            self.config.brand_select_str,
            self.config.brand_get,
            self.config.brand_get_str,
            self.config.category_select_str,
            self.config.category_get,
            self.config.category_get_str,
            self.config.old_price_node_select_str,
            self.config.old_price_select_str,
            self.config.old_price_get,
            self.config.old_price_get_str,
            self.config.old_price_get_price,
            self.config.new_price_select_str,
            self.config.new_price_get,
            self.config.new_price_get_str,
            self.config.new_price_get_price,
            self.config.sale_price_select_str,
            self.config.sale_price_get,
            self.config.sale_price_get_str,
            self.config.sale_price_get_price,
            self.store_id
        )

        delete_regex_query = """
            DELETE FROM regex
            WHERE store_config_id = %s
        """

        regex_query = """
            INSERT INTO regex
                (
                    sequence,
                    store_config_id
                )
            VALUES
                (
                    %s, %s
                )
        """

        regex_values = list((c, self.store_id) for c in self.config.regexes)

        # updating store_config
        cursor.execute(store_config_query, store_config_values)

        # deleting related regexes
        cursor.execute(delete_regex_query, (self.store_id, ))        

        # inserting related regexes
        cursor.executemany(regex_query, regex_values)


class StoreUpdateJSONParserTransaction(database.TransactionQuery):
    ''' StoreUpdateJSONParser using Transaction.

    Args:
        config (Config): Config object
        store_id (int): Store id

    Attributes:
        config (Config): Config object
        store_id (int): Store id
    '''

    def __init__(self, config, store_id):
        self.config = config
        self.store_id = store_id

    def execute_queries(self, cursor):
        '''
        Execute queries with transaction.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor
        '''        

        store_config_query = """
            UPDATE store_config
            SET
                url_api = %s,
                url_json_paging_extras = %s,
                url_json_test = %s,
                items_per_page_json = %s,
                product_nodes_keys = %s,
                get_brand_json = %s,
                get_category_json = %s,
                get_category_by_first_name_json = %s,
                name_keys = %s,
                image_keys = %s,
                url_keys = %s,
                sku_keys = %s,
                brand_keys = %s,
                category_keys = %s,
                old_price_node_keys = %s,
                old_price_keys = %s,
                old_price_get_price_json = %s,
                new_price_keys = %s,
                new_price_get_price_json = %s,
                sale_price_keys = %s,
                sale_price_get_price_json = %s
            WHERE id = %s
        """

        store_config_values = (
            self.config.url_api,
            self.config.url_json_paging_extras,
            self.config.url_json_test,
            self.config.items_per_page_json,
            self.config.product_nodes_keys,
            self.config.get_brand_json,
            self.config.get_category_json,
            self.config.get_category_by_first_name_json,
            self.config.name_keys,
            self.config.image_keys,
            self.config.url_keys,
            self.config.sku_keys,
            self.config.brand_keys,
            self.config.category_keys,
            self.config.old_price_node_keys,
            self.config.old_price_keys,
            self.config.old_price_get_price_json,
            self.config.new_price_keys,
            self.config.new_price_get_price_json,
            self.config.sale_price_keys,
            self.config.sale_price_get_price_json,
            self.store_id
        )

        delete_category_query = """
            DELETE FROM category_json
            WHERE store_config_id = %s
        """

        category_query = """
            INSERT INTO category_json
                (
                    name,
                    store_config_id
                )
            VALUES
                (
                    %s, %s
                )
        """

        category_values = list(
            (c, self.store_id) for c in self.config.categories_json
        )

        # updating store_config
        cursor.execute(store_config_query, store_config_values)

        # deleting related regexes
        cursor.execute(delete_category_query, (self.store_id, ))        

        # inserting related regexes
        cursor.executemany(category_query, category_values)


class StoreDeletionTransaction(database.TransactionQuery):
    ''' StoreUpdateDeletion using Transaction.

    Args:
        store_id (int): Store id

    Attributes:
        store_id (int): Store id
    '''

    def __init__(self, store_id):
        self.store_id = store_id

    def execute_queries(self, cursor):
        '''
        Execute queries with transaction.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor
        '''        

        category_query = """
            DELETE FROM category
            WHERE store_config_id = %s
        """

        regex_query = """
            DELETE FROM regex
            WHERE store_config_id = %s
        """

        store_config_query = """
            DELETE FROM store_config
            WHERE id = %s
        """

        cursor.execute(category_query, (self.store_id, ))
        cursor.execute(regex_query, (self.store_id, ))
        cursor.execute(store_config_query, (self.store_id, ))


# DEBUG INICIAL
# INFOS JAH ESTAO NO DATABASE
# WorldTenisConfig
#     
#     categories = [
#         'tenis-feminino',
#         'tenis-masculino',
#         'tenis-infantil',
#         'tenis-de-corrida'
#     ]   

#     url_base = 'http://www.wtennis.com.br'
#     url_paging_extras = '?p='
#     url_test = 'http://www.wtennis.com.br/tenis-feminino?p=2'

#     product_nodes_tag = '.item'

#     name_select_str = '.product-name'
#     name_get = 'get_text'

#     image_select_str = '.product-image'
#     image_get = 'get'
#     image_get_str = 'src'

#     url_select_str = '.product-name a'
#     url_get = 'get'
#     url_get_str = 'href'

#     sku_regexes = [r".com.br/(.+)?"]

#     old_price_node_select_str = '.old-price'

#     old_price_select_str = '.price'
#     old_price_get = 'get_text'
#     old_price_get_price = True

#     new_price_select_str = '.special-price .price'
#     new_price_get = 'get_text'
#     new_price_get_price = True

#     sale_price_select_str = '.regular-price .price'
#     sale_price_get = 'get_text'
#     sale_price_get_price = True


#  MarabrazConfig

#     categories = [
#         'moveis/moveis-escritorio/mesas-para-computador',
#         'moveis/moveis-escritorio/cadeiras-de-escritorio',
#         'moveis/moveis-escritorio/estantes-para-escritorio',
#         'moveis/moveis-escritorio/gaveteiros'
#     ]

#     Config 2
#     moveis/moveis-escritorio/mesas-para-computador
#     moveis/moveis-escritorio/cadeiras-de-escritorio 
#     moveis/moveis-cozinha/armarios-modulares
#     moveis/moveis-para-sala-de-estar/racks

#     url_base = 'http://www.marabraz.com.br'
#     url_paging_extras = '.html?p='
#     url_test = 'https://www.marabraz.com.br/moveis/moveis-escritorio/mesas-para-computador.html?p=2'

#     product_nodes_tag = '.item'
#     sku_regexes = [r"--(\w+).html"]

#     name_select_str = '.product-name'
#     name_get = 'get_text'

#     image_select_str = '.container-product-img img'
#     image_get = 'get'
#     image_get_str = 'data-src'

#     url_select_str = '.container-product-img'
#     url_get = 'get'
#     url_get_str = 'href'

#     old_price_node_select_str = '.old-price'

#     old_price_select_str = '.price'
#     old_price_get = 'get_text'
#     old_price_get_price = True

#     new_price_select_str = '.special-price .price'
#     new_price_get = 'get_text'
#     new_price_get_price = True

#     sale_price_select_str = '.special-price .price'
#     sale_price_get = 'get_text'
#     sale_price_get_price = True


"""
Renner
product_node_keys = 'contentItem contents [0] records'
name_keys = 'attributes prop.product.displayName [0]'
image_keys = 'attributes prop.product.largeImageUrl [0]'
url_keys = 'attributes prop.product.url [0]'
sku_keys = 'attributes prop.product.defaultSku [0]'
brand_keys = 'attributes prop.product.brand.name [0]'
category_keys = 'attributes dim.product.categoryHierarchy [0]'
sale_price_keys = 'attributes prop.sku.activePrice [0]'

categorias
contentPath=/content/Shared/Results%20List/Cat%20Masculino/Results%20List%20Cat%20Masculino&N=1iw5q9o
contentPath=/content/Shared/Results%20List/Cat%20Masculino/Results%20List%20Cat%20Masculino%20-%20Relogios%20Masc&N=1lbg86e

url de teste
https://www.lojasrenner.com.br/rest/model/lrsa/api/CatalogActor/resultsList?pushSite=rennerBrasilDesktop&contentPath=/content/Shared/Results%20List/Cat%20Masculino/Results%20List%20Cat%20Masculino%20-%20Relogios%20Masc&contentPathFilter=/content/Shared/Record%20Filter/Product&Ns=&Ntt=&No=48&N=1lbg86e&Nf=&isAjax=true

offset = 48
"""

"""
Hering
    url_paging_extras = 'store/pt/search?q=%3Aname-asc&page='
    url_test = 'https://www.hering.com.br/store/pt/search?q=%3Aname-asc&page=88'
    product_nodes_tag = '.box-product'
    sku_regexes = [r"-(\w+)\? -(\w+)$"]

    name_select_str = '.box-product__footer a'
    name_get = 'get_text'

    image_select_str = '.image-prod a'
    image_get = 'get'
    image_get_str = 'href'

    url_select_str = '.box-product__footer a'
    url_get = 'get'
    url_get_str = 'href'

    old_price_node_select_str = '.old-price'

    new_price_select_str = '.price'
    new_price_get = 'get_text'
    new_price_get_price = True

    sale_price_select_str = '.price'
    sale_price_get = 'get_text'
    sale_price_get_price = True
"""