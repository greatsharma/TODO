import sqlite3


class DBHelper():
    
    def __init__(self, dbname_):
        self.dbname_ = dbname_


    def connect_db(self):
        try:
            self.conn = sqlite3.connect(self.dbname_)
        except Exception as e:
            print('\nunable to connect to db, error descr -> \n{}'.format(e))
            return False

        return True


    def create_table(self, table_name, column_with_type):
        try:
            query = 'CREATE TABLE IF NOT EXISTS {}('.format(table_name)
            for key, val in column_with_type.items():
                query += (key + ' ' + val + ',')

            query = query.rstrip(',')
            query += ')' 

            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            print('\nunable to create table, error descr -> \n{}'.format(e))
            return False

        return True


    def create_index(self, table_name, column_name, index_name, order):
        try:
            query = 'CREATE INDEX IF NOT EXISTS {} ON {} ( {} {})'.\
                    format(index_name, table_name, column_name, order)
            
            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            print('\nunable to create index, error descr -> \n{}'.format(e))
            return False

        return True


    def add_item(self, table_name, column_item_name):
        try:
            query = 'INSERT INTO {} ('.format(table_name)
            
            for col in column_item_name.keys():
                query += (col + ',')
            
            query = query.rstrip(',')
            query += ') VALUES ('

            items = list(column_item_name.values())

            for _ in items:
                query += '?,'

            query = query.rstrip(',')
            query+= ')'

            self.conn.execute(query, items)
            self.conn.commit()
        except Exception as e:
            print('\nunable to add item, error descr -> \n{}'.format(e))
            return False

        return True


    def add_multiple_items(self, table_name, column_names, rows):
        try:
            query = 'INSERT INTO {} ('.format(table_name)
            
            for col in column_names:
                query += (col + ',')
            
            query = query.rstrip(',')
            query += ') VALUES ('

            for _ in column_names:
                query += '?,'

            query = query.rstrip(',')
            query+= ')'

            cur = self.conn.cursor()
            cur.executemany(query, rows)
            self.conn.commit()
        except Exception as e:
            print('\nunable to add item, error descr -> \n{}'.format(e))
            return False

        return True


    def delete_item(self, table_name, condition):
        try:
            query = 'DELETE FROM {} WHERE '.format(table_name)
            query += condition
        
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print('\nunable to delete item, error descr -> \n{}'.format(e))
            return False, 'unable to remove item.'

        return cur.rowcount, 'item doesn\'t exists, add it to the list.'


    def delete_all_items(self, table_name):
        try:
            query = 'DELETE FROM {}'.format(table_name)
            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            print('\nunable to delete all items, error descr -> \n{}'.format(e))
            return False

        return True


    def fetch_items(self, table_name, column_names, condition):
        try:
            query = 'SELECT {} FROM {} WHERE {}'.format(column_names, table_name, condition)
            
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()           
        except Exception as e:
            print('\nunable to fetch items, error descr -> \n{}'.format(e))
            return None

        return rows


    def fetch_all_items(self, table_name, column_names):
        try:
            query = 'SELECT {} FROM {}'.format(column_names, table_name)
            
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()           
        except Exception as e:
            print('\nunable to fetch items, error descr -> \n{}'.format(e))
            return None

        return rows


    def search_item(self, table_name, condition, return_list = False):
        try:
            query = 'SELECT * FROM {} WHERE '.format(table_name)
            query += condition
        
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        except Exception as e:
            print('\nunable to search item, error descr -> \n{}'.format(e))

        if return_list: return rows
        else: return len(rows)


    def advanced_search(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        except Exception as e:
            print('\nunable to advanced search, error descr -> \n{}'.format(e))

        return rows


    def close_connection(self):
        self.conn.close()
        return self.conn is None