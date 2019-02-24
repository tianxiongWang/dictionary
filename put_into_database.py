import pymysql
import sys
import re

db = pymysql.connect('localhost','root','931225','dict');
cursor = db.cursor()

# 仅用来测试游标对象建立是否有误	
# data = cursor.fetchall()
# print(data)

try:
	f = open('dict.txt')
except Exception as e:
	sys.exit(e)
else:
	for line in f:
		data = re.search(r'(\w+\b)\s+(.*)',line)
		word = data.group(1)
		mean = data.group(2)
		sql = '''insert into dictionary values(%s, %s)'''
		try:
			cursor.execute(sql, [word, mean])
			db.commit()
		except Exception as e:
			db.rollback()
			print(e)
print('数据导入完成!')
cursor.close()
db.close()