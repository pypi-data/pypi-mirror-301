#เพิ่มและแก้ไข
lst = [1, 2, 3]
lst.append(4)            # เพิ่ม 4 ไปท้ายลิสต์ [1, 2, 3, 4]
lst.insert(1, "a")       # แทรก "a" ที่ตำแหน่ง 1 [1, "a", 2, 3, 4]
lst.extend([5, 6])       # ขยายลิสต์ด้วยอีกลิสต์ [1, "a", 2, 3, 4, 5, 6]
lst[0] = 0               # เปลี่ยนค่าที่ตำแหน่ง 0 เป็น 0 [0, "a", 2, 3, 4, 5, 6]
lst[1:3] = ["b", "c"]    # แทนที่ช่วงตำแหน่ง 1-2 ด้วย ["b", "c"] [0, "b", "c", 3, 4, 5, 6]

#การเรียง
lst = [3, 1, 4, 2, 5]
lst.sort()               # เรียงลำดับลิสต์จากน้อยไปมาก [1, 2, 3, 4, 5]
lst.sort(reverse=True)   # เรียงลำดับลิสต์จากมากไปน้อย [5, 4, 3, 2, 1]
lst.reverse()            # สลับลำดับในลิสต์จากหลังมาหน้า [1, 2, 3, 4, 5]

#การค้นหาและตรวจสอบ
lst = [1, 2, 3, 4, 5]
index = lst.index(3)     # หาตำแหน่งของค่า 3 ในลิสต์ index = 2
count = lst.count(2)     # นับจำนวนครั้งที่ 2 ปรากฏในลิสต์ count = 1
exists = 4 in lst        # ตรวจสอบว่ามี 4 อยู่ในลิสต์หรือไม่ True

#การคัดลอกและนับจำนวน
lst = [1, 2, 3]
lst_copy = lst.copy()    # สร้างสำเนาลิสต์ใหม่ lst_copy = [1, 2, 3]
length = len(lst)        # นับจำนวนสมาชิกในลิสต์ length = 3

#การรวมและแยก
lst = [1, 2, 3]
lst.extend([4, 5])       # ขยายลิสต์ด้วยอีกลิสต์ [1, 2, 3, 4, 5]
combined = lst + [6, 7]  # รวมลิสต์กับลิสต์ใหม่ [1, 2, 3, 4, 5, 6, 7]
sliced = lst[1:3]        # สร้างลิสต์ใหม่จากส่วนย่อยของลิสต์ [2, 3]

#การลบและทำความสะอาดข้อมูล
lst = [0, "b", "c", 3, 4, 5, 6]
lst.remove("b")          # ลบค่าที่เป็น "b" ออกจากลิสต์ [0, "c", 3, 4, 5, 6]
popped = lst.pop()       # เอาค่าตัวสุดท้ายออกจากลิสต์และเก็บไว้ใน popped [0, "c", 3, 4, 5] (popped = 6)
popped = lst.pop(2)      # เอาค่าที่ตำแหน่ง 2 ออกจากลิสต์และเก็บไว้ใน popped [0, "c", 4, 5] (popped = 3)
lst.clear()              # ลบข้อมูลทั้งหมดในลิสต์ []

#ว่าด้วยการคัดกรอง
numbers = [1, 4, 6, 8, 3, 7, 2]
filtered_numbers = [num for num in numbers if num > 5]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))



doubled_numbers = list(map(lambda x: x * 2, numbers))

#เรียงตาม?? ค่อยคิด
students = [{'name': 'Alice', 'score': 90},
            {'name': 'Bob', 'score': 75},
            {'name': 'Charlie', 'score': 85}]
sorted_students = sorted(students, key=lambda x: x['score'])








