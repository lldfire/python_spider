import csv, re, math
from pyecharts import TreeMap
from matplotlib import pyplot as plt

education = []
salary = []
work_year = []
def get_message():
    with open('./lagou.csv', 'r' , newline  = '') as csvfile:
        content = csv.reader(csvfile)
        
        #读取学历、薪水、工作经验信息
        i = 0
        for row in content:
            if i != 0:
                education.append(row[2])  
                salary.append(row[3])
                work_year.append(row[1])
   
            i += 1
    #print(work_year)
def make_bar():

    #创建字典，每个学历的统计数 count(x) 统计列表中x的次数，
    education_table = {}
    for i in education:
        education_table[i] = education.count(i)
    #print(education_table)

    #将字典中键、值分别于列表中，作为图标的数值参数
    keys = []
    values = []
        
    #遍历键值对并存入列表
    for k, v in education_table.items(): #将字典转化为可迭代对象
        keys.append(k)
        values.append(v)
    print(keys, values)
    
    #设置显示中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    #使用matplotlib.pyplot，创建条形图
    plt.bar(keys, values, width = 0.35, color = 'red')
    plt.xticks(range(len(keys)), keys)
    plt.title('education_required')
    
    #在图上显示数值,plt.text()给直方图添加标签，第一个参数：标签值，第二个：y轴位置位置，第三个参数：未知，第四个参数：居中、左、右
    for x, y in enumerate(values):
        plt.text(x, y+5, '%s' % round(y,1), ha='center')

    plt.show()
  
    """
    #使用 pyecharts.TreeMap
    data = [] #准备绘制图形的参数，参数为一个包含二元字典的列表
    for i in range(len(keys)):
        dict_1 = {'value':12, 'name':'sss'}
        dict_1['value'] = values[i]
        dict_1['name'] = keys[i]
        data.append(dict_1)
    print(data)

    #使用TreeMap方法画图,创建队形并设置图形的名称，和尺寸
    tree_map = TreeMap('矩形数图', width = 1200, height = 600 )
    #传入数据，并显示出来，并设置
    tree_map.add('学历要求', data, is_label_show = True, label_pos = 'inside')    
    """
def make_pie():
    #整理薪水数据
    #遍历每条薪水数据，求其中间值并存储起来
    avg_salary = []
    for s in salary:
        pat = '([0-9]+)'
        response = re.findall(pat, s)
        
        if len(response) == 2:
            a0 = (response[0])
            b0 = response[1]
        else:
            a0 = response[0]
            b0 = response[0]
    
        avg_salary.append((int(a0)+int(b0))/2)
    #print(avg_salary)  #薪资的平均值
    
    #统计平均值中各值 的数量，并以字典存储起来
    salary_table = {}
    for x in avg_salary:
        salary_table[x] = avg_salary.count(x)
    #print(salary_table)

    key = ['5K以下', '5K-10K', '10K-20K', '20K-30K', '30K-40K', '40K-50K', '50K以上']
    a0,b0,c0,d0,e0,f0,g0 = [0, 0, 0, 0, 0, 0, 0]

    for k, v in salary_table.items():
        #使用math.ceil()将价格转化为整数，向上取整
        avg = math.ceil(k)
        #print(avg)
        if avg <= 5:
            a0 += v
        elif 5 < avg <=10:
            b0 += v
        elif 10 < avg <=20:
            c0 += v
        elif 20 < avg <=30:
            d0 += v
        elif 30 < avg <=40:
            e0 += v
        elif 40 < avg <=50:
            f0 += v
        else:
            g0 += v

    values = [a0,b0,c0,d0,e0,f0,g0]
    #print(values)

    #设置显示中文，
    plt.rcParams['font.sans-serif'] = ['SimHei'] #字体5
    plt.rcParams['axes.unicode_minus'] = False   
    
    #设置颜色
    cols = ['r', 'y', 'b', 'g', 'c', 'm', 'k']
    plt.pie(values,
        #饼状图上的文字
        labels=key,
        #颜色设置
        colors=cols,
        #定义饼状图的起始角度为90°
        startangle=90,
        #为饼状图添加阴影，False无阴影
        shadow= True,
        #将某个切片拉出来，为0不拉出来
        explode=(0,0,0,0,0,0,0),
        #将百分比添加到对应的饼状图上
        autopct='%1.2f%%')

    plt.title('薪资分布')
    plt.show()

def workyear_bar():
    #创建字典，每个学历的统计数 count(x) 统计列表中x的次数，
    work_year_table = {}
    for i in work_year:
        work_year_table[i] = work_year.count(i)
    #print(work_year_table)

    #将字典中键、值分别于列表中，作为图标的数值参数
    keys = []
    values = []
        
    #遍历键值对并存入列表
    for k, v in work_year_table.items(): #将字典转化为可迭代对象
        keys.append(k)
        values.append(v)
    print(keys, values)
    
    #设置显示中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    #使用matplotlib.pyplot，创建条形图
    plt.bar(keys, values, width = 0.35, color = 'red')
    plt.xticks(range(len(keys)), keys)
    plt.title('工作经验')
    
    #在图上显示数值,plt.text()给直方图添加标签，第一个参数：标签值，第二个：y轴位置位置，第三个参数：未知，第四个参数：居中、左、右
    for x, y in enumerate(values):
        plt.text(x, y+5, '%s' % round(y,1), ha='center')

    plt.show()  

if __name__ == '__main__':
    get_message()
    #make_bar()
    make_pie()
    #workyear_bar()