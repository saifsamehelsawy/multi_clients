import tkinter as tk
import socket
import threading


def log_message(message):
    log_text.after(0, lambda: log_text.insert(tk.END, message + '\n'))


def handle_client(client_socket, address):
    log_message(f'Connection from {address} established.')

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode().strip().lower()
            log_message(f'Received: {message}')

            if message == "hi":
                response = "Hi, how can I help you?"
            elif message == "hello":
                response = "Hello, it's good to see you."
            else:
                response = "I don't know how to respond to that."

            client_socket.send(response.encode())

    except ConnectionResetError:
        log_message(f'Client {address} disconnected unexpectedly.')

    finally:
        client_socket.close()
        log_message(f'Connection with {address} closed.')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 23451))
    server_socket.listen()
    log_message('Listening on localhost:23451')

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()


def start_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()


# GUI 
root = tk.Tk()
root.title("Socket Server")

log_text = tk.Text(root, height=20, width=50)
log_text.pack()

start_button = tk.Button(root, text='Start Server', command=start_server_thread)
start_button.pack()

root.mainloop()