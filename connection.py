import mysql.connector

db_name = "employees"
db_user = "root"
db_password = "ali@1234"
db_host = "127.0.0.1"

def connect():
    connection = mysql.connector.connect(
    host=db_host, user=db_user, password=db_password, database=db_name)  
    return connection