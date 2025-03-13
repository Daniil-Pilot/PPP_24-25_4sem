import subprocess
import time

def main():
    server_process = subprocess.Popen(["python", "server.py"])
    
    # Ждун на 2 секунды
    time.sleep(2)
    
    client_process = subprocess.Popen(["python", "client.py"])
    
    client_process.wait()
    
    server_process.terminate()

if __name__ == "__main__":
    main()