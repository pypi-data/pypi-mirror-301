from multiprocessing import Process
import time
def process_1():
    for i in range(5):
        print(f"Process 1 - {i}")
        time.sleep(1)
        a+=1

def process_2():
    for i in range(5):
        print(f"Process 2 - {i}")
        time.sleep(2)
        b+=1

if __name__ == "__main__":
    # สร้าง Process สำหรับแต่ละฟังก์ชัน
    p1 = Process(target=process_1)
    p2 = Process(target=process_2)

    # เริ่มการทำงานของ Process ทั้งสอง
    p1.start()
    p2.start()

    # รอให้ Process ทั้งสองเสร็จสิ้นการทำงาน
    p1.join()
    p2.join()

    print("Both processes have finished.")
