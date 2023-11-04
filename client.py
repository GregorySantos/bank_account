import socket

def send_request(command, *args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345))

    client_clock = 0 
    request = f"{client_clock} {command} {' '.join(args)}"

    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    print(response)

    client_socket.close()

# Example usage
if __name__ == "__main__":
    send_request("BALANCE", "123")
    send_request("BALANCE", "456")