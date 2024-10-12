from iprint import *
oncode()
import pandas as pd
if False:
    pd.read_csv('url')
    pd.read_csv('path')
    df = pd.read_csv('ที่ตั้ง', encoding="ISO-8859-11",thousands=',',na_values='-')

    pd.read_excel('djkls')
    # from google.colab import drive
    # drive.mount('/content/drive')
    # file_path = '/content/drive/My Drive/data_.csv'

    

#ประกาศจากอาเรย์ หรือใกล้เคียง 
#ไม่มีหัวคอลัมน์ pandas จะเจนให้เป็นเลข
#กลายเป็นข้อมูลใน DataFrame
#    0  1  2
# 0  a  1  2
# 1  b  2  3
# 2  c  3  4
M = [['a',1,4],
     ['b',2,3],
     ['c',3,2],
     ['d',4,1]]
df = pd.DataFrame(M)
df = pd.DataFrame(M, columns=['ก', 'ข', 'ค'])

df.head(3)
df.tail(3)
#df.info() #สั่ง print() ในตัวเอง

df.shape # (4,3) ดูจำนวน แถว,คอลัม
df.dtypes #ดูชนิดของข้อมูลในแต่ละคอลัมน์


df.describe() #ให้ค่าสถิติของข้อมูลคอลัมที่เป็นตัวเลข

df['ข'].max() #สืบทอดคุณสมบัติแบบ numpy
df['ข'].mean()
df['ข'].sum()


df.iloc[:,1] # แถว:คอลัมน์  (index || slice)
df.loc[0,'ค'] #คอลัมน์เป็นชื่อเท่านั้น

df.columns = ['A','B','C']

df.columns.name = None #??
df = df.reset_index() #เรียงอินเดกซ์ใหม่
##################################
#ตอนที่ 2 ทำความสะอาด
import pandas as pd
import numpy as np
data = {
    'A': [1, 2, 30, 4, 5, 60, 7, np.nan, 9, 10],
    'B': [1, 2, 3, np.nan, 5, 6, 70, np.nan, 9, 20],
    'C': [1, 20, 3, 4, 5, 60, 7, np.nan, 9, 30],
    'D': [np.nan, 2, 3, 4, np.nan, 6, 7, np.nan, 9, 40],
    'E': [1, 2, 3, np.nan, 5, 6, 7, np.nan, 9, 50]
}
df = pd.DataFrame(data)

df[df['E'].isnull()] #ตารางที่มีเฉพาะแถวที่มีค่าใดค่าหนึ่งเป็น NaN

df.dropna() #เคลียร์แถวที่มี NaN ทิ้ง
df.dropna(subset=['A','B']) #คิดแค่คอลัมน์ A B



ij(df)


##################################
#ตอนที่ 3 ว่าด้วยเรื่องการจัดกลุ่ม
exit()
# สร้าง DataFrame ตัวอย่าง
data = {
    'พนักงาน': ['John', 'Anna', 'Peter', 'Linda', 'James', 'Emily', 'Michael', 'Sarah', 'David', 'Laura'],
    'แผนก': ['IT', 'HR', 'IT', 'HR', 'Finance', 'Finance', 'IT', 'HR', 'Finance', 'IT'],
    'เงินเดือน': [50000, 60000, 55000, 58000, 45000, 47000, 62000, 54000, 48000, 51000],
    'วันทำงาน': [220, 210, 225, 200, 240, 235, 215, 205, 225, 230]
}
df = pd.DataFrame(data)

#คำสั่งgrupby ต้องใช้กับเมธอดสถิติเท่านั้น
df = df.groupby('แผนก')['เงินเดือน'].sum()
agg_result = df.groupby('แผนก')['เงินเดือน'].agg(['mean', 'min', 'max'])
multi_grouped = df.groupby(['แผนก', 'วันทำงาน'])['เงินเดือน'].sum()
pivot = df.pivot_table(values='เงินเดือน', index='แผนก', aggfunc='mean')

####################################################################














