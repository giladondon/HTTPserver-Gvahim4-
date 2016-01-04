import socket
import os
import types

__author__ = "Gilad Barak"
__name__ = "main"

"""
A GET HTTP protocol server, based on exercises from Gvahim book Chapter 4.
"""

PORT = 80
IP = '0.0.0.0'
HEADB = "\r"
VALIDMETHODS = ["GET", "POST"]
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
VARCELL = 5
ROOTDIR = "/Users/Giladondon/Cyber/compNet/wwwroot"
ROOTFILE = "index.html"
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
NUMBERTYPE = (types.IntType, types.LongType, types.FloatType, types.ComplexType)
CALCDEFULT = 5
POSTADDRESS = "/upload"
CONTENTCELL = 5
UPLOADPOSTDIR = "/Users/Giladondon/Cyber/compNet/wwwroot/upload"


def parse_get(elements):
    """
    :param elements: a GET request separated by whitespaces into a list.
    :return: list with http request elements + verification if valid HTTP GET request (boolean)
    [Method, URL, Protocol, Headers(list), is_valid]
    """
    request_headers = elements[PROTOCOLCELL][elements[PROTOCOLCELL].index(PROTOCOL) + len(PROTOCOL) + 1:]
    elements.append(request_headers)
    elements[PROTOCOLCELL] = elements[PROTOCOLCELL][:elements[PROTOCOLCELL].index(PROTOCOL) + len(PROTOCOL)]
    elements[HEADERCELL] = elements[HEADERCELL].split(SEPREQ)
    calculate = False
    if "/calculate-next" in elements[URLCELL] or "/calculate-area" in elements[URLCELL] or "/image" in elements[URLCELL]:
        calculate = True
        if "?" not in elements[URLCELL] or "=" not in elements[URLCELL]:
            print("a")
            variables_dict = {}
        else:
            print("b")
            variables = elements[URLCELL].split('?')[1]
            print(variables)
            variables = variables.split('&')
            print(variables)
            variables_dict = {}
            for cell in range(0, len(variables)):
                variables_dict[variables[cell].split('=')[0]] = variables[cell].split('=')[1]
            print(variables_dict)
    if elements[METHODCELL] not in VALIDMETHODS:
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
    if calculate:
        elements.append(variables_dict)

    return elements


def parse_post(elements):
    """
    :param elements: a POST request separated by whitespaces into a list.
    :return: list with http request elements + verification if valid HTTP GET request (boolean)
    [Method, Address, Protocol, Headers, is_valid, Content]
    """
    request_headers = elements[PROTOCOLCELL][elements[PROTOCOLCELL].index(PROTOCOL) + len(PROTOCOL) + 1:]
    elements.append(request_headers)
    elements[PROTOCOLCELL] = elements[PROTOCOLCELL][:elements[PROTOCOLCELL].index(PROTOCOL) + len(PROTOCOL)]
    elements[HEADERCELL] = elements[HEADERCELL].split(SEPREQ)
    elements[HEADERCELL][0] = elements[HEADERCELL][0][1:]
    if elements[METHODCELL] not in VALIDMETHODS:
        elements.append(False)
    elif not elements[URLCELL][0] == FSLASH:
        elements.append(False)
    elif not elements[PROTOCOLCELL] == PROTOCOL:
        elements.append(False)
    elif not elements[URLCELL] == POSTADDRESS:
        elements.append(False)
    else:
        elements.append(True)

    elements = generate_content(elements)

    print(elements)

    return elements


def generate_content(elements):
    start = elements[HEADERCELL].index('')+1
    content = ""
    for i in range(start, len(elements[HEADERCELL])):
        if content == "":
            content += elements[HEADERCELL][i]
        else:
            content += SEPREQ + elements[HEADERCELL][i]
    for i in range(start, len(elements[HEADERCELL])):
        elements[HEADERCELL].pop(start)
    elements.append(content)
    return elements

