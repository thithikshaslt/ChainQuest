import socket
import pickle
import hashlib
import os
import sqlite3

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 1024

# Create the SQLite database and table if they don't exist
conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    salt TEXT
                )""")
conn.commit()

def register_user(username, password):
    try:
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            return {'status': 'error', 'message': 'Username already exists.'}

        # Generate a random salt
        salt = os.urandom(16).hex()

        # Hash the password with the salt
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, hashed_password.hex(), salt))
        conn.commit()
        return {'status': 'success', 'message': 'Registration successful.'}
    except sqlite3.Error as e:
        return {'status': 'error', 'message': str(e)}

def authenticate_user(username, password):
    try:
        # Fetch the user's hashed password and salt from the database
        cursor.execute("SELECT password, salt FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result is None:
            return {'status': 'error', 'message': 'Invalid username or password.'}

        stored_password, stored_salt = result
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), stored_salt.encode(), 100000)

        # Compare the hashed password with the stored hashed password
        if hashed_password.hex() == stored_password:
            return {'status': 'success', 'message': 'Login successful.'}
        else:
            return {'status': 'error', 'message': 'Invalid username or password.'}
    except sqlite3.Error as e:
        return {'status': 'error', 'message': str(e)}

def handle_client(client_socket):
    try:
        data = client_socket.recv(BUFFER_SIZE)
        request = pickle.loads(data)
        action = request['action']
        username = request['username']
        password = request['password']

        if action == 'register':
            response = register_user(username, password)
        elif action == 'login':
            response = authenticate_user(username, password)
        else:
            response = {'status': 'error', 'message': "Unknown action."}

        client_socket.send(pickle.dumps(response))
    except Exception as e:
        print(f"Error handling client: {e}")
        response = {'status': 'error', 'message': str(e)}
        client_socket.send(pickle.dumps(response))
    finally:
        client_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                handle_client(conn)

if __name__ == "__main__":
    main()