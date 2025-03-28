import time
import os

print("Процесс запущен. PID:", os.getpid())
while True:
    time.sleep(1)
    print("Работаю....")