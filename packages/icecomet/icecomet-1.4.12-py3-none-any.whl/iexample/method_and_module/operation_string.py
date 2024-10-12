#main

"hello,world".split(",")   # แยกสตริงโดยใช้ "," เป็นตัวแบ่ง ['hello', 'world']
",".join(["a", "b", "c"])  # รวมลิสต์เป็นสตริง โดยใช้ "," เป็นตัวเชื่อม "a,b,c"
"hello world".replace("world", "Python")  # แทนที่ "world" ด้วย "Python" "hello Python"

"hello world".count("l")   # นับจำนวนครั้งที่ "l" ปรากฏในสตริง 3

"123".isdigit()           # ตรวจสอบว่ามีแต่ตัวเลขหรือไม่ True

"hello".upper()           # ทำให้เป็นตัวใหญ่ทั้งหมด "HELLO"
"HELLO".lower()           # ทำให้เป็นตัวเล็กทั้งหมด "hello"


##################################################################################
#การแก้ไข
"hello".upper()           # ทำให้เป็นตัวใหญ่ทั้งหมด "HELLO"
"HELLO".lower()           # ทำให้เป็นตัวเล็กทั้งหมด "hello"
"hello world".capitalize()# ทำให้ตัวแรกเป็นตัวใหญ่ "Hello world"
"hello world".title()     # ทำให้ตัวแรกของแต่ละคำเป็นตัวใหญ่ "Hello World"
"  hello  ".strip()       # ลบช่องว่างหน้าหลัง "hello"
"  hello  ".lstrip()      # ลบช่องว่างด้านซ้าย "hello  "
"  hello  ".rstrip()      # ลบช่องว่างด้านขวา "  hello"
"hello world".replace("world", "Python")  # แทนที่ "world" ด้วย "Python" "hello Python"
"hello world".swapcase()  # สลับตัวใหญ่-เล็ก "HELLO WORLD"
"hello".center(10)        # จัดสตริงให้อยู่กลางในพื้นที่กว้าง 10 ช่อง "  hello   "
"hello".ljust(10)         # จัดสตริงชิดซ้ายในพื้นที่กว้าง 10 ช่อง "hello     "
"hello".rjust(10)         # จัดสตริงชิดขวาในพื้นที่กว้าง 10 ช่อง "     hello"
"abcd"[::-1]              # กลับด้านข้อความ

#การตรวจสอบและค้นหา
"hello".startswith("he")  # ตรวจสอบว่าขึ้นต้นด้วย "he" หรือไม่ True
"hello".endswith("lo")    # ตรวจสอบว่าลงท้ายด้วย "lo" หรือไม่ True
"hello".isalpha()         # ตรวจสอบว่ามีแต่ตัวอักษรหรือไม่ True
"123".isdigit()           # ตรวจสอบว่ามีแต่ตัวเลขหรือไม่ True
"hello123".isalnum()      # ตรวจสอบว่ามีแต่ตัวอักษรหรือตัวเลขหรือไม่ True
"hello".islower()         # ตรวจสอบว่าทุกตัวเป็นตัวเล็กหรือไม่ True
"HELLO".isupper()         # ตรวจสอบว่าทุกตัวเป็นตัวใหญ่หรือไม่ True
"   ".isspace()           # ตรวจสอบว่าเป็นช่องว่างทั้งหมดหรือไม่ True
"Hello World".istitle()   # ตรวจสอบว่าเป็นแบบ title case หรือไม่ True

#การแยกข้อความ
"hello world".split()      # แยกสตริงโดยใช้ช่องว่างเป็นตัวแบ่ง ['hello', 'world']
"hello,world".split(",")   # แยกสตริงโดยใช้ "," เป็นตัวแบ่ง ['hello', 'world']
"hello world".rsplit()     # แยกสตริงจากด้านขวา โดยใช้ช่องว่างเป็นตัวแบ่ง ['hello', 'world']
"hello".partition("l")     # แยกสตริงเป็นสามส่วนที่เจอ "l" ('he', 'l', 'lo')
"hello".rpartition("l")    # แยกสตริงเป็นสามส่วนจากด้านขวาที่เจอ "l" ('hel', 'l', 'o')
",".join(["a", "b", "c"])  # รวมลิสต์เป็นสตริง โดยใช้ "," เป็นตัวเชื่อม "a,b,c"
"hello world".count("l")   # นับจำนวนครั้งที่ "l" ปรากฏในสตริง 3
"hello world".find("world")# หาตำแหน่งที่เจอ "world" เป็นครั้งแรก 6
"hello world".index("world")# หาตำแหน่งที่เจอ "world" เป็นครั้งแรก 6
"hello world".rfind("l")   # หาตำแหน่ง "l" ครั้งสุดท้ายจากขวา 9
"hello world".rindex("l")  # หาตำแหน่ง "l" ครั้งสุดท้ายจากขวา 9

#การเติมเต็มสตริง
"42".zfill(5)              # เติมศูนย์ด้านหน้าจนความยาวเป็น 5 "00042"
"42".rjust(5, '0')         # เติม "0" ด้านซ้ายจนความยาวเป็น 5 "00042"
"hello".ljust(10, '*')     # เติม "*" ด้านขวาจนความยาวเป็น 10 "hello*****"
"hello".rjust(10, '*')     # เติม "*" ด้านซ้ายจนความยาวเป็น 10 "*****hello"
