import requests
from lxml import etree
import pymysql
import time


def spider():
    url_list = [
        'https://www.meishichina.com/YuanLiao/category/rql/',
        'https://www.meishichina.com/YuanLiao/category/scl/',
        'https://www.meishichina.com/YuanLiao/category/shucailei/',
        'https://www.meishichina.com/YuanLiao/category/guopinlei/',
        'https://www.meishichina.com/YuanLiao/category/mmdr/',
        'https://www.meishichina.com/YuanLiao/category/tiaoweipinl/',
        'https://www.meishichina.com/YuanLiao/category/yaoshiqita/'
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    list_more = []
    for url in url_list:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        list = []
        for div in html.xpath('//div[@class="w clear"]/div/div'):
            link = div.xpath('./ul/li/a/@href')
            # if len(link) < 25:
            #     list.extend(link)
            # else:
            #     list.extend(link[0:25])
            list.extend(link)
        list_more.extend(list)
    return list_more


def spider2(url):
    list = []
    url1 = url + r'tiyan/'
    url2 = url + r'useful/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        img_url = html.xpath('//*[@id="category_pic"]/@data-src')[0].strip() + '?x-oss-process=style/c320'
        html_img = requests.get(img_url, headers=headers)
        path = 'D:\PythonWork\mypython\menu\media\\ingre\\'
        filename = img_url.split('/')[-2].split('?')[0]
        fp = open(path + filename, 'wb')
        fp.write(html_img.content)
        fp.close()
        img = 'ingre/' + filename
        name = ''.join(html.xpath('//*[@id="category_pic"]/@alt'))
    except:
        return list

    try:
        response = requests.get(url1, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        descs = '\n'.join(html.xpath('//div[@class="blog_message"]/p/text()'))
    except:
        descs = ''

    try:
        response = requests.get(url2, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        details = '\n'.join(html.xpath('//div[@class="category_usebox mt10 clear"]/div/p//text()')).split('。')[0]
    except:
        details = ''

    list.append(name)
    list.append(img)
    list.append(descs)
    list.append(details)
    print(list)
    return list


# 连接到数据库
def connect(info, num):
    db = pymysql.connect('localhost', 'root', 'lk078622', 'cate2')
    cursor = db.cursor()

    if len(info) == 0:
        num -= 1
        print("列表为空")
        return num

    try:
        sql_ingre = '''
                            insert ignore into ingre (id, name, img, descs, details, cate_id) values ("%d", "%s", "%s", "%s", "%s", "%d")
                        ''' % (num, info[0], info[1], info[2], info[3], 2)
        cursor.execute(sql_ingre)
    except:
        num -= 1
        print("没有插入：{}".format(info))
        return num

    db.commit()
    db.close()


if __name__ == '__main__':
    result = spider()
    num = 1
    for url in result:
        print(url)
        info = spider2(url)
        connect(info, num)
        num += 1
        time.sleep(8)
