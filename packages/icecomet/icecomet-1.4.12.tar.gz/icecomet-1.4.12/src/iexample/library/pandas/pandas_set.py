index,value,start,end,ABC_charSets,target = 0
import pandas as pd
from icprint import *
df = pd.read_csv('m.csv')

df['e'] = 4
del df['e']

df.drop('column_name', axis=1)
df.drop('column_name', axis=1, inplace=True)
df = df.drop(['column_name1', 'column_name2'], axis=1)

df = df.drop(index)
df.drop(index, inplace=True)
df = df[df['column_name'] != value] #คัดกรองเอาแค่แถว ที่มีค่าไม่เข้าเงื่อนไขตามที่กำหนด
df = df.drop(df.index[start:end])
df = df[df['fomula'].notna()] #คัดกรองเอาค่าว่าง(NaN) ออกไป

df['fomula'][ABC_charSets.index(target)] #ส่งกลับเป็นค่าในคอลัม fomula ที่คอลัม target


df = df.reset_index(drop=True) #เรียงอินเดกซ์ใหม่

'''คอลัม'''
# df['column_name']
df.c

'''แถว'''
df.iloc[0]  # เข้าถึงแถวแรก

'''ล็อกพิกัด'''
df.iloc[0, 1]  # เข้าถึงข้อมูลในแถวแรก คอลัมน์ที่สอง
df.loc[3, 'age']  # เข้าถึงข้อมูลในแถวที่มี index เท่ากับ 3 และคอลัมน์ 'age'

'''คัดกรอง'''
df[df['age'] > 30]  # เข้าถึงแถวที่มีค่าของคอลัมน์ 'age' มากกว่า 30


for i,o in df.iterrows(): #ส่งค่าทั้งแถวออกมา
    ij(o.tolist(),'ti')






import matplotlib.pyplot as plt
import pandas as pd
#อ่าน
url = 'url_or_file_path'
df = pd.read_excel(url)
df = pd.read_csv(url)
df_e = pd.read_csv(url, encoding="ISO-8859-11")

df_e = pd.read_csv(url, encoding="ISO-8859-11", thousands=',', na_values='-')


#เรียกข้อมูล
df.info()
df.head(9)
df.tail(9)
A = df[['sex','game_name','device']].head(5) #คอลัมตามนั้น เอา 5 แถวแรก



#missing data
a = df.dropna() ##แถวที่มี none ไม่เรียงอินเดกซ์ใหม่
a = df.dropna(inplace=True)  ##ลบแถวที่มี none แล้วเรียงอินเดกซ์ใหม่

a = df.dropna(subset=['A','B'])  # run โค้ดนี้เพื่อดูผลลัพธ์ของการตัดแถวที่ข้อมูลในคอลัมน์ 'A' หรือ 'B' เป็น NaN
D = pd.read_csv(url, thousands=',', na_values='-') #thousands=',' บอกว่านี่คือตัวคั่นหลักพัน //// na_values='-' บอกว่า ตัวนี้แทนค่าว่าง
N = df[df['E'].isnull()] #ตารางแถวที่มีค่าเป็น none ใน E


# แก้ไขค่า
variable = {'male': 1, 'female': 2}   #แทนที่
df = df.replace({'เพศ': variable})    #แทนที่

#สร้างข้อมูล

df['country'] = "Thailand"
df['newSex'] = df['sex']
df['age'] = df['age']+100
df = df.drop(4) #ลบข้อมูลแถวที่ 4
del df['age']

#สถิติพื้นฐาน
print(df.describe())
df['sex'].value_counts()
med = df['age'].median()

from scipy import stats #เรียกใช้โมดูลทางคณิตศาสตร์
mode = stats.mode(df['age'])

data = df[['age', 'hr']]
data.corr()



















    








