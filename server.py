from datetime import date
import os
import socket
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5005
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"



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
    new_path = path + "/" + name
    files = os.listdir(path)
    if name in files:
        conn.send("not ok".encode(FORMAT))
        return
    conn.send("ok".encode(FORMAT))
    file = open(new_path, "wb")
    while True :
        data = conn.recv(SIZE)
        if data[-11:] == b"End of file":
            break
        else:
            file.write(data)
    file.close()

def send_file(conn, name, path):
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
    conn.send(b"End of file")


def handle_client(conn, addr):
    print(f"New connection: {addr}")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == "exit":
            print(f"[{addr} - {date.today()}@{time.strftime('%H:%M:%S')} ] Connection closed")
            connected = False
        elif msg[:3] == "ls ":
            print(f"[{addr} - {date.today()}@{time.strftime('%H:%M:%S')} ] ls")
            ls(conn, msg[3:])
        elif msg[0:3] == "cd ":
            args = msg.split(" ")
            print(f"[{addr} - {date.today()}@{time.strftime('%H:%M:%S')} ] cd {args[1]}")
            cd(conn, args[1], args[2])
        elif msg[0:6] == "mkdir ":
            args = msg.split(" ")
            print(f"[{addr} - {date.today()}@{time.strftime('%H:%M:%S')} ] mkdir {args[1]}")
            mkdir(conn, args[1], args[2])
        elif msg[0:7] == "upload ":
            args = msg.split(" ")
            print(f"[{addr} - {date.today()}@{time.strftime('%H:%M:%S')} ] upload {args[1]}")
            receive_file(conn, args[1], args[2])
        elif msg[0:9] == "download ":
            args = msg.split(" ")
            print(f"[{addr} - {date.today()}@{time.strftime('%H:%M:%S')} ] download {args[1]}")
            send_file(conn, args[1], args[2])
        else:
            print(f"[{addr} - {date.today()}@{time.strftime('%H:%M:%S')} ] Unknown command")
            conn.send("Command not found".encode(FORMAT))

    conn.close()


def server_program():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen(10)
    print(f"Server started on {IP}:{PORT}")
    print("Waiting for connection...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    server_program()
