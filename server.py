import socket
from threading import Thread
import subprocess
import os

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8000

binary_file_type = ['png', 'jpeg', 'jpg']
text_file_type = ['html', 'css', 'js']
executable_file_type = ['py']

def process_request(socket_client, client_addr):
	print("Conexão bem sucedida")

	# receber dados do client
	received_data = socket_client.recv(1024)
	received_data = received_data.decode()

	# parsing do cabeçalho 
	headers = received_data.split('\r\n')
	header_get = headers[0]

	# obtendo o arquivo solicitado
	requested_file = header_get.split(" ")[1][1:]
	if not requested_file:
		requested_file = "index.html"
	print(f'Arquivo solicitado: {requested_file}')

	# obtendo extensão 
	ext = requested_file.split('.')[-1]

	binary_file = False
	executable_file = False

	if ext in executable_file_type:
		executable_file = True

	if ext in binary_file_type:
		binary_file = True

	# abrir o arquivo
	if os.path.exists(requested_file):
		try:
			if executable_file:
				process = subprocess.run(['python', requested_file], stdout=subprocess.PIPE, text=True)
				stdout = process.stdout
				headers = f'HTTP/1.1 200 OK\r\n\r\n'
				answer = headers + stdout
				socket_client.sendall(answer.encode('utf-8'))
				return True	
			elif binary_file:
				file = open(requested_file, 'rb')
			else:
				file = open(requested_file, 'r', encoding='utf-8')
			file_content = file.read()
		except:
			print(f"Arquivo não existe {requested_file}")
			socket_client.sendall(b'HTTP/1.1 404 File not found\r\n\r\nFile not found')
			socket_client.close()
			return False
	else:
		print(f"Arquivo não existe {requested_file}")
		requested_file = "404.html"
		if binary_file:
			file = open(requested_file, 'rb')
		else:
			file = open(requested_file, 'r', encoding='utf-8')
		file_content = file.read()

	# resposta ao browser
	response_header = f'HTTP/1.1 200 OK\r\n\r\n'

	if binary_file:
		final_response = bytes(response_header, 'utf-8') + file_content
		socket_client.sendall(final_response)
	else:
		final_response = response_header + file_content
		socket_client.sendall(final_response.encode('utf-8'))

	# encerar conexão
	socket_client.close()

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# solicitação para porta estipulada

socket_server.bind((SERVER_ADDRESS, SERVER_PORT))
socket_server.listen(10)

while True:

	# conexão client

	print(f'Servidor em {SERVER_ADDRESS}:{SERVER_PORT} aguardando conexões...\n')

	socket_client, client_addr = socket_server.accept()

	# despachando a requisição para a thread processa-la

	Thread(target=process_request, args=(socket_client, client_addr)).start()

socket_server.close()