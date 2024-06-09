import mysql.connector

db_name = "employees"
db_user = "root"
# db_password = "ali@1234"
db_host = "127.0.0.1"

def connect():
    connection = mysql.connector.connect(host=db_host, user=db_user,
                                         database=db_name)  
    cursor = connection.cursor()
    
    # create tables
    tables = {}
    tables['users'] = (
                    """CREATE TABLE IF NOT EXISTS users (
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) NOT NULL UNIQUE,
                        first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100) NOT NULL,
                        phone VARCHAR(15),
                        gender ENUM('M', 'F') NOT NULL,
                        birth_date DATE NOT NULL,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        CHECK (CHAR_LENGTH(username) >= 5)
                        ) ENGINE=InnoDB""")
    
    tables['files'] = (
                    """CREATE TABLE IF NOT EXISTS files (
                        file_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        filename BLOB NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                        ) ENGINE=InnoDB""")

    for table_name in tables:
        cursor.execute(tables[table_name])
        connection.commit()

    cursor.close()
    

    return connection