import argparse
import os
import socket

__author__ = 'Gilad Barak'
__name__ = "main"

"""
This client is used as a demo for a POST client for server.py - based on exercises 4.10-4.11 from Gvahim book.
"""

SEPREQ = "\r\n"
NOTFOUND = "File was not found!"
IP = "127.0.0.1"
PORT = 80
POSTADDRESS = "/upload"
KB = 1024


def img_file_content(file_path):
    """
    :param file_path: a str type object representing path to file including file name
    :return: file binary content if file exists else returns False
    """
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        content = f.read()
        f.close()
        return content
    else:
        return False


def generate_post_request(content, file_path):
    """
    :param content: binary content of file passed in POST request
    :param file_path: a str type object representing path to file including file name
    :return: POST request str
    """
    file_name = get_file_name(file_path)
    request = "POST " + POSTADDRESS + " HTTP/1.1" + SEPREQ
    request += "file-name: " + file_name + SEPREQ
    request += "content-length: " + str(len(content)) + SEPREQ
    request += SEPREQ
    request += content
    return request


def get_file_name(file_path):
    """
    :param file_path: a str type object representing path to file including file name
    :return: file name given path is pointing at
    """
    sep_index = file_path.rfind(os.sep)
    file_name = file_path[sep_index + 1:]
    return file_name


def main():
    """
    manages the sending and receiving of the POST client using parse args.
    Used as a demo client for server.py based on 4.10-4.11 Gvahim book
    """
    parser = argparse.ArgumentParser(description="Sends a POST request to server with given content.")
    parser.add_argument("file", type=str, help="Enter path to img file including img name")
    args = parser.parse_args()
    content = img_file_content(args.file)
    if content is not False:
        client_socket = socket.socket()
        client_socket.connect((IP, PORT))
        request = generate_post_request(content, args.file)
        client_socket.send(request)

        data = client_socket.recv(KB)
        print(data)

        client_socket.close()
    else:
        print(NOTFOUND)


if __name__ == 'main':
    main()
