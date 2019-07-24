import requests
from lxml import etree
import pymysql
import time


def spider(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    list = []
    try:
        title = html.xpath('//h1[@class="title"]/a/text()')[0]
        list.append(title)
    except:
        print("爬取标题出错")
        return

    try:
        if len(html.xpath('//div[@class="measure"]/div/p/img')) != 0:
            img_url = html.xpath('//div[@class="measure"]/div/p/img/@src')[0]
            print(img_url)
            html_img = requests.get(img_url, headers=headers)
            path = 'D:\PythonWork\mypython\menu\media\\article\\'
            filename = img_url.split('/')[-1]
            fp = open(path + filename, 'wb')
            fp.write(html_img.content)
            fp.close()
            img = ('article/' + filename)
            list.append(img)
    except:
        print("爬取图片出错")
        return

    try:
        details = '\n'.join(html.xpath('//div[@class="measure"]/div/p/text()'))
        list.append(details)
    except:
        print("爬取文章出错")
        return

    return list




def spider2():
    list = []
    for i in range(1, 5):
        url = 'https://www.meishij.net/health.php?cid=20&sortby=update&page={}'.format(i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        try:
            link = html.xpath('//div[@class="listtyle1_list clearfix"]/div/div[1]/a/@href')
            list.extend(link)
        except:
            print("获取链接失败")
        # time.sleep(5)
    return list


# 连接到数据库
def connect(list):
    db = pymysql.connect('localhost', 'root', 'lk078622', 'cate2')
    cursor = db.cursor()

    try:
        sql = '''
            insert ignore into article (title, img, details, article_cate_id) 
            values ("%s", "%s", "%s", "%d")
        ''' % (list[0], list[1], list[2], 4)
        cursor.execute(sql)
        print("插入成功")
    except:
        print("插入错误")
        return

    db.commit()
    db.close()


if __name__ == '__main__':
    result = spider2()
    for url in result:
        result2 = spider(url)
        if not result2:
            continue
        connect(result2)