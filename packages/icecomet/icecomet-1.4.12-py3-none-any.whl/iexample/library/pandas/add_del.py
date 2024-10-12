from ipandas import *
from icprint import *

df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': ['one', 'two', 'three', 'four', 'five'],
    'C': ['small', 'large', 'large', 'small', 'large'],
})
#การประกาศคอลัมน์ใหม่ และดำเนินการกับแต่ละค่าใน colum
####################################################################
df['D'] = 3
df['D'] = df['D']+[i+1 for i in range(5)]

df['D'] = [i for i in 'ABCDE']
df['D'] = df['D']+'HHH'

del df['D']


#การประกาศแถวใหม่ และดำเนินการกับแต่ละค่าใน row
new_values = [10, 20, 30,40,50]

# แทนที่ข้อมูลในแถวที่ 2 (index 1)
df.loc[1] = new_values

#df.insert(index_col, name, [list / serise / ค่าเดียว], อนุญาติให้ค่าซ้ำกันหรือไม่)
df.insert(0, 'sta', new_values, allow_duplicates=False)
####################################################################

#การแก้ไข
####################################################################




ij(df)










