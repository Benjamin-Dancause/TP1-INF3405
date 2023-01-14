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

    # while True:
    #     msg = input("-> ")
    #     if msg == "exit":
    #         break
    #     elif msg == "ls":
    #         break
            

    send_file(client, "test.txt")

    client.close()



if __name__ == '__main__':
    client_program()