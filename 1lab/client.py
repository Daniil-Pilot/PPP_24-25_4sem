import socket
import os
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("client.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Client")

def save_received_file(data, file_format):
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    dir_name = datetime.now().strftime("%d-%m-%Y")
    os.makedirs(dir_name, exist_ok=True)
    filename = f"{dir_name}/{timestamp}.{file_format}"
    
    with open(filename, 'wb') as f:
        f.write(data)
    logger.info(f"Файл сохранен: {filename}")

def send_command(command):
    server_address = ('127.0.0.1', 12345)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(server_address)
            client.sendall(command.encode('utf-8'))
            response = b''
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                response += chunk
            logger.info(f"Команда '{command}' отправлена")
            return response
    except Exception as e:
        logger.error(f"Ошибка при отправке команды: {e}")
        return None

def main():
    while True:
        print("\nДоступные команды:")
        print("1. UPDATE - запросить обновленный список процессов (JSON)")
        print("2. UPDATE XML - запросить обновленный список процессов (XML)")
        print("3. KILL <pid> <signal> - завершить процесс")
        print("4. EXIT - выйти")
        
        command = input("Введите команду: ")
        if command.upper() == "EXIT":
            logger.info("Клиент завершает работу")
            break
        
        response = send_command(command)
        
        if response is None:
            print("Ошибка при отправке команды. Проверьте логи.")
            continue
        
        if command.upper().startswith("UPDATE"):
            if "XML" in command.upper():
                save_received_file(response, 'xml')
            else:
                save_received_file(response, 'json')
        else:
            print("Ответ сервера:", response.decode('utf-8'))

if __name__ == "__main__":
    main()