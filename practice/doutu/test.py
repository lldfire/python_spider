import requests

url = 'http://img.doutula.com/production/uploads/image//2019/01/22/20190122123497_UKbQuA.gif!dta'
response = requests.get(url)
print(response.content)
with open('./1.jpg', 'ab') as f:
	f.write(response.content)