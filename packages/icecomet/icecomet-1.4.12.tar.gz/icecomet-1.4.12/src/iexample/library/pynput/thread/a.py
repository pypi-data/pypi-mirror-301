import threading
import time
def func():
    n=0
    while n<5:
        print(n)
        n+=1
        time.sleep(1)
t = threading.Thread(target=func)
r = threading.Thread(target=func)

t.start()  # เริ่มการทำงานของ thread ที่เรียกฟังก์ชัน scroll
time.sleep(3)
t.start()
r.start()


