import matplotlib.pyplot as plt
import numpy as np


fi = plt.figure('window_name')

ax1 = fi.add_subplot(221, projection='3d')
ax2 = fi.add_subplot(222, projection='3d')
ax3 = fi.add_subplot(235, projection='3d')


# สร้าง Figure และ Axes
fig, ax = plt.subplots(figsize=(12, 8))

# 25 : 1. การวาดกราฟเส้น
# 29 : 2. การวาดกราฟจุดกระจาย
# 32 : 3. การวาดกราฟแท่ง
# 35 : 4. การวาดฮิสโตแกรม bins : ขอบเขต
# 39 : 5. การวาดกล่องที่แสดงการกระจาย
# 42 : 6. การแสดงภาพ
# 46 : 7. การวาดแผนภูมิวงกลม
# 51 : 8. การปรับแต่งกราฟ
# 60 : 9. การเพิ่มข้อความ
# 63 : 10. การเพิ่มการแสดงข้อความหรือป้าย
# 67 : 11. การวาดเส้นแนวนอนและแนวตั้ง
# 71 : 12. การเติมพื้นที่ใต้เส้นกราฟ
# 75 : 13. การจัดการความสัมพันธ์
# 81 : 14. การบันทึกภาพกราฟ
# 84 : แสดงผลกราฟ

x=[1,2,3,4]
y=[1,2,3,4]
# 1. การวาดกราฟเส้น
ax.plot(x, y, label='sin(x)')


# 2. การวาดกราฟจุดกระจาย
ax.scatter(x, y, color='red', label='Random Points')

# 3. การวาดกราฟแท่ง
ax.bar(x, y, color='green', alpha=0.6, label='Bar Chart')

# 4. การวาดฮิสโตแกรม bins : ขอบเขต
data = np.random.randn(1000)
ax.hist(data, bins=30, alpha=0.3, label='Histogram')

# 5. การวาดกล่องที่แสดงการกระจาย
data_box = [np.random.normal(size=100) for _ in range(5)]
ax.boxplot(data_box, labels=['A', 'B', 'C', 'D', 'E'])
# 6. การแสดงภาพ
image = np.random.rand(10, 10)
ax.imshow(image, cmap='viridis', interpolation='none', alpha=1, label='Image')

# 7. การวาดแผนภูมิวงกลม
sizes = [15, 30, 45, 10]
labels = ['A', 'B', 'C', 'D']
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

# 8. การปรับแต่งกราฟ
ax.set_title('Comprehensive Example of Axes Methods')
ax.set_xlabel('X-axis Label')
ax.set_ylabel('Y-axis Label')
ax.set_xlim(0, 10)
ax.set_ylim(-2, 2)
ax.grid(True)
ax.legend()

# 9. การเพิ่มข้อความ
ax.text(5, 0, 'Center Text', fontsize=12, ha='center')

# 10. การเพิ่มการแสดงข้อความหรือป้าย
ax.annotate('Peak', xy=(5, np.sin(5)), xytext=(6, 0.5),
            arrowprops=dict(facecolor='black', shrink=0.05))

# 11. การวาดเส้นแนวนอนและแนวตั้ง
ax.axhline(y=0, color='black', linestyle='--')
ax.axvline(x=5, color='blue', linestyle='-.')

# 12. การเติมพื้นที่ใต้เส้นกราฟ
ax.fill_between(x, y, color='lightblue', alpha=0.5)


# 13. การจัดการความสัมพันธ์
ax2 = ax.twinx()  # สร้างแกน Y ที่สอง
ax2.plot(x, [i*2 for i in y], color='orange', label='2 * sin(x)')
ax2.set_ylabel('Secondary Y-axis')
ax2.legend(loc='upper right')

# 14. การบันทึกภาพกราฟ
fig.savefig('matplotlib_examples.png')

# แสดงผลกราฟ

plt.show()