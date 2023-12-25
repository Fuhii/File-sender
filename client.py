import os
import sys
import socket

def protocol_header(filename_size, json_length, data_length):
    return filename_size.to_bytes(1, "big")+json_length.to_bytes(3, "big")+data_length.to_bytes(4, "big")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = input("Types int the server's address to contact to: ")
server_port = 9001

print("connecting {} port {}".format(server_address, server_port))

try:
    sock.connect((server_address, server_port))
except socket.error as err:
    print(str(err))
    sys.exit(1)

try:
    filepath = input("Typr ina file to upload")

    with open(filepath, "rb") as f:
        f.seek(0, os.SEEK_END)
        filesize = f.tell()
        f.seek(0,0)
    
        if filesize > pow(2, 31):
            raise Exception("Filesize must be below 2GB")
    
        filename = os.path.basename(filepath)
        filename_bits = filename.encode("UTF-8")

        header = protocol_header(len(filename_bits), 0, filesize)

        sock.send(header)
        sock.send(filename_bits)

        data = f.read(4096)
        while data:
            print("Sending...")
            sock.send(data)
            data = f.read(4096)

finally:
    print('closing socket')
    sock.close()
