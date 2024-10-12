import sys

# เช็คจำนวน argument
if len(sys.argv) < 2:
    print("กรุณาส่งค่า argument อย่างน้อย 1 ค่า")
    sys.exit(1)

# รับค่าจาก argument
argument = sys.argv[1]
print(f"ค่าที่ส่งเข้ามาคือ: {argument}")
