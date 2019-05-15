import pandas as pd

# file_path = os.path('./infos.csv') #指定文件路径

# 将csv中的数据读取出来
data = pd.read_csv('./infos.csv', encoding='gbk')
# print(data)

# 给数据创建对象
frame = pd.DataFrame(data)

# DataFrame.drop_duplicates(subset=None, keep='first', inplace=False)
'''
subset：指定特定列，默认为所有列
keep:保留特定列，默认保留第一列，
inplace:为真时，保留一个副本
'''
# 对数据去重
frame.drop_duplicates('电话', 'first', inplace=True)

# 写入csv
# frame.to_csv('./new_infos.csv', encoding = 'gbk', index = False)
# 写入excel
frame.to_excel('./infos.xlsx', encoding='gbk', index=False)
