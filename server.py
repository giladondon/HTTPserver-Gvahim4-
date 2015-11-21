import socket
import os

__author__ = "Gilad Barak"
__name__ = "main"

"""
A GET HTTP protocol server, based on exercise from Gvahim book Chapter 4.
Currently solved up to exercise 4.4 (5).
"""

PORT = 80
IP = '0.0.0.0'
HEADB = "\r"
GET = "GET"
PROTOCOL = "HTTP/1.1"
SEPREQ = "\r\n"
FSLASH = "/"
KB = 1024
EMPTY = ''
MAXSPLIT = 2
METHODCELL = 0
URLCELL = 1
PROTOCOLCELL = 2
HEADERCELL = 3
VALIDCELL = 4
ROOTDIR = "/Users/Giladondon/Cyber/compNet/wwwroot"
SPACE = " "
OK = "OK"
OKCODE = "200"
NOTFOUND = "NotFound"
NOTFOUNDCODE = "404"
FORBIDDENFOLDER = "forbiddenFiles"
FORBIDDENCODE = "403"
FORBIDDEN = "Forbidden"
NOTFOUNDCONTENT = "File was not found!"
FORBIDDENCONTENT = "The file you are trying to reach is forbidden!"
MOVEDCODE = "302"
MOVED = "Found"
MOVEDCONTENT = "File was moved!"
UNKNOWN = "unknown"
INTERNAL = "Internal Server Error"
INTERNALCODE = "505"


def parse_request(client_data):
    """
    @param client_data from client's request as a str
    Parses client's http request into - method, url, protocol and headers (list of headers)
    @return list with http request elements + verification if valid HTTP GET request (boolean)
    [Method, URL, Protocol, Headers(list), is_valid]
    """
    elements = client_data.split(' ', MAXSPLIT)
    request_headers = elements[PROTOCOLCELL][elements[PROTOCOLCELL].index(PROTOCOL) + len(PROTOCOL) + 1:]
    elements.append(request_headers)
    elements[PROTOCOLCELL] = elements[PROTOCOLCELL][:elements[PROTOCOLCELL].index(PROTOCOL) + len(PROTOCOL)]
    elements[HEADERCELL] = elements[HEADERCELL].split(SEPREQ)
    if not elements[METHODCELL] == GET:
        elements.append(False)
    elif not elements[URLCELL][0] == FSLASH:
        elements.append(False)
    elif not elements[PROTOCOLCELL] == PROTOCOL:
        elements.append(False)
    elif not elements[HEADERCELL][len(elements[HEADERCELL]) - 1] == EMPTY:
        if not elements[HEADERCELL][len(elements[HEADERCELL]) - 2] == EMPTY:
            elements.append(False)
    else:
        elements.append(True)
    return elements


def find_file(file_path):
    """
    @param file_path - str including path to file and file name
    @return str of first match or False if non was found
    """
    name = file_path[file_path.rfind(os.sep)+1:]
    path = file_path[:file_path.rfind(os.sep)]
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return False


def get_file_name(request_elements):
    """
    @param request_elements list of HTTP request elements - [Method, URL, Protocol, Headers(list), is_valid]
    @Return requested file name as str
    """
    fslash_index = request_elements[URLCELL].index("/")
    file_name = request_elements[URLCELL][fslash_index + 1:]
    return file_name


def send_file(request_elements, client_socket):
    """
    @param request_elements list of HTTP request elements - [Method, URL, Protocol, Headers(list), is_valid]
    @param client_socket - a socket._socketobject that represent the client side
    Function sends requested file to client
    @return true or false
    """
    if not request_elements[VALIDCELL]:
        full_response = headers(UNKNOWN)[0] + "Internal server error"
        client_socket.send(full_response)
    elif not get_file_name(request_elements) == "":
        file_path = request_elements[URLCELL]
        file_path = file_path.replace(FSLASH, os.sep)
        file_path = ROOTDIR + file_path
    else:
        file_path = ROOTDIR + os.sep + "index.html"
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        content = f.read()
        f.close()
        if headers(file_path)[1] == FORBIDDENCODE:
            full_response = headers(file_path)[0] + FORBIDDENCONTENT
        else:
            full_response = headers(file_path)[0] + str(content)
        client_socket.send(full_response)
        return True
    else:
        if headers(file_path)[1] == MOVEDCODE:
            f = open(find_file(file_path), 'rb')
            content = f.read()
            f.close()
            full_response = headers(file_path)[0] + str(content)
            client_socket.send(full_response)
            return True
        elif headers(file_path)[1] == NOTFOUNDCODE:
            full_response = headers(file_path)[0] + NOTFOUNDCONTENT
            client_socket.send(full_response)
    return False


def headers(file_path):
    """
    @file path - full path including file name, if not valid request file_path = UNKNOWN
    @return headers for HTTP protocol response
    """
    if file_path == UNKNOWN:
        response_code = INTERNALCODE
        response_phrase = INTERNAL
        header = PROTOCOL + SPACE + response_code + SPACE + response_phrase + SEPREQ
        header += SEPREQ
    elif os.path.isfile(file_path):
        if FORBIDDENFOLDER in file_path:
            response_code = FORBIDDENCODE
            response_phrase = FORBIDDEN
            header = PROTOCOL + SPACE + response_code + SPACE + response_phrase + SEPREQ
            header += SEPREQ
        else:
            response_code = OKCODE
            response_phrase = OK
            header = PROTOCOL + SPACE + response_code + SPACE + response_phrase + SEPREQ
            header += "Content-Length: " + str(os.path.getsize(file_path)) + SEPREQ
            header += SEPREQ
    else:
        if not find_file(file_path):
            response_code = NOTFOUNDCODE
            response_phrase = NOTFOUND
            header = PROTOCOL + SPACE + response_code + SPACE + response_phrase + SEPREQ
            header += SEPREQ
        else:
            response_code = MOVEDCODE
            response_phrase = MOVED
            header = PROTOCOL + SPACE + response_code + SPACE + response_phrase + SEPREQ
            header += "Location: " + '/'.join(find_file(file_path).split(os.sep)[len(ROOTDIR.split(os.sep)):]) + SEPREQ
            header += SEPREQ

    return header, response_code


def main():
    """
    Connects to client and sends html.index file
    Solution for Ex 4.4, Chapter 4
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)

    client_socket, client_address = server_socket.accept()
    client_data = client_socket.recv(KB)
    while True:
        while client_data == "":
            client_socket.close()
            client_socket, client_address = server_socket.accept()
            client_data = client_socket.recv(KB)
        client_data = parse_request(client_data)
        if not client_data[VALIDCELL]:
            client_socket.close()
        else:
            file_name = get_file_name(client_data)
            is_sent = send_file(client_data, client_socket)
            if not is_sent:
                print(client_address[0] + "-" + file_name)
        client_socket.close()
        client_socket, client_address = server_socket.accept()
        client_data = client_socket.recv(KB)

    server_socket.close()


if __name__ == "main":
    main()
