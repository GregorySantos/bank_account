import socket

class Client:
    def __init__(self):
        self.logical_clock = 0

    def send_request(self, command):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12345))

        try:
            self.logical_clock += 1
            client_socket.send(f"{self.logical_clock} {command}".encode())
            response = client_socket.recv(1024).decode()
            print(response)
        finally:
            client_socket.close()

def main():
    client = Client()

    while True:
        print("\nOpcoes:")
        print("1. Verificar Saldo")
        print("2. Saque")
        print("3. Deposito")
        print("4. Transferencia entre contas")
        print("5. Sair")
        choice = input("Digite a sua escolha (1-5): ")

        if choice == "1":
            account_number = input("Digite o numero da conta: ")
            command = f"BALANCE {account_number}"
            client.send_request(command)

        elif choice == "2":
            account_number = input("Digite o numero da conta: ")
            amount = input("Digite o valor a ser sacado: ")
            command = f"WITHDRAW {account_number} {amount}"
            client.send_request(command)

        elif choice == "3":
            account_number = input("Digite o numero da conta: ")
            amount = input("Digite o valor a ser depositado: ")
            command = f"DEPOSIT {account_number} {amount}"
            client.send_request(command)

        elif choice == "4":
            from_account = input("Digite o numero da conta: ")
            to_account = input("Digite o numero da conta destino: ")
            amount = input("Digite o valor a ser transferido: ")
            command = f"TRANSFER {from_account} {to_account} {amount}"
            client.send_request(command)

        elif choice == "5":
            print("Saindo...")
            break

        else:
            print("Opcao invalida. Por favor escolha um valor entre 1 e 5.")

if __name__ == "__main__":
    main()