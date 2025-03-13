import socket
import os
import json
import xml.etree.ElementTree as ET
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Server")

def get_processes():
    processes = []
    if os.name == "nt":
        output = os.popen("tasklist").read().splitlines()
        for line in output[3:]:
            parts = line.split()
            if len(parts) > 1:
                processes.append({"pid": parts[1], "name": parts[0]})
    else:  # Linux / macOS
        output = os.popen("ps -eo pid,comm,user").read().splitlines()
        for line in output[1:]:  # Пропускаем заголовок
            parts = line.split(None, 2)
            if len(parts) == 3:
                processes.append({"pid": parts[0], "name": parts[1], "username": parts[2]})
    return processes

def save_processes(format='json'):
    data = get_processes()
    filename = f"processes.{format}"
    if format == 'json':
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    elif format == 'xml':
        root = ET.Element("processes")
        for proc in data:
            proc_elem = ET.SubElement(root, "process")
            for key, value in proc.items():
                ET.SubElement(proc_elem, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
    logger.info(f"Сохранен файл с процессами: {filename}")
    return filename

def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break  #клиент закрыл соединение
            
            command = data.split()
            logger.info(f"Получена команда от клиента: {command}")
            
            if command[0] == 'UPDATE':
                if len(command) > 1 and command[1].upper() == 'XML':
                    filename = save_processes(format='xml')
                else:
                    filename = save_processes(format='json')
                
                try:
                    with open(filename, 'rb') as f:
                        file_data = f.read()
                    conn.sendall(file_data)  #отправляем данные клиенту
                    logger.info(f"Отправлен файл с процессами клиенту: {filename}")
                except ConnectionError as e:
                    logger.error(f"Ошибка при отправке данных клиенту: {e}")
                    break
            elif command[0] == 'KILL' and len(command) == 3:
                try:
                    pid = int(command[1])
                    sig = int(command[2])
                    os.kill(pid, sig)
                    conn.send(b'SUCCESS')
                    logger.info(f"Отправлен сигнал {sig} процессу {pid}")
                except Exception as e:
                    conn.send(str(e).encode('utf-8'))
                    logger.error(f"Ошибка при отправке сигнала: {e}")
            else:
                conn.send(b'INVALID COMMAND')
                logger.warning(f"Неизвестная команда: {command}")
    except Exception as e:
        logger.error(f"Ошибка при обработке клиента: {e}")
    finally:
        conn.close()
        logger.info("Соединение с клиентом закрыто")

def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    logger.info(f"Сервер запущен на {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        logger.info(f"Подключен клиент: {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_server()