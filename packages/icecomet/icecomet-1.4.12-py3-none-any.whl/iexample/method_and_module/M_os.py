import os

os.rename("old_name.txt", "new_name.txt")  # เปลี่ยนชื่อไฟล์ old_name.txt เป็น new_name.txt


####################################################################################################
#การทำงานกับไดเรคเทอรี
os.chdir("/path/to/directory")  # เปลี่ยนไดเร็กทอรีปัจจุบัน
current_directory = os.getcwd()  # หาตำแหน่งไดเร็กทอรีปัจจุบัน
files = os.listdir(".")  # แสดงรายการไฟล์และไดเร็กทอรีในไดเร็กทอรีปัจจุบัน
path = os.path.join("/path", "to", "directory")  # รวมเป็นเส้นทางเดียวกัน "/path/to/directory"
filename, file_extension = os.path.splitext("file.txt")  # แยกชื่อไฟล์และนามสกุล ("file", ".txt")

#การตามหา
directory = os.path.dirname("/path/to/file.txt")  # หาชื่อไดเร็กทอรี "/path/to"


####################################################################################################
#การสร้างและลบ
os.mkdir("new_directory")   # สร้างไดเร็กทอรีใหม่ชื่อ new_directory
os.makedirs("parent/child") # สร้างไดเร็กทอรีย่อย ๆ เช่น parent/child

os.remove("file.txt")       # ลบไฟล์ชื่อ file.txt
os.rmdir("new_directory")   # ลบไดเร็กทอรีที่ชื่อ new_directory
os.removedirs("parent/child") # ลบไดเร็กทอรี child และ parent หากเป็นไดเร็กทอรีว่าง

####################################################################################################
#การตรวจสอบ
os.path.exists("file.txt")  # ตรวจสอบว่า file.txt มีอยู่หรือไม่ True/False
os.path.isfile("file.txt")  # ตรวจสอบว่าเป็นไฟล์หรือไม่ True/False
os.path.isdir("my_directory") # ตรวจสอบว่าเป็นไดเร็กทอรีหรือไม่ True/False

####################################################################################################
#การทำงานกับ Environment Variables
path = os.getenv("PATH")  # เข้าถึง Environment Variable ชื่อ PATH
os.environ["MY_VARIABLE"] = "some_value"  # ตั้งค่า Environment Variable ใหม่









