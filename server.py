import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"



def receive_file(conn, filename):
    file = open(filename, "w") #openeing a non existing file will create it
    data = conn.recv(SIZE).decode(FORMAT)
    file.write(data)
    conn.send("File received".encode(FORMAT))
    file.close()




def server_program():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen(5)
    print("Server started")
    print("Waiting for connection...")

    while True:
        conn, addr = server.accept()
        print("Connection from: " + str(addr))

        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"Receiving :{filename}")
        file = open(filename, "w")
        conn.send("File name received".encode(FORMAT))

        data = conn.recv(SIZE).decode(FORMAT)
        file.write(data)
        conn.send("File received".encode(FORMAT))

        file.close()

        conn.close()



if __name__ == '__main__':
    server_program()
