import subprocess

# รันสคริปต์ Python และรับผลลัพธ์
result = subprocess.run(['python', 'script.py', 'your_value'], capture_output=True, text=True)
print("ผลลัพธ์จากสคริปต์:", result.stdout)
##############################################################################################
import os
#ในสคริปต์ ให้สั่ง print() แล้วมันจะกลายเป็น result
# รันสคริปต์ Python และรับผลลัพธ์
result = os.popen('python script.py your_value').read()
print("ผลลัพธ์จากสคริปต์:", result)