import requests
from lxml import etree
from time import sleep
import pymysql
import os


url = 'https://home.meishichina.com/recipe-445089.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
response = requests.get(url, headers=headers)
print(response.status_code)
response.encoding = 'utf-8'
html = etree.HTML(response.text)
list = []

main_list2 = []
print(html.xpath('/html/body/div[5]/div/div[1]/div[2]/div/fieldset[1]/div/ul/li'))
for main in html.xpath('/html/body/div[5]/div/div[1]/div[2]/div/fieldset[1]/div/ul/li'):
    main_list1 = []

    main_text = main.xpath('./span[1]//b/text()')[0]
    print(main_text)
    main_number = main.xpath('./span[2]/text()')[0]
    print(main_number)
    main_list1.append(main_text)
    main_list1.append(main_number)

    main_list2.append(main_list1)
    print(main_list2)
list.append(main_list2)
print(list)





# db = pymysql.connect('localhost', 'root', 'lk078622', 'cate2')
# cursor = db.cursor()
#
#
# sql = '''
#     insert ignore into demo (text11) values ("%s")
# ''' %('drgergshthrthstr')
# cursor.execute(sql)

# db.commit()
# db.close()