def parse_request(client_data):
    """
    @param client_data from client's request as a str
    Parses client's http request into - method, url, protocol and headers (list of headers)
    @return list with http request elements + verification if valid HTTP GET request (boolean)
    [Method, URL, Protocol, Headers(list), is_valid]
    [Method, Address, Protocol, Headers, Content, is_valid, variables(optional)]
    """
    elements = client_data.split(' ', MAXSPLIT)
    if elements[METHODCELL] == "GET":
        elements = parse_get(elements)
    elif elements[METHODCELL] == "POST":
        elements = parse_post(elements)
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
    @return requested file name as str
    """
    fslash_index = request_elements[URLCELL].rfind("/")
    file_name = request_elements[URLCELL][fslash_index + 1:]
    return file_name


def send_file(request_elements, client_socket):
    """
    @param request_elements list of HTTP request elements -
    [Method, URL, Protocol, Headers(list), is_valid, (optional) dictionary of variables]
    @param client_socket - a socket._socketobject that represent the client side
    Function sends requested file or function result to client
    @return True or False if sent
    """
    if not request_elements[VALIDCELL]:
        full_response = headers(UNKNOWN)[0] + "Internal server error"
        client_socket.send(full_response)
        return False

    elif len(request_elements) == VARCELL + 1:
        if "/calculate-next" in request_elements[URLCELL]:
            return calculate_next(request_elements[VARCELL], client_socket)
        elif "/calculate-area" in request_elements[URLCELL]:
            return calculate_area(request_elements[VARCELL], client_socket)
        elif "/image" in request_elements[URLCELL]:
            print(request_elements[VARCELL])
            file_path = UPLOADPOSTDIR + os.sep + request_elements[VARCELL]["image-name"]
            print(file_path)
    else:
        file_path = generate_file_path(request_elements)

    if os.path.isfile(file_path):
        return file_in_manage(client_socket, file_path)
    else:
        return file_not_in_manage(client_socket, file_path)


def file_not_in_manage(client_socket, file_path):
    """
    @param client_socket - a socket._socketobject that represent the client side.
    @param file_path - string of path to file including file name
    @returns True or False if data is sent to client properly
    """
    if headers(file_path)[1] == MOVEDCODE:
        f = open(find_file(file_path), 'rb')
        content = f.read()
        f.close()
        full_response = headers(file_path)[0] + str(content)
        client_socket.send(full_response)
        return False
    elif headers(file_path)[1] == NOTFOUNDCODE:
        full_response = headers(file_path)[0] + NOTFOUNDCONTENT
        client_socket.send(full_response)
        return True

    return False


def file_in_manage(client_socket, file_path):
    """
    @param client_socket - a socket._socketobject that represent the client side.
    @param file_path - string of path to file including file name
    @returns True or False if data is sent to client properly
    """
    f = open(file_path, 'rb')
    content = f.read()
    f.close()
    if headers(file_path)[1] == FORBIDDENCODE:
        full_response = headers(file_path)[0] + FORBIDDENCONTENT
        client_socket.send(full_response)
        return True
    else:
        full_response = headers(file_path)[0] + str(content)
        client_socket.send(full_response)
        return True

    return False


def generate_file_path(request_elements):
    """
    @param request_elements - list of HTTP request elements -
    [Method, URL, Protocol, Headers(list), is_valid, (optional) dictionary of variables]
    @returns string of path to file including file name
    """
    if not get_file_name(request_elements) == "":
        file_path = request_elements[URLCELL]
        file_path = file_path.replace(FSLASH, os.sep)
        file_path = ROOTDIR + file_path
    else:
        file_path = find_file(ROOTDIR + os.sep + ROOTFILE)
    return file_path


def calculate_next(variables_dict, client_socket):
    """
    @param variables_dict - dictionary with variables names as keys and values from user as values.
    @param client_socket - a socket._socketobject that represent the client side.
    @return True or False if response is sent to client with user values.
    """
    try:
        next_num = int(variables_dict["num"]) + 1
        full_response = headers(next_num)[0] + str(next_num)
    except:
        full_response = headers(CALCDEFULT)[0] + str(CALCDEFULT)
        return False
    finally:
        client_socket.send(full_response)
        return True


def calculate_area(variables_dict, client_socket):
    """
    @param variables_dict - dictionary with variables names as keys and values from user as values.
    @param client_socket - a socket._socketobject that represent the client side.
    @return True or False if full_response is sent with user values.
    """
    try:
        width = int(variables_dict["width"])
        height = int(variables_dict["height"])
        area = int((width * height) / 2)
        full_response = headers(area)[0] + str(area)
    except:
        area = 0
        full_response = headers(area)[0] + str(area)
        return False
    finally:
        client_socket.send(full_response)
        return True


def functions_header(value):
    """
    @param value that will be sent to client
    @return tuple (header, response code of header)
    """
    response_code = OKCODE
    response_phrase = OK
    header = PROTOCOL + SPACE + response_code + SPACE + response_phrase + SEPREQ
    header += "Content-Length: " + str(len(str(value))) + SEPREQ
    header += SEPREQ
    return header, response_code


def headers(file_path):
    """
    @file path - full path including file name
    if not valid request file_path = UNKNOWN
    if calculate function request file_path = given num
    @return headers for HTTP protocol response
    """
    if isinstance(file_path, NUMBERTYPE):
        return functions_header(file_path)
    elif file_path == UNKNOWN:
        response_code = INTERNALCODE
        header = PROTOCOL + SPACE + response_code + SPACE + INTERNAL + SEPREQ
        header += SEPREQ
    elif os.path.isfile(file_path):
        if FORBIDDENFOLDER in file_path:
            response_code = FORBIDDENCODE
            header = PROTOCOL + SPACE + response_code + SPACE + FORBIDDEN + SEPREQ
            header += SEPREQ
        else:
            response_code = OKCODE
            header = PROTOCOL + SPACE + response_code + SPACE + OK + SEPREQ
            header += "Content-Length: " + str(os.path.getsize(file_path)) + SEPREQ
            header += SEPREQ
    else:
        if not find_file(file_path):
            response_code = NOTFOUNDCODE
            header = PROTOCOL + SPACE + response_code + SPACE + NOTFOUND + SEPREQ
            header += SEPREQ
        else:
            response_code = MOVEDCODE
            header = PROTOCOL + SPACE + response_code + SPACE + MOVED + SEPREQ
            header += "Location: " + '/'.join(find_file(file_path).split(os.sep)[len(ROOTDIR.split(os.sep)):]) + SEPREQ
            header += SEPREQ

    return header, response_code


def save_from_post(headers_list, content, client_socket):
    """
    :param headers_list: a list of headers from POST request
    :param content: the content of the POST request
    :return: true if writing to file succeeded and false if didn't
    """
    for i in range(len(headers_list)):
        if "file-name: " in headers_list[i]:
            index_name = i
        if "content-length: " in headers_list[i]:
            index_content = i
    file_name = headers_list[index_name][len("file-name: "):]
    content_length = int(headers_list[index_content][len("content-length: "):])
    file = open(UPLOADPOSTDIR + os.sep + file_name, 'wb')
    file.write(content)
    more = client_socket.recv(content_length)
    file.write(more)

    return True


def main():
    """
    Connects to client and sends html.index file
    Solution for Ex 4.10, Chapter 4
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
                if client_data[METHODCELL] == "GET":
                    file_name = get_file_name(client_data)
                    is_sent = send_file(client_data, client_socket)
                    if not is_sent:
                        print(client_address[0] + "*** " + file_name)
                elif client_data[METHODCELL] == "POST":
                    acknoledge = save_from_post(client_data[HEADERCELL], client_data[CONTENTCELL], client_socket)
                    if not acknoledge:
                        print("***POST")
        client_socket.close()
        client_socket, client_address = server_socket.accept()
        client_data = client_socket.recv(KB)

    server_socket.close()


if __name__ == "main":
    main()
