import os
import socket
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5005
SIZE = 1024
FORMAT = "utf-8"

def get_address():
    while True:
        IP = input("Enter IP address: ")
        bytes = IP.split(".")
        if len(bytes) != 4:
            print("Invalid IP address")
            continue
        for i in bytes:
            if not i.isdigit():
                print("Invalid IP address")
                continue
            if int(i) > 255 or int(i) < 0:
                print("Invalid IP address")
                continue
        break
    while True:
        PORT = input("Enter port: ")
        if not PORT.isdigit():
            print("Invalid port")
            continue
        if int(PORT) < 5000 or int(PORT) > 5050:
            print("Invalid port")
            continue
        PORT = int(PORT)
        break
    return (IP, PORT)
        


def ls(client, path):
    client.send(f"ls {path}".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(msg)

def cd(client, newCurrentPath, currentPath):
    if newCurrentPath == "..":
        if currentPath == "root":
            print("You are already in root")
            return currentPath
        else:
            currentPath = currentPath[:currentPath.rfind("/")]
            return currentPath
    else:
        client.send(f"cd {newCurrentPath} {currentPath}".encode(FORMAT))
        if client.recv(SIZE).decode(FORMAT) == "ok":
            return f"{currentPath}/{newCurrentPath}"
        else:
            print("Directory not found")
            return currentPath

def mkdir(client, newDir, path):
    client.send(f"mkdir {newDir} {path}".encode(FORMAT))
    if client.recv(SIZE).decode(FORMAT) == "ok":
        print("Directory created")
    else:
        print("Directory already exists")

def send_file(client, name, path):
    
    client.send(f"upload {name} {path}".encode(FORMAT))
    
    file = open(name , "rb")

    if client.recv(SIZE).decode(FORMAT) == "not ok":
        print("File name already exists")
        file.close()
        return
    
    while True:
        read = file.read(SIZE)
        if not read:
            break
        client.send(read)

    file.close

    client.send(b"End of file")
    print("File sent")

def receive_file(client, name, path):
    client.send(f"download {name} {path}".encode(FORMAT))

    if client.recv(SIZE).decode(FORMAT) == "not ok":
        print("File does not exist")
        return
    
    file = open(name, "wb")
    while True :
        data = client.recv(SIZE)
        if data[-11:] == b"End of file":
            break
        else:
            file.write(data)
    file.close()
    print("File downloaded")


def client_program(ADDR):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    currentDir = "root"

    while True:
        msg = input("-> ")
        if msg == "exit":
            client.send(msg.encode(FORMAT))
            break

        elif msg == "ls":
            ls(client, currentDir)

        elif msg[:3] == "cd ":
            currentDir = cd(client, msg[3:], currentDir)
            print(currentDir)

        elif msg[0:6] == "mkdir ":
            print("mkdir")
            mkdir(client, msg[6:], currentDir)

        elif msg[0:7] == "upload ":
            print("upload")
            files = os.listdir()
            if msg[7:] in files:
                send_file(client, msg[7:], currentDir)
            else:
                print("File does not exist")
        elif msg[0:9] == "download ":
            print("download")
            receive_file(client, msg[9:], currentDir)





if __name__ == '__main__':
    ADDR = get_address()
    client_program(ADDR)
