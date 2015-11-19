__author__ = "Gilad Barak"
__name__ = "main"

import socket
import os

"""
A GET HTTP protocol server, based on excersises from Gvahim book Chapter 4.
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
ROOTDIR = "F:" + os.sep + "wwwroot"
SPACE = " "
OK = "OK"
OKCODE = "200"
NOTFOUND = "NotFound"
NOTFOUNDCODE = "404"

def parse_request(client_data):
	"""
	@param data from client's request as a str
	Parses client's http request into - method, url, protocol and headers (list of headers)
	@return list with http request elements + verification if valid HTTP GET request (boolean)
	[Method, URL, Protocol, Headers(list), is_valid]
	"""	
	elements = client_data.split(' ', MAXSPLIT)
	headers = elements[PROTOCOLCELL][elements[PROTOCOLCELL].index(HEADB)+1:]
	elements.append(headers)
	elements[PROTOCOLCELL] = elements[PROTOCOLCELL][:elements[PROTOCOLCELL].index(HEADB)]
	elements[HEADERCELL] = elements[HEADERCELL].split(SEPREQ)
	if not elements[METHODCELL] == GET:
		elements.append(False)
	elif not elements[URLCELL][0] == FSLASH:
		elements.append(False)
	elif not elements[PROTOCOLCELL] == PROTOCOL:
		elements.append(False)
	elif not elements[HEADERCELL][len(elements[HEADERCELL])-1] == EMPTY and not elements[HEADERCELL][len(elements[HEADERCELL])-2] == EMPTY:
		elements.append(False)
	else:
		elements.append(True)
	return elements


def get_file_name(request_elements):
	"""
	@param list of HTTP request elements - [Method, URL, Protocol, Headers(list), is_valid]
	@Return requested file name as str
	"""
	fslash_index = request_elements[URLCELL].index("/")
	file_name = request_elements[URLCELL][fslash_index + 1:]
	return file_name


def send_file(request_elements, client_socket):
	"""
	@param list of HTTP request elements - [Method, URL, Protocol, Headers(list), is_valid]
	@param client_socket - a socket._socketobject that represent the client side
	Function sends requested file to client
	@return true or false
	"""
	file_path = request_elements[URLCELL]
	file_path = file_path.replace(FSLASH, os.sep)
	file_path = ROOTDIR + file_path
	if os.path.isfile(file_path):
		f = open(file_path, 'rb')
		content = f.read()
		f.close()
		full_response = headers(file_path) + content
		client_socket.send(full_response)
		return True
	else:
		return False


def headers(file_path):
	"""
	@file path - full path including file name
	@return headers for HTTP protocol response
	"""
	if os.path.isfile(file_path):
		response_code = OKCODE
		response_phrase = OK
	else:
		response_code = NOTFOUNDCODE
		response_phrase = NOTFOUND

	header = PROTOCOL + SPACE + response_code + SPACE + response_phrase + SEPREQ
	header += "Content-Length: " + str(os.path.getsize(file_path)) + SEPREQ
	header += SEPREQ

	return header

def main():
	"""
	Connects to client and sends html.index file
	Sulotion for Ex 4.4, Chapter 4
	"""
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((IP, PORT))
	server_socket.listen(1)

	client_socket, client_address = server_socket.accept()
	client_data = client_socket.recv(KB)
	while True:
		client_data = parse_request(client_data)
		if not client_data[VALIDCELL]:
			client_socket.close()
		else:
			file_name = get_file_name(client_data)
			is_sent = send_file(client_data, client_socket)
			if not is_sent:
				print client_address[0] + ": Error occurded with " + file_name

		client_socket.close()

		client_socket, client_address = server_socket.accept()
		client_data = client_socket.recv(KB)

	server_socket.close()

if __name__ == "main":
	main()
