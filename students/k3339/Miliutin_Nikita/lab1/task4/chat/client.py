import socket       
import json
import threading
from chat.server_messages import CLIENT_SEND_ERROR
from chat.config import BUFFER_SIZE, ENCODING, HOST, PORT


class Client:
    
    def __init__(self) -> None:
        self.name = input("Введите ваше имя: ")
        self.file = input("Введите файл вывода: ")
        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c_socket.connect((HOST, PORT))
        self.give_name()
        self.l_thread = threading.Thread(target=self.listen, daemon=True)
        self.wi_thread = threading.Thread(target=self.w_input)
        self.l_thread.start()
        self.wi_thread.start()


    def give_name(self) -> None:
        try:
            server_request = json.loads(self.c_socket.recv(BUFFER_SIZE).decode(ENCODING))
            if isinstance(server_request, dict) and server_request["mes_type"] == "REG_NAME":
                name_mes = json.dumps({"name": self.name})
                self.send(name_mes)
            else:
                raise Exception
        except Exception as e:
            self.c_socket.close()
            print(e)


    def send(self, mes: str) -> None:
        try:
            self.c_socket.send(mes.encode(ENCODING))
        except Exception:
            print(CLIENT_SEND_ERROR)


    def listen(self):
        try:
            while True:
                data = self.c_socket.recv(BUFFER_SIZE).decode(ENCODING)
                with open(self.file, "a") as file:
                    file.write(data + "\n")
                if not data:
                    break
        except Exception as e:
            self.c_socket.close()
            print(e)


    def w_input(self):
        try:
            while True:
                c_mes = input("Введите сообщение: ")
                if c_mes == "exit":
                    print("Завершаю соединение.")
                    break
                self.send(c_mes)
        except Exception as e:
            self.c_socket.close()
            print(e)
