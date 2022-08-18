from model import database


""" The parameter 'values' in cursor.execute() is used to avoid SQL INJECTION,
except when it is the 'id' field (user cannot insert).
"""


class Product(object):
    ''' Model Product.'''

    def select_all_products(self, store_id_list):
        '''
        Select all products from a list of stores.

        Args:
            store_id_list (list): List of store ids

        Returns:
            products (list): All products from a list of stores
        '''
        
        query = """
            SELECT
                pr.sku,
                pr.name,
                pr.url,
                pr.image,
                pr.brand,
                pr.category,
                pr.old_price,
                pr.sale_price,
                sc.name as store
            FROM product pr
            INNER JOIN store_config sc
            ON pr.store_id = sc.id
            WHERE pr.store_id in ({parameters})  
        """.format(parameters=','.join(['%s'] * len(store_id_list)))

        return database.SimpleQuery().select(query, tuple(store_id_list))
    
    def select_products_group_by_category(self, store_id_list):
        '''
        Select all products grouped by category from a list of stores.

        Args:
            store_id_list (list): List of store ids

        Returns:
            products (list): All products grouped by category from a list of
                             stores
        '''
        
        query = """
            SELECT
                category,
                COUNT(id) as quantity,
                AVG(old_price) as avg_old_price,
                AVG(sale_price) as avg_sale_price,
                MIN(old_price) as min_old_price,
                MAX(old_price) as max_old_price,
                MIN(sale_price) as min_sale_price,
                MAX(sale_price) as max_sale_price
            FROM product
            WHERE store_id in ({parameters})  
            GROUP BY category
        """.format(parameters=','.join(['%s'] * len(store_id_list)))

        return database.SimpleQuery().select(query, tuple(store_id_list))

    def save_products(self, products_by_id, store_id):
        '''
        Save products.

        Args:
            products_by_id (dict): Products to save

        Returns:
            save (boolean): The result of save
        '''
        
        t = ProductSavingTransaction(products_by_id, store_id)
        saved = t.execute_transaction()
        return saved


class ProductSavingTransaction(database.TransactionQuery):
    ''' ProductSaving using Transaction.

    Args:
        products_by_id (dict): Products to save
        store_id (int): Store id

    Attributes:
        products_by_id (dict): Products to save
        store_id (int): Store id
    '''

    def __init__(self, products_by_id, store_id):
        self.products_by_id = products_by_id
        self.store_id = store_id

    def execute_queries(self, cursor):
        '''
        Execute queries with transaction.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor
        '''        

        delete_query = """
            DELETE FROM product
            WHERE store_id = %s
        """

        insert_query = """
            INSERT INTO product
                (
                    sku,
                    name,
                    url,
                    image,
                    brand,
                    category,
                    old_price,
                    sale_price,
                    store_id
                )
            VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
        """

        product_values = []
        for product in self.products_by_id.values():
            # get pega o valor, caso contrario None
            product_values.append(
                (
                    product.get('sku'),
                    product.get('name'),
                    product.get('url'),
                    product.get('image'),
                    product.get('brand'),
                    product.get('category'),
                    product.get('old_price'),
                    product.get('sale_price'),
                    self.store_id
                )
            )

        cursor.execute(delete_query, (self.store_id, ))
        cursor.executemany(insert_query, product_values)

