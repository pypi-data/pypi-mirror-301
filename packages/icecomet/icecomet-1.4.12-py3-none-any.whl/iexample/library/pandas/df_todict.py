import pandas as pd
df = pd.DataFrame({
    'A': ['foo', 'bar', 'foo', 'bar', 'foo'],
    'B': ['one', 'one', 'two', 'three', 'two']
})

#สำหรับทำ dataframe ให้เป็น dict
def to_dict_format(DataFrame):
    Output_DataFrame = {}
    for i in df:
        Output_DataFrame[i]=DataFrame[i].tolist()
    return Output_DataFrame