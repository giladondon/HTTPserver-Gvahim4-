import argparse
import os
import socket

__author__ = 'Gilad Barak'
__name__ = "main"

SEPREQ = "\r\n"
NOTFOUND = "File was not found!"
IP = "127.0.0.1"
PORT = 80
POSTADDRESS = "/upload"


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
    request += "content-length: " + str(os.path.getsize(file_path)) + SEPREQ
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
    parser = argparse.ArgumentParser(description="Sends a POST request to server with given content.")
    parser.add_argument("file", type=str, help="Enter path to img file including img name")
    args = parser.parse_args()
    content = img_file_content(args.file)
    if content is not False:
        client_socket = socket.socket()
        client_socket.connect((IP, PORT))
        request = generate_post_request(content, args.file)
        client_socket.send(request)

        client_socket.close()
    else:
        print(NOTFOUND)


if __name__ == 'main':
    main()
