sum([1, 2, 3])           # หาผลรวมของลิสต์ 6
min(1, 2, 3)             # หาค่าต่ำสุด 1
max(1, 2, 3)             # หาค่าสูงสุด 3
mean = sum([3,4,5])/len([3,4,5])

from collections import Counter
data = [1, 2, 2, 3, 4, 4, 4, 5, 5, 5, 5]
counter = Counter(data)  # นับจำนวนของแต่ละค่าในลิสต์
print(counter)           # Output: Counter({5: 4, 4: 3, 2: 2, 1: 1, 3: 1})


############################################################################################
import statistics
data = [1, 2, 2, 3, 4, 4, 4, 5, 5, 5, 5]

mean = statistics.mean(data)         # หาค่าเฉลี่ย (mean) 3.4545454545454546
median = statistics.median(data)     # หาค่ามัธยฐาน (median) 4
mode = statistics.mode(data)         # หาค่าฐานนิยม (mode) 5
variance = statistics.variance(data) # หาค่าความแปรปรวน (variance) 1.6565656565656566
stdev = statistics.stdev(data)       # หาค่าส่วนเบี่ยงเบนมาตรฐาน (standard deviation) 1.2878473445191775
############################################################################################
import numpy as np
data = [1, 2, 2, 3, 4, 4, 4, 5, 5, 5, 5]
array = np.array(data)

mean = np.mean(array)                # หาค่าเฉลี่ย (mean) 3.4545454545454546
median = np.median(array)            # หาค่ามัธยฐาน (median) 4.0
mode = np.argmax(np.bincount(array)) # หาค่าฐานนิยม (mode) 5
variance = np.var(array)             # หาค่าความแปรปรวน (variance) 1.5041322314049586
stdev = np.std(array)                # หาค่าส่วนเบี่ยงเบนมาตรฐาน (standard deviation) 1.2260107272602906
