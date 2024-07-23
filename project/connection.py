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
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) NOT NULL UNIQUE,
                        first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100),
                        phone VARCHAR(15),
                        gender ENUM('M', 'F'),
                        birth_date DATE,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        delete_date DATE DEFAULT NULL,
                        password VARCHAR(255) NOT NULL,
                        CHECK (CHAR_LENGTH(username) >= 5)
                        ) ENGINE=InnoDB""")
    
    tables['files'] = (
                    """CREATE TABLE IF NOT EXISTS files (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        filename BLOB NOT NULL,
                        delete_date DATE DEFAULT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                        ) ENGINE=InnoDB""")
    tables['temp_codes'] = (
                        """CREATE TABLE IF NOT EXISTS temp_codes (
                        user_id INT NOT NULL,
                        code INT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                        ) ENGINE=InnoDB""")
    tables['posts'] = (
                        """CREATE TABLE IF NOT EXISTS posts (
                        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        description VARCHAR(250) NOT NULL,
                        delete_date DATE DEFAULT NULL
                        ) ENGINE=InnoDB""")
    tables['the_tags'] = (
                        """CREATE TABLE IF NOT EXISTS the_tags (
                        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL UNIQUE
                        ) ENGINE=InnoDB""")
    tables['post_tag'] = (
                        """CREATE TABLE IF NOT EXISTS post_tag (
                        post_id INT, 
                        tag_id INT, 
                        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE, 
                        FOREIGN KEY (tag_id) REFERENCES the_tags(id) ON DELETE CASCADE
                        ) ENGINE=InnoDB""")


    for table_name in tables:
        cursor.execute(tables[table_name])
        connection.commit()

    cursor.close()
    return connection