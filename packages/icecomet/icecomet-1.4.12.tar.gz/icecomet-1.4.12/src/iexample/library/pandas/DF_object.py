import pandas as pd
from iprint import *

df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': ['one', 'two', 'three', 'four', 'five'],
    'C': ['small', 'large', 'large', 'small', 'large'],
})

#for i in df: > ชื่อของแต่ละคอลัมน์
#serise.to_list() จะใด้ลิสต์ของข้อมูล

#for i in df.items(): > (name_col,serise_col)      : i[1].to_list() จะใด้ลิสต์ของข้อมูลใน คอลัมน์
#for i in df.iterrow(): > (index_row,serise_row)   : i[1].to_list() จะใด้ลิสต์ของข้อมูลใน แถว

'''ถ้าเลือกเป็นช่วงข้อมูล จะใด้เป็น ซีรีย์'''
j = df.iloc[:,1]   #(name_col,serise_col)
j = df.iloc[0,:]   #(index_row,serise_row)
j = df.iloc[0]     #(index_row,serise_row)

'''ถ้าเลือกเป็นพื้นที่ จะใด้ค่าเป็นตารางใหม่'''
#iloc[index_line_row,index_col]
j = df.iloc[:4,:]

df.iterrows() #ส่งค่ากลับเหมือน enumerate [(index,ค่า),...]








