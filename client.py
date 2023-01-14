import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def send_file(client, file):
    #open file
    file = open(file , "r")
    data = file.read()

    #send file name
    client.send("sdw".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(msg)

    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(msg)

    file.close



def client_program():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    current_dir = "root"

    while True:
        msg = input("-> ")
        if msg == "exit":
            client.send(msg.encode(FORMAT))
            break
        elif msg == "test":
            send_file(client, "test.txt")
        elif msg == "ls":
            msg += f" {current_dir}"
            client.send(msg.encode(FORMAT))
            data = client.recv(SIZE).decode(FORMAT)
            print(data)
        elif msg[0:2] == "cd ":
            if msg[3:] == "..":
                if current_dir == "root":
                    print("You are already in root")
                else:
                    current_dir = current_dir[:current_dir.rfind("/")]
            else:
                current_dir = msg[3:]
                client.send(msg.encode(FORMAT))
                data = client.recv(SIZE).decode(FORMAT)
                #verify if the directory exists
                #if not receive an error message from the server
                #else receive an ok message from the server and chande directory
        elif msg[0:5] == "mkdir ":
            print("mkdir")
            #send mkdir command to the server with as a third argument the current directory
            #create the directory in the server
            #receive an ok message from the server
        elif msg[0:6] == "upload ":
            print("upload")
            #send upload command to the server with as a third argument the current directory
            #send the file name to the server
            #receive an ok message from the server
            #send the file to the server
            #receive an ok message from the server
        elif msg[0:8] == "download ":
            print("download")
            #send download command to the server with as a third argument the current directory
            #send the file name to the server
            #receive an ok message from the server or an error message
            #receive the file from the server
            #save the file in the client

    



if __name__ == '__main__':
    client_program()