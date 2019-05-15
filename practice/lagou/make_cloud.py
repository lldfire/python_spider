#需要先创建一个词汇文件，并使用jieba统计
import jieba  #中文分词库
from wordcloud import WordCloud, ImageColorGenerator 
import numpy as np 
from matplotlib import pyplot as plt 
from PIL import Image 

with open('./duty.txt', 'r', encoding = 'gbk') as file:
    content = ''.join(file.readlines()) #逐行读取,并以''进行连接
    content = content.replace('岗位要求', '')
    content = content.replace('岗位职责', '')

content_after = '/'.join(jieba.cut(content)) #进行中文分词，全模式

#用于自定义背景
image = Image.open('./timg.png')
maskImage = np.array(image)

'''
font_path:设置字体路径，可在系统字体库中获取
background_color:设置背景颜色
max_words:词语最大尺寸
max_font_size:字体最大尺寸
width,height:云此图尺寸
mask:云词图背景
mode='RGBA'和colormap='pink' 统一文字颜色，可不加
'''
#默认背景图
wc = WordCloud(font_path="./SIMSUN.TTC",background_color="black",max_words=1000,max_font_size=100,width=2000,height=2500,mask=maskImage)
wc.generate(content_after) #生成云词图方法

#自定义背景图
'''
wc = WordCloud(font_path="./SIMSUN.TTC",max_words=1000,max_font_size=100,mask=maskImage,mode='RGBA',colormap='pink')
wc.generate(content_after) #生成云词图方法

image_color = ImageColorGenerator(maskImage)#从背景图片生成颜色值
wc.recolor(color_func=image_color)
'''

plt.figure("词云图") #指定所绘图名称
plt.imshow(wc)       # 以图片的形式显示词云
plt.axis("off")      #关闭图像坐标系
plt.show()

wc.to_file('./wordcloud1.png')  #保存云词图

#print(content_after)