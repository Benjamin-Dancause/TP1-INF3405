import os
import socket
import sys
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5005
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"




def send_file(conn, file):
    pass


def ls(conn, path):
    files = os.listdir(path)
    directories = ""
    for name in files:
        directories += f"\n{name}"
    if directories == "":
        directories = " This directory is empty"
    conn.send(directories[1:].encode(FORMAT))

def cd(conn, newPath, currentPath):
    files = os.listdir(currentPath)
    if newPath in files:
        conn.send("ok".encode(FORMAT))
    else:
        conn.send("not ok".encode(FORMAT))


def mkdir(conn, newDir, path):
    files = os.listdir(path)
    if newDir not in files:
        os.mkdir(f"{path}/{newDir}")
        conn.send("ok".encode(FORMAT))
    else:
        conn.send("not ok".encode(FORMAT))


def receive_file(conn, name, path):
    print(f"Receiving :{name}")
    new_path = path + "/" + name
    files = os.listdir(path)
    if name in files:
        conn.send("not ok".encode(FORMAT))
        return
    conn.send("ok".encode(FORMAT))
    file = open(new_path, "wb") #openeing a non existing file will create it
    while True :
        write = conn.recv(SIZE)
        file.write(write)
        if sys.getsizeof(write) < 1024: #if the size of the data is less than 1024 bytes it means that it is the last data
            break
    file.close()
    conn.send("ok".encode(FORMAT))

def send_file(conn, name, path):
    print(f"Checking : {name}")
    files = os.listdir(path)
    if name in files:
        conn.send("ok".encode(FORMAT))
    else:
        conn.send("not ok".encode(FORMAT))
        return
    file = open(path + "/" + name, "rb")
    while True:
        read = file.read(SIZE)
        if not read:
            break
        conn.send(read)
    file.close
    print("File sent")
    conn.send("ok".encode(FORMAT))


def handle_client(conn, addr, client_id):
    print(f"New connection: {addr} client id: {client_id}")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f"Message from {addr}: {msg}")
        if msg == "exit":
            print(f"Connection from client {client_id} closed ({addr})")
            connected = False
        elif msg[:3] == "ls ":
            print(f"ls {addr}")
            ls(conn, msg[3:])
        elif msg[0:3] == "cd ":
            print(f"cd {addr}")
            args = msg.split(" ")
            cd(conn, args[1], args[2])
        elif msg[0:6] == "mkdir ":
            print(f"mkdir {addr}")
            print(msg)
            args = msg.split(" ")
            mkdir(conn, args[1], args[2])
        elif msg[0:7] == "upload ":
            print(f"upload {addr}")
            args = msg.split(" ")
            receive_file(conn, args[1], args[2])
        elif msg[0:9] == "download ":
            print(f"download{addr}")
            args = msg.split(" ")
            send_file(conn, args[1], args[2])
        else:
            print(f"Command not found from {addr}")
            conn.send("Command not found".encode(FORMAT))

    conn.close()


def server_program():
    client_id = 0
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen(10)
    print(f"Server started on {IP}:{PORT}")
    print("Waiting for connection...")

    while True:
        conn, addr = server.accept()
        client_id += 1
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        thread.start()


if __name__ == '__main__':
    server_program()
