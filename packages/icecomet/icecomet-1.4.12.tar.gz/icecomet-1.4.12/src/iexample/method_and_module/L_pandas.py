import pandas as pd  # โดยทั่วไปจะเรียกใช้งานไลบรารีนี้ด้วยการใช้ชื่อย่อว่า pd


#การอ่านข้อมูลจากไฟล์
df = pd.read_csv('data.csv')  # อ่านข้อมูลจากไฟล์ CSV

#คัดเลือกและแยก
print(df['Name'])  # เลือกคอลัมน์เดียว
print(df[['Name', 'City']])  # เลือกหลายคอลัมน์
adults = df[df['Age'] > 30]  # เลือกแถวที่มีอายุมากกว่า 30


#การดูข้อมูล
print(df.head())  # แสดงข้อมูล 5 แถวแรก (ค่าเริ่มต้น)
print(df.tail(3)) # แสดงข้อมูล 3 แถวสุดท้าย
print(df.info())  # แสดงข้อมูลเบื้องต้นของ DataFrame
print(df.describe()) # แสดงค่าสถิติของข้อมูลใน DataFrame

##########################################################################
#การสร้าง DataFrame จาก Dictionary
##########################################################################
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

df = pd.DataFrame(data)

#การสร้าง DataFrame จาก List
##########################################################################
data = [
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'Los Angeles'],
    ['Charlie', 35, 'Chicago']
]

df = pd.DataFrame(data, columns=['Name', 'Age', 'City'])

