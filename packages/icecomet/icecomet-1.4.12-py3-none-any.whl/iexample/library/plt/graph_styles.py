import matplotlib.pyplot as plt
import numpy as np

# สร้างข้อมูลตัวอย่าง
x = np.linspace(0, 10, 100)
y = np.sin(x)

# สร้าง Figure และ Axes
fig, ax = plt.subplots(figsize=(10, 6), dpi=80)

# การปรับแต่ง Axes
ax.set_xlim(0, 10)                  # ขอบเขตของแกน x
ax.set_ylim(-1.5, 1.5)              # ขอบเขตของแกน y
ax.set_xlabel('X-axis')             # ป้ายกำกับแกน x
ax.set_ylabel('Y-axis')             # ป้ายกำกับแกน y
ax.set_title('Sample Plot')         # ชื่อเรื่องของกราฟ
ax.grid(True)                       # แสดงกริด
ax.set_aspect('auto')               # การตั้งค่าอัตราส่วนของ Axes

# การปรับแต่ง Spines
ax.spines['top'].set_color('none')         # ซ่อน spine ด้านบน
ax.spines['right'].set_color('none')       # ซ่อน spine ด้านขวา
ax.spines['left'].set_color('blue')        # เปลี่ยนสี spine ด้านซ้าย
ax.spines['left'].set_linewidth(2)         # เปลี่ยนความหนาของ spine ด้านซ้าย
ax.spines['bottom'].set_color('red')       # เปลี่ยนสี spine ด้านล่าง

# การปรับแต่ง Ticks
ax.tick_params(axis='both', which='major', labelsize=12)     # ขนาดของ tick labels
ax.tick_params(axis='x', direction='inout', length=10)       # การปรับขนาดและทิศทางของ ticks

# การเพิ่ม Legend
ax.plot(x, y, label='Sine Wave')
ax.legend(loc='upper right', fontsize='small', title='Legend')

# การปรับแต่ง Facecolor
ax.set_facecolor('lightgrey')          # เปลี่ยนสีพื้นหลังของ Axes

# การแสดงผล
plt.show()
