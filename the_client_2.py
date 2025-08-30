import socket
import threading
import tkinter as tk

def start_client():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 23451))
    append_text("Connected to server as Client 2")
    threading.Thread(target=receive_messages, daemon=True).start()

def send_message():
    msg = entry.get()
    if msg:
        if msg.lower() == 'exit':
            close_client()
            return
        client.send(msg.encode())
        append_text(f"You (Client 2): {msg}")
        entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            response = client.recv(1024).decode()
            if not response:
                break
            append_text(f"Server: {response}")
        except:
            break

def close_client():
    try:
        client.close()
    except:
        pass
    append_text("Connection closed.")

def append_text(message):
    text_area.config(state='normal')
    text_area.insert(tk.END, message + "\n")
    text_area.config(state='disabled')
    text_area.see(tk.END)

# GUI
root = tk.Tk()
root.title("Socket Client 2 ")

text_area = tk.Text(root, height=15, width=50, state='disabled')
text_area.pack()

entry = tk.Entry(root, width=40)
entry.pack()

send_button = tk.Button(root, text="Send Message", command=send_message)
send_button.pack()

start_button = tk.Button(root, text="Start Client", command=start_client)
start_button.pack()

close_button = tk.Button(root, text="Close Client", command=close_client)
close_button.pack()

root.mainloop()