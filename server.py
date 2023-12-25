import os
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "0.0.0.0"
server_port = 9001

dpath = "tmp"
if not os.path.exists(dpath):
    os.mkdir(dpath)

sock.bind((server_address, server_port))
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print("connection from {}".format(client_address))
        header = connection.recv(8)

        filename_size = int.from_bytes(header[:1], "big")
        json_length = int.from_bytes(header[1:3], "big")
        data_length = int.from_bytes(header[4:8], "big")
        stream_rate = 4096

        print("Recieved data from client: filename_size {}, json_length {}, data_length {}".format(filename_size, json_length, data_length))

        filename = connection.recv(filename_size).decode("UTF-8")
        print("filename is {}".format(filename))

        if json_length != 0:
            raise("Json data is not supported")
        
        if data_length == 0:
            raise("No data to read from client")
        
        with open(os.path.join(dpath, filename), "wb") as f:
            while data_length > 0:
                data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                f.write(data)
                print("received {} bytes".format(len(data)))
                data_length -= len(data)
                print(data_length)

                print("Finished downloading the file from client")

    except Exception as err:
        print(str(err))

    finally:
        print("closed connection")
        connection.close()


