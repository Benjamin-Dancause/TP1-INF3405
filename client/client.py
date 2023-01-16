import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5030
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"



def ls(client, path):
    client.send(f"ls {path}".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(msg)

def cd(client, newCurrentPath, currentPath):
    if newCurrentPath == "..":
        if currentPath == "root":
            print("You are already in root")
        else:
            currentPath = currentPath[:currentPath.rfind("/")]
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

def send_file(client, name, path): #don't know if file should be a path or just the name for now it's just the name
    file_size = os.path.getsize(name)
    
    client.send(f"upload {name} {path} {file_size}".encode(FORMAT))
    
    #open file
    file = open(name , "rb")

    #send file name
    if client.recv(SIZE).decode(FORMAT) == "not ok":
        print("File name already exists")
        return
    
    line = file.readline(SIZE)
    while line:
        client.send(line)
        line = file.readline(SIZE)
    
    file.close

def client_program():
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

        elif msg[0:7] == "upload ":#need to verify if the file exists
            print("upload")
            send_file(client, msg[7:], currentDir)
        elif msg[0:9] == "download ":
            print("download")
            #send download command to the server with as a third argument the current directory
            #send the file name to the server
            #receive an ok message from the server or an error message
            #receive the file from the server
            #save the file in the client





if __name__ == '__main__':
    client_program()