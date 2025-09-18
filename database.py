# database.py
import sqlite3
import hashlib

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('marketing_content.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates the necessary tables if they don't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Generated content table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            generated_text TEXT NOT NULL,
            image_prompt TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Adds a new user to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # This error occurs if username is not unique
        return False
    finally:
        conn.close()

def check_user(username, password):
    """Checks if a user exists and the password is correct."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user['password_hash'] == hash_password(password):
        return user
    return None

def save_content(user_id, product_name, generated_text, image_prompt):
    """Saves generated content for a specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO generated_content (user_id, product_name, generated_text, image_prompt) VALUES (?, ?, ?, ?)",
        (user_id, product_name, generated_text, image_prompt)
    )
    conn.commit()
    conn.close()

def get_user_content(user_id):
    """Retrieves all saved content for a specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM generated_content WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    content_history = cursor.fetchall()
    conn.close()
    return content_history

# Initialize the database and tables when the module is first imported
create_tables()