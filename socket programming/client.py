import socket
import pickle

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 1024

def register_user(username, password):
    request = {'action': 'register', 'username': username, 'password': password}
    response = send_and_receive_response(request)
    return response

def authenticate_user(username, password):
    request = {'action': 'login', 'username': username, 'password': password}
    response = send_and_receive_response(request)
    return response

def send_and_receive_response(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(pickle.dumps(request))
        data = s.recv(BUFFER_SIZE)
        response = pickle.loads(data)
        return response

def main():
    while True:
        print("Welcome to the authentication system!")
        print("Please select an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            response = register_user(username, password)
            print(response['message'])
        elif choice == '2':
            username = input("Enter your username: ")
            password = password = input("Enter your password: ")
            response = authenticate_user(username, password)
            print(response['message'])
        elif choice == '3':
            print("Exiting the authentication system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()