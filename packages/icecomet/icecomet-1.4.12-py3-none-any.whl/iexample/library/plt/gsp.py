import matplotlib.pyplot as plt
import matplotlib.patches as patches

# สร้างกราฟ
fig, ax = plt.subplots()

# การวาดเส้น
ax.plot(x, y, label='sin(x)')

# สร้างวงกลม
circle = patches.Circle((0, 0), radius=1, edgecolor='blue', facecolor='lightblue')

# การวาดเส้นแนวนอนและแนวตั้ง
ax.axhline(y=0, color='black', linestyle='--')
ax.axvline(x=5, color='blue', linestyle='-.')


# เพิ่มวงกลมลงในกราฟ
ax.add_patch(circle)

# กำหนดขนาดแกน
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal', 'box')  # ทำให้แกนมีสัดส่วนเท่าเทียมกัน

# แสดงกราฟ
plt.grid()
plt.title("Circle using patches")
plt.show()
