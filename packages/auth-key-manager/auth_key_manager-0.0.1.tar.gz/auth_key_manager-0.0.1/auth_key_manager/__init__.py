import mysql.connector
from pymongo import MongoClient
import random
import string
import datetime
import importlib
import requests
from .update_checker import UpdateChecker


class AuthKeyManager:
    def __init__(self, db_type, connection_params, db_name, table_name, column_user_id, column_license_key, column_created_at):
        self.update_checker = UpdateChecker()
        self.update_checker.check_for_updates()

        self.db_type = db_type
        self.connection_params = connection_params
        self.db_name = db_name
        self.table_name = table_name
        self.column_user_id = column_user_id
        self.column_license_key = column_license_key
        self.column_created_at = column_created_at

        try:
            if db_type == "mysql":
                self.conn = mysql.connector.connect(**connection_params)
                self.cursor = self.conn.cursor()

                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                self.conn.commit()

                connection_params["database"] = db_name
                self.conn = mysql.connector.connect(**connection_params)
                self.cursor = self.conn.cursor()

                self.create_table_mysql()

            elif db_type == "mongodb":
                client = MongoClient(**connection_params)
                self.db = client[db_name]
                self.collection = self.db[table_name]
        except Exception as e:
            raise Exception(f"Database connection error: {str(e)}")

    def create_table_mysql(self):
        try:
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {self.column_user_id} VARCHAR(255),
                {self.column_license_key} VARCHAR(255) UNIQUE,
                {self.column_created_at} TIMESTAMP
            );
            '''
            self.cursor.execute(create_table_query)
            self.conn.commit()
        except mysql.connector.Error as err:
            raise Exception(f"MySQL table creation error: {str(err)}")

    def generate_license_key(self, length=12):
        prefix = "LICENSE-"
        charset = string.ascii_uppercase + string.digits
        license_key = ''.join(random.choices(charset, k=length))
        grouped_key = '-'.join([license_key[i:i+4] for i in range(0, len(license_key), 4)])
        return prefix + grouped_key

    def create_license_record(self, user_id):
        created_at = datetime.datetime.now()
        license_key = self.generate_license_key()
        if self.db_type == "mysql":
            try:
                save_query = f'''
                INSERT INTO {self.table_name} ({self.column_user_id}, {self.column_license_key}, {self.column_created_at})
                VALUES (%s, %s, %s);
                '''
                self.cursor.execute(save_query, (user_id, license_key, created_at))
                self.conn.commit()
                return license_key
            except mysql.connector.Error as err:
                raise Exception(f"MySQL save error: {str(err)}")

        elif self.db_type == "mongodb":
            try:
                self.collection.insert_one({
                    self.column_license_key: license_key,
                    self.column_created_at: created_at,
                    self.column_user_id: user_id
                })
                return license_key
            except Exception as e:
                raise Exception(f"MongoDB save error: {str(e)}")

    def query_license_keys(self, user_id, include_date=False):
        if self.db_type == "mysql":
            try:
                if include_date:
                    query = f"SELECT {self.column_license_key}, {self.column_date} FROM {self.table_name} WHERE {self.column_user_id} = %s;"
                else:
                    query = f"SELECT {self.column_license_key} FROM {self.table_name} WHERE {self.column_user_id} = %s;"
                
                self.cursor.execute(query, (user_id,))
                results = self.cursor.fetchall()

                if include_date:
                    return [{"license_key": row[0], "date": row[1]} for row in results] if results else []
                else:
                    return [row[0] for row in results] if results else []
            except mysql.connector.Error as err:
                raise Exception(f"MySQL query error: {str(err)}")
        elif self.db_type == "mongodb":
            try:
                results = self.collection.find({self.column_user_id: user_id})
                if include_date:
                    return [{"license_key": result[self.column_license_key], "date": result[self.column_created_at]} for result in results]
                else:
                    return [result[self.column_license_key] for result in results]
            except Exception as e:
                raise Exception(f"MongoDB query error: {str(e)}")

    def validate_license_key(self, user_id, license_key):
        if self.db_type == "mysql":
            try:
                query = f"SELECT * FROM {self.table_name} WHERE {self.column_user_id} = %s AND {self.column_license_key} = %s;"
                self.cursor.execute(query, (user_id, license_key))
                result = self.cursor.fetchone()
                return bool(result)
            except mysql.connector.Error as err:
                raise Exception(f"MySQL validation error: {str(err)}")

        elif self.db_type == "mongodb":
            try:
                result = self.collection.find_one({self.column_license_key: license_key, self.column_user_id: user_id})
                return bool(result)
            except Exception as e:
                raise Exception(f"MongoDB validation error: {str(e)}")

    def delete_license_key(self, user_id, license_key):
        if self.db_type == "mysql":
            try:
                delete_query = f"DELETE FROM {self.table_name} WHERE {self.column_user_id} = %s AND {self.column_license_key} = %s;"
                self.cursor.execute(delete_query, (user_id, license_key))
                self.conn.commit()
                return self.cursor.rowcount > 0
            except mysql.connector.Error as err:
                raise Exception(f"MySQL deletion error: {str(err)}")

        elif self.db_type == "mongodb":
            try:
                result = self.collection.delete_one({self.column_user_id: user_id, self.column_license_key: license_key})
                return result.deleted_count > 0
            except Exception as e:
                raise Exception(f"MongoDB deletion error: {str(e)}")

    def close_connection(self):
        try:
            if self.db_type == "mysql":
                self.cursor.close()
                self.conn.close()
            elif self.db_type == "mongodb":
                pass
        except Exception as e:
            raise Exception(f"Connection close error: {str(e)}")
