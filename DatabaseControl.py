import mysql.connector


class DatabaseControl:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def all_tables(self):
        self.cursor.execute(f"SHOW TABLES")
        return self.cursor.fetchall()

    def features(self, table, type=''):
        self.cursor.execute(f"SELECT * FROM {table}")
        num_fields = len(self.cursor.description)
        field_names = [i[0] for i in self.cursor.description]
        print(f'>{table} ({num_fields} cols): ', end='')
        for i in field_names:
            print(i, end=', ')
        print()
        if 'columns' in type:
            self.connection.close()
            return field_names
        else:
            return self.cursor.fetchall()

    def create(self, table, data):
        insert_query = f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({', '.join(['%s'] * len(data))})"
        self.cursor.execute(insert_query, list(data.values()))
        self.connection.commit()
        return self.cursor.lastrowid

    def read(self, table, condition=None, column='*'):
        query = f"SELECT {column} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def read_as_dict(self, table, condition=None, column='*'):
        query = f"SELECT {column} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        # result = self.cursor.fetchall()
        # print(self.cursor.description)
        column_names = [i[0] for i in self.cursor.description]
        # print(column_names)
        result = []
        for row in self.cursor.fetchall():
            row_dict={}
            for i, column_name in enumerate(column_names):
                row_dict[column_name]=row[i]
            result.append(row_dict)

        return result

    def update(self, table, data, condition):
        update_query = f"UPDATE {table} SET {', '.join([f'{key}=%s' for key in data.keys()])} WHERE {condition}"
        self.cursor.execute(update_query, list(data.values()))
        self.connection.commit()

    def delete(self, table, condition):
        delete_query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(delete_query)
        self.connection.commit()

    def resetIncrement(self, table, value):
        delete_query = f"ALTER TABLE {table} AUTO_INCREMENT = {value};"
        self.cursor.execute(delete_query)
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
