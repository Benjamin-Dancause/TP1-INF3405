import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5031
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"



def receive_file(conn):
    filename = conn.recv(SIZE).decode(FORMAT)
    print(f"Receiving :{filename}")
    file = open(filename, "w") #openeing a non existing file will create it
    data = conn.recv(SIZE).decode(FORMAT)
    file.write(data)
    conn.send("File received".encode(FORMAT))
    file.close()


def ls(conn, path):
    files = os.listdir(path)
    directories = ""
    for name in files:
        directories += f"\n{name}"
    print(directories)
    conn.send(directories[1:].encode(FORMAT))



def handle_client(conn, addr, client_id):
    print(f"New connection: {addr} client id: {client_id}")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == "exit":
            print(f"Connection from client {client_id} closed ({addr})")
            connected = False
        elif msg[:3] == "ls ":
            print(f"ls {addr}")
            ls(conn, msg[3:])
        elif msg[0:2] == "cd ":
            print("cd")
        elif msg[0:5] == "mkdir ":
            print("mkdir")
        elif msg[0:6] == "upload ":
            print("upload")
        elif msg[0:8] == "download ":
            print("download")
        else:
            conn.send("Command not found".encode(FORMAT))
    conn.close()



def server_program():
    client_id = 0
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen(5)
    print("Server started")
    print("Waiting for connection...")

    while True:
        conn, addr = server.accept()
        client_id += 1
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        thread.start()


if __name__ == '__main__':
    server_program()
