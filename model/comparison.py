from model import database


""" The parameter 'values' in cursor.execute() is used to avoid SQL INJECTION,
except when it is the 'id' field (user cannot insert).
"""


class Comparison(object):
    ''' Model Comparison.'''

    def update_products(self, new_products):
        '''
        Update products.

        Args:
            new_products (list): Products to update

        Returns:
            updated (boolean): The result of update
        '''
        
        t = ProductComparisonUpdateTransaction(new_products)
        updated = t.execute_transaction()
        return updated

    def select_all_comparison(self):
        '''
        Select all comparison.

        Returns:
            products (list): Áll comparison
        '''
        
        query = """
            SELECT
                cm.sku,
                pr.sale_price,
                st.name as store,
                pr.url
            FROM product pr
            INNER JOIN comparison cm
            ON pr.comparison_id = cm.id
            INNER JOIN store_config st
            ON pr.store_id = st.id
        """

        return database.SimpleQuery().select(query)
        

class ProductComparisonUpdateTransaction(database.TransactionQuery):
    ''' ProductComparisonUpdate using Transaction.

    Args:
        new_products (list): Products to update

    Attributes:
        new_products (list): Products to update
    '''

    def __init__(self, new_products):
        self.new_products = new_products

    def execute_queries(self, cursor):
        '''
        Execute queries with transaction.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor
        '''        

        # clean old compared products
        cleaning_query = """
            UPDATE product
            SET
                comparison_id = Null
        """
        cursor.execute(cleaning_query)

        delete_query = "DELETE FROM comparison"
        cursor.execute(delete_query)

        # insert new compared products
        insert_query = """
            INSERT INTO comparison
                (
                    sku
                )
            VALUES
                (
                    %s
                )
        """        
        
        for product in self.new_products:
            sku = product['produto']
            cursor.execute(insert_query, (sku, ))
            product_id = cursor.lastrowid

            for store, sku in product.items(): 

                if store == 'produto':
                    continue

                if type(sku == int):
                    sku = str(sku)

                if type(sku) != str:
                    continue

                update_query = f"""
                    UPDATE product
                    SET
                        comparison_id = %s
                    WHERE sku = %s
                    AND store_id = (
                        SELECT id
                        FROM store_config
                        WHERE name = %s
                    )
                """

                update_values = (product_id, sku, store)

                cursor.execute(update_query, update_values)

            """ Se fizer do jeito abaixo não filtra por loja e pode ficar
            incorreto caso existir o mesmo sku em lojas diferentes
            """

            # skus = [
            #     y for x, y in product.items() 
            #     if type(y) == str and x != 'produto'
            # ]
            
            # https://stackoverflow.com/questions/5766230/select-from-sqlite-table-where-rowid-in-list-using-python-sqlite3-db-api-2-0
            # update_query = f"""
            #     UPDATE product
            #     SET
            #         comparison_id = %s
            #     WHERE sku in ({','.join(['%s']*len(skus))})
            # """
            
            # update_values = [product_id] + skus

            # cursor.execute(update_query, update_values)



