import socket
import threading

class BankServer:
    def __init__(self):
        self.accounts = {}  # Account number -> (balance, client_name)
        self.logical_clock = 0

    def create_account(self, account_number, initial_balance, client_name):
        self.accounts[account_number] = (initial_balance, client_name)

    def get_balance(self, account_number, client_clock):
        self.logical_clock = max(self.logical_clock, client_clock) + 1
        if account_number in self.accounts:
            return self.accounts[account_number][0], self.logical_clock
        return None, self.logical_clock

    def withdraw(self, account_number, amount, client_clock):
        self.logical_clock = max(self.logical_clock, client_clock) + 1
        if account_number in self.accounts:
            balance, client_name = self.accounts[account_number]
            if balance >= amount:
                self.accounts[account_number] = (balance - amount, client_name)
                return True, self.logical_clock
        return False, self.logical_clock

    def deposit(self, account_number, amount, client_clock):
        self.logical_clock = max(self.logical_clock, client_clock) + 1
        if account_number in self.accounts:
            balance, client_name = self.accounts[account_number]
            self.accounts[account_number] = (balance + amount, client_name)
            return True, self.logical_clock
        return False, self.logical_clock

    def transfer(self, from_account, to_account, amount, client_clock):
        self.logical_clock = max(self.logical_clock, client_clock) + 1
        if from_account in self.accounts and to_account in self.accounts:
            if self.withdraw(from_account, amount, client_clock)[0]:
                return self.deposit(to_account, amount, client_clock)
        return False, self.logical_clock

def handle_client(client_socket, server):
    try:
        client_socket.settimeout(60)  # Optional: Set a timeout for the client socket.
        request = client_socket.recv(1024).decode()
        client_clock, command, *args = request.split()

        if command == "BALANCE":
            account_number = int(args[0])
            balance, server_clock = server.get_balance(account_number, int(client_clock))
            response = f"{server_clock} Balance: {balance}"
        
        elif command == "WITHDRAW":
            account_number = int(args[0])
            amount = float(args[1])
            success, server_clock = server.withdraw(account_number, amount, int(client_clock))
            response = f"{server_clock} Withdraw {'successful' if success else 'failed'}."

        elif command == "DEPOSIT":
            account_number = int(args[0])
            amount = float(args[1])
            success, server_clock = server.deposit(account_number, amount, int(client_clock))
            response = f"{server_clock} Deposit {'successful' if success else 'failed'}."

        elif command == "TRANSFER":
            from_account = int(args[0])
            to_account = int(args[1])
            amount = float(args[2])
            success, server_clock = server.transfer(from_account, to_account, amount, int(client_clock))
            response = f"{server_clock} Transfer {'successful' if success else 'failed'}."

        else:
            response = "Invalid command."

        client_socket.send(response.encode())
    finally:
        client_socket.close()

def main():
    server = BankServer()
    server.create_account(123, 1000.0, "John")
    server.create_account(456, 500.0, "Alice")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)

    print("Bank server is running...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, server))
        client_thread.start()

if __name__ == "__main__":
    main()
