from model.database import *
import sys


class InstallDatabase(object):
    '''
    Database installation class.

    Attributes:
        sq (SimpleQuery): Object that make the queries
    '''

    def __init__(self):
        self.sq = SimpleQuery()
        self.create_database_project()
        self.create_table_store_config()
        self.create_table_category()
        self.create_table_category_json()
        self.create_table_regex()
        self.create_table_comparison()
        self.create_table_product()

        # passar para o create quando for possível
        self.update_table_store_config()

    def create_database_project(self):
        ''' Create database query.'''        

        created = self.sq.create_database("projeto_scrapper")
        if not created:
            sys.exit()

    def create_table_store_config(self):
        ''' Create Table query.'''        
        
        name = 'store_config'
        exists = self.sq.table_exists(name)
        if exists == -1:
            sys.exit()
        elif exists:
            print(f"Tabela {name} já existe.")
        else:
            criada = self.sq.create_table(
                """
                    CREATE TABLE {name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        status VARCHAR(255),
                        last_execution DATE,
                        products_quantity INT,
                        developer_scraper BOOLEAN,
                        number_of_processes INT,
                        scraper_type VARCHAR(255),
                        max_attempts_per_url INT,
                        retry_attempt_delay INT,
                        retry_delay INT,
                        url_base VARCHAR(255),
                        url_paging_extras VARCHAR(255),
                        url_test VARCHAR(255),
                        product_nodes_tag VARCHAR(255),
                        name_select VARCHAR(255),
                        name_select_str VARCHAR(255),
                        name_get VARCHAR(255),
                        name_get_str VARCHAR(255),
                        image_select VARCHAR(255),
                        image_select_str VARCHAR(255),
                        image_get VARCHAR(255),
                        image_get_str VARCHAR(255),
                        url_select VARCHAR(255),
                        url_select_str VARCHAR(255),
                        url_get VARCHAR(255),
                        url_get_str VARCHAR(255),
                        get_brand BOOLEAN,
                        get_category BOOLEAN,
                        get_category_by_first_name BOOLEAN,
                        brand_select VARCHAR(255),
                        brand_select_str VARCHAR(255),
                        brand_get VARCHAR(255),
                        brand_get_str VARCHAR(255),
                        category_select VARCHAR(255),
                        category_select_str VARCHAR(255),
                        category_get VARCHAR(255),
                        category_get_str VARCHAR(255),
                        sku_regexes VARCHAR(255),
                        old_price_node_select VARCHAR(255),
                        old_price_node_select_str VARCHAR(255),
                        old_price_select VARCHAR(255),
                        old_price_select_str VARCHAR(255),
                        old_price_get VARCHAR(255),
                        old_price_get_str VARCHAR(255),
                        old_price_get_price BOOLEAN,
                        new_price_select VARCHAR(255),
                        new_price_select_str VARCHAR(255),
                        new_price_get VARCHAR(255),
                        new_price_get_str VARCHAR(255),
                        new_price_get_price BOOLEAN,
                        sale_price_select VARCHAR(255),
                        sale_price_select_str VARCHAR(255),
                        sale_price_get VARCHAR(255),
                        sale_price_get_str VARCHAR(255),
                        sale_price_get_price BOOLEAN,
                        items_per_page INT,
                        parser_type VARCHAR(255),
                        url_json_paging_extras VARCHAR(255),
                        url_json_test LONGTEXT,
                        product_nodes_keys VARCHAR(255),
                        sku_keys VARCHAR(255),
                        name_keys VARCHAR(255),
                        url_keys VARCHAR(255),
                        image_keys VARCHAR(255),
                        brand_keys VARCHAR(255),
                        category_keys VARCHAR(255),
                        old_price_keys VARCHAR(255),
                        new_price_keys VARCHAR(255),
                        sale_price_keys VARCHAR(255),
                        get_brand_json BOOLEAN,
                        get_category_json BOOLEAN,
                        get_category_by_first_name_json BOOLEAN,
                        new_price_get_price_json BOOLEAN,
                        old_price_get_price_json BOOLEAN,
                        sale_price_get_price_json BOOLEAN,
                        url_api VARCHAR(255),
                        old_price_node_keys VARCHAR(255)
                    )
                """.format(name=name)
            )
            if criada:
                print("Tabela {} criada.".format(name))
            else:
                sys.exit()
    
    def create_table_category(self):
        ''' Create Table query.'''

        name = 'category'
        exists = self.sq.table_exists(name)
        if exists == -1:
            sys.exit()
        elif exists:
            print(f"Tabela {name} já existe.")
        else:
            criated = self.sq.create_table(
                """
                    CREATE TABLE {name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        store_config_id INT,
                        INDEX idx_category_store_config_id
                        (store_config_id ASC) VISIBLE,
                        CONSTRAINT fk_category_store_config
                        FOREIGN KEY (store_config_id)
                        REFERENCES store_config (id)
                    )
                """.format(name=name)
            )
            if criated:
                print(f"Tabela {name} criada.")
            else:
                sys.exit()

    def create_table_category_json(self):
        ''' Create Table query.'''

        name = 'category_json'
        exists = self.sq.table_exists(name)
        if exists == -1:
            sys.exit()
        elif exists:
            print(f"Tabela {name} já existe.")
        else:
            criated = self.sq.create_table(
                """
                    CREATE TABLE {name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        store_config_id INT,
                        INDEX idx_category_json_store_config_id
                        (store_config_id ASC) VISIBLE,
                        CONSTRAINT fk_category_json_store_config
                        FOREIGN KEY (store_config_id)
                        REFERENCES store_config (id)
                    )
                """.format(name=name)
            )
            if criated:
                print(f"Tabela {name} criada.")
            else:
                sys.exit()

    def create_table_regex(self):
        ''' Create Table query.'''

        name = 'regex'
        exists = self.sq.table_exists(name)
        if exists == -1:
            sys.exit()
        elif exists:
            print(f"Tabela {name} já existe.")
        else:
        
            criated = self.sq.create_table(
                """
                    CREATE TABLE {name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        sequence VARCHAR(255),
                        store_config_id INT,
                        INDEX idx_regex_store_config_id
                        (store_config_id ASC) VISIBLE,
                        CONSTRAINT fk_rexes_store_config
                        FOREIGN KEY (store_config_id)
                        REFERENCES store_config (id)
                    )
                """.format(name=name)
            )
            if criated:
                print(f"Tabela {name} criada.")
            else:
                sys.exit()

    def create_table_comparison(self):
        ''' Create Table query.'''

        name = 'comparison'
        exists = self.sq.table_exists(name)
        if exists == -1:
            sys.exit()
        elif exists:
            print(f"Tabela {name} já existe.")
        else:
            created = self.sq.create_table(
                """
                    CREATE TABLE {name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        sku VARCHAR(255)
                    )
                """.format(name=name)
            )
            if created:
                print("Tabela {} criada.".format(name))
            else:
                sys.exit()

    def create_table_product(self):
        ''' Create Table query.'''

        name = 'product'
        exists = self.sq.table_exists(name)
        if exists == -1:
            sys.exit()
        elif exists:
            print(f"Tabela {name} já existe.")
        else:
            created = self.sq.create_table(
                """
                    CREATE TABLE {name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        sku VARCHAR(255),
                        name VARCHAR(255),
                        url VARCHAR(255),
                        image VARCHAR(255),
                        brand VARCHAR(255),
                        category VARCHAR(255),
                        store_id INT,
                        old_price FLOAT,
                        sale_price FLOAT,
                        comparison_id INT,
                        INDEX idx_product_store_config_id
                        (store_id ASC) VISIBLE,
                        CONSTRAINT fk_product_store_config
                        FOREIGN KEY (store_id)
                        REFERENCES store_config (id),
                        INDEX idx_product_comparison_id
                        (comparison_id ASC) VISIBLE,
                        CONSTRAINT fk_product_comparison
                        FOREIGN KEY (comparison_id)
                        REFERENCES comparison (id)              
                    )
                """.format(name=name)
            )
            if created:
                print("Tabela {} criada.".format(name))
            else:
                sys.exit()

    def update_table_store_config(self):
        '''
        Alter Table query. Use for punctual updates. Insert new fields in
        CREATE TABLE queries when consolidated.
        '''

        name = 'store_config'

        # updated = self.sq.alter_table(
        #     """
                
        #     """.format(name=name)
        # )


InstallDatabase()