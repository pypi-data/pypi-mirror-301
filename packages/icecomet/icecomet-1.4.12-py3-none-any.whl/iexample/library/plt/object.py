import matplotlib.pyplot as plt



#แบบย่อ แค่กราฟรูปเดียวต่อหนึ่งหน้าต่าง
# ประกาศชุดข้อมูลเป็นลิสต์
x = [1, 2, 3, 4, 5]  # ค่า x
y = [2, 3, 5, 7, 11]  # ค่า y

# สร้างหน้ากราฟ
plt.figure(figsize=(10, 6))  # ขนาดกราฟ หน่วยเป็นนิ้ว ใส่ขนาดหรือไม่ก็ใด้
plt.plot(x, y, marker='o', linestyle='-', color='blue', label='Data Line')

###########################################
#ถ้ามีการประกาศตัวแปร จะสามารถเข้าถึงภายหลังใด้
#สำหรับการสร้างกราฟหลายรูป
fi = plt.figure('ถ้ามีการประกาศตัวแปร จะสามารถเข้าถึงเพื่อแก้ไขภายหลักใด้')
ax1 = fi.add_subplot(221)
ax2 = fi.add_subplot(222)
ax3 = fi.add_subplot(235)

ax1.set_title('A')
ax2.set_title('B')
ax3.set_title('C')

#############################################
G = plt.figure('แต่จะไม่กำหนดก็ใด้ ถ้าแค่ใช้ชั่วคราว')
G.add_subplot(221)
G.add_subplot(222)
##กรณีประกาศตำแหน่งเดียวกับ จะทำการสร้างซ้อนกันของอัน
G.add_subplot(235).set_title('k')
G.add_subplot(235).set_title('T')


plt.show()









