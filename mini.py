import mysql.connector

def connect_to_database(user, password, host="localhost", database="library_db"):
    try:
        return mysql.connector.connect(user=user, password=password, host=host, database=database)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()

    # Create tables
    tables = {
        "books": """
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author_id INT,
                genre_id INT,
                isbn VARCHAR(13) NOT NULL,
                publication_date DATE,
                availability BOOLEAN DEFAULT 1,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (genre_id) REFERENCES genres(id)
            )
        """,
        "authors": """
            CREATE TABLE IF NOT EXISTS authors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                biography TEXT
            )
        """,
        "genres": """
            CREATE TABLE IF NOT EXISTS genres (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(50)
            )
        """,
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                library_id VARCHAR(10) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL 
            )
        """,
        "borrowed_books": """
            CREATE TABLE IF NOT EXISTS borrowed_books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                book_id INT,
                borrow_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        """
    }

    for table_name, create_table_query in tables.items():
        try:
            print(f"Creating table {table_name} if it doesn't exist...")
            cursor.execute(create_table_query)
        except mysql.connector.Error as err:
            print(f"Error creating table {table_name}: {err}")

    connection.commit()  
    cursor.close()