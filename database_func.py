import mysql.connector
from dotenv import load_dotenv
import os


class database_func:
    def __init__(self):
        load_dotenv()
        connection_config_dict = {
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD'),
            'host': os.getenv('HOST'),
            'database': os.getenv('DATABASE'),
            'raise_on_warnings': True,
        }
        self.connection = mysql.connector.connect(**connection_config_dict)
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            self.cursor = self.connection.cursor()
            print(db_Info)

    def add_user(self, name, server, timezone):
        # insert a user into the user table given
        # username, serverid, and timezone
        insert_stmt = "insert into Users (username,servers,time_zone)""Values (%s, %s,%s)"
        data = (name, server, timezone)
        self.cursor.execute(insert_stmt, data)
        self.connection.commit()
        print("Inserted successfully")

    def add_class(self, class_name, server):
        insert_stmt = "insert into Classes (class_name,servers)""Values (%s, %s)"
        data = (class_name, server)
        self.cursor.execute(insert_stmt, data)
        self.connection.commit()
        print("Inserted successfully" % class_name)

    def delete_user(self, name):
        delete_stmt = "delete from Users where username = %s"
        data = (name,)
        self.cursor.execute(delete_stmt, data)
        self.connection.commit()
        print("delete %s successfully" % name)

    def delete_class(self, class_name):
        delete_stmt = "delete from Classes where class_name = %s"
        data = (class_name,)
        self.cursor.execute(delete_stmt, data)
        self.connection.commit()
        print("delete %s successfully" % class_name)

    def users_in_class(self, class_id):
        select_stmt = "select Users.username from Users join Enrollments on Users.user_id = Enrollments.user_id where Enrollments.class_id =%s"
        data = (class_id,)
        self.cursor.execute(select_stmt, data)
        results = self.cursor.fetchall()
        for x in results:
            print(x)

    def print_all_users(self):
        select_stmt = "select* from Users"
        self.cursor.execute(select_stmt)
        results = self.cursor.fetchall()
        for x in results:
            print(x)

    def print_all_class(self):
        select_stmt = "select* from Classes"
        self.cursor.execute(select_stmt)
        results = self.cursor.fetchall()
        for x in results:
            print(x)

    def update_user(self,name,server,time_zone):
        update_stmt = "update Users set username = %s , servers = %s, time_zone = %s where username = %s;"
        data = (name,server,time_zone)
        self.cursor.execute(update_stmt, data)
        self.connection.commit()
        print("update %s successfully" % name)

    def update_class(self,classname,server):
        update_stmt = "update Classes set class_name = %s, servers = %s where class_name =%s"
        data = (classname,server)
        self.cursor.execute(update_stmt, data)
        self.connection.commit()
        print("update %s successfully" % classname)

    def disconnect(self):
        # make sure to disconnect database after finish everything
        self.cursor.close()
        self.connection.close()