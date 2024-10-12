import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from iprint import *

#ตั้งค่าตำแหน่งที่ภาพจะแสดง
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(121, projection='3d')

#กำหนดเส้นแกนของกราฟเพื่อที่จะวาดภาพออกมา
x = np.arange(4)
y = np.arange(5)
xx, yy = np.meshgrid(x, y)

x, y = xx.ravel(), yy.ravel()
top = x + y
bottom = np.zeros_like(top)

# #ขนาดแท่ง
width = 0.9
depth = 0.9

#ภาพที่แสดงแบบมีมิติ shade = True
ax.bar3d(x, y, bottom, width, depth, top , shade=True)

ax.set_title('')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')



plt.show()