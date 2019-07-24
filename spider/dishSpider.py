# -*- coding:utf-8 -*-
import pymysql
import requests
from lxml import etree
import time


def connect(list, num):
    db = pymysql.connect('localhost', 'root', 'lk078622', 'cate2')
    cursor = db.cursor()

    if len(list) == 0:
        print("菜品列表为空")
        return "no"

# ***********************************************************************************************
    try:
        sql_skill = '''
                    select id from dish_skill where name = '%s'
                ''' % list[5]
        try:
            cursor.execute(sql_skill)
        except:
            cursor.execute('''insert into dish_skill (name) values ("%s")''' % (list[5]))
            db.commit()
            cursor.execute(sql_skill)
        skill = cursor.fetchone()[0]

# ************************************************************************************

        sql_taste = '''
                        select id from dish_taste where name = '%s'
                    ''' % list[4]
        try:
            cursor.execute(sql_taste)
        except:
            cursor.execute('''insert into dish_taste (name) values ("%s")''' % (list[5]))
            db.commit()
            cursor.execute(sql_taste)
        taste = cursor.fetchone()[0]

    # ************************************************************************************

        sql_time = '''
                            select id from dish_time where name = '%s'
                        ''' % list[6]
        try:
            cursor.execute(sql_time)
        except:
            cursor.execute('''insert into dish_time (name) values ("%s")''' % (list[5]))
            db.commit()
            cursor.execute(sql_time)
        time2 = cursor.fetchone()[0]

    # ************************************************************************************

        sql_degree = '''
                                select id from dish_degree where name = '%s'
                            ''' % list[7]
        try:
            cursor.execute(sql_degree)
        except:
            cursor.execute('''insert into dish_degree (name) values ("%s")''' % (list[5]))
            db.commit()
            cursor.execute(sql_degree)
        degree = cursor.fetchone()[0]
    except:
        print("@1sql出问题，获取菜品工艺等外键")
        return "no"

# ************************************************************************************
#
    try:
        sql_dish = '''
                insert into dish (id, name, descs, details, img, skill_id, taste_id, time_id, degree_id, user_id, addTime) values ("%d", "%s", "%s", "%s", "%s", "%d", "%d", "%d", "%d", "%d", "%s")
            ''' % (num, list[0], list[2], list[3], list[1], skill, taste, time2, degree, 17, time.strftime('%Y-%m-%d', time.localtime(time.time())))
        try:
            cursor.execute(sql_dish)
            db.commit()
            print("往dish表中插入了菜品：{}".format(list[0]))
        except:
            print("往dish表中插入数据出错了")
            return "no"
    except:
        print("@2sql出问题, 向菜品表插入数据")
        return "no"
    # sql_dish = '''
    #                 insert into dish (id, name, descs, details, img, skill_id, taste_id, time_id, degree_id, user_id, addTime) values ("%d", "%s", "%s", "%s", "%s", "%d", "%d", "%d", "%d", "%d", "%s")
    #             ''' % (num, list[0], list[2], list[3], list[1], skill, taste, time2, degree, 13,
    #                    time.strftime('%Y-%m-%d', time.localtime(time.time())))
    #
    # cursor.execute(sql_dish)
    # db.commit()

# ******************************************************************************************************
    try:
        sql_dishId = '''
                select id from dish where name = '%s'
            ''' % list[0]
        try:
            cursor.execute(sql_dishId)
            dishId = cursor.fetchone()[0]
        except:
            print("没有找到dishid")
            return "no"

        for step in list[8]:

            textStep1 = step[0]
            textStep2 = step[1]
            imgStep = step[2]

            sql_step = '''
                    insert into dish_step (textStep1, textStep2, imgStep, dish_id) values ("%s", "%s", "%s", "%d")
                ''' % (textStep1, textStep2, imgStep, dishId)
            cursor.execute(sql_step)
    except:
        print("@3sql出问题, 向步骤表插入数据")
        return "no"

# ******************************************************************************************************************************************

    for main in list[9]:
        try:
            main_text = main[0]
            main_number = main[1]

            sql_ingreId1 = '''
                            select id from ingre where name = '%s'
                        ''' % main_text
            try:
                cursor.execute(sql_ingreId1)
                ingreId = cursor.fetchone()[0]
                cursor.execute('''insert into createdish (ingre_id, dish_id) values ("%d", "%d")''' % (ingreId, dishId))
                cursor.execute('''insert into dish_main (name, number, dish_id) values ("%s", "%s", "%d")''' % (main_text, main_number, dishId))
            except:
                cursor.execute('''insert into dish_main (name, number, dish_id) values ("%s", "%s", "%d")''' % (main_text, main_number, dishId))
        except:
            print("@4sql语法有问题，向主料表中插入数据失败")
            return "no"

# ******************************************************************************************************************************************

    for auxi in list[10]:
        try:
            auxi_text = auxi[0]
            auxi_number = auxi[1]

            sql_ingreId2 = '''
                            select id from ingre where name = '%s'
                        ''' % auxi_text
            try:
                cursor.execute(sql_ingreId2)
                ingreId = cursor.fetchone()[0]
                cursor.execute('''insert into createdish (ingre_id, dish_id) values ("%d", "%d")''' % (ingreId, dishId))
                cursor.execute('''insert into dish_auxi (name, number, dish_id) values ("%s", "%s", "%d")''' % (auxi_text, auxi_number, dishId))
            except:
                cursor.execute('''insert into dish_auxi (name, number, dish_id) values ("%s", "%s", "%d")''' % (auxi_text, auxi_number, dishId))
        except:
            print("@5sql语法有问题，向辅料表中插入数据失败")
            return "no"

# *************************************************************************************************************************************

    for classify in list[11]:
        try:
            sql_classify = '''
                                    select id from dish_cate where name = '%s'
                                ''' % classify
            try:
                cursor.execute(sql_classify)
                dish_cateId = cursor.fetchone()[0]
            except:
                continue

            sql_Menu = '''
                insert ignore into menu (dish_cate_id, dish_id) values ("%d", "%d")
            ''' % (dish_cateId, dishId)
            cursor.execute(sql_Menu)
        except:
            print("@6sql语法有问题，向菜品分类表中插入数据失败")
            return "no"

    db.commit()
    db.close()


# 爬取菜单分类下的菜品链接
def spiderLink():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    list = []
    for i in range(1, 10):
        try:
            # url = "https://home.meishichina.com/show-top-type-recipe-page-{}.html".format(i)
            # url = "https://home.meishichina.com/recipe/bingqilin/page/{}/".format(i)
            url = "https://home.meishichina.com/recipe/zaocan/page/{}/".format(i)
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            html = etree.HTML(response.text)
            link = html.xpath('//div[@class="ui_newlist_1 get_num"]/ul/li/div[2]/h2/a/@href')
            list.extend(link)
        except:
            print('爬取第{}页菜品链接失败'.format(i))
            continue
    return(list)


# 爬取具体菜品信息
def spiderMenu(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)

    list = []
    try:
        name = html.xpath('//*[@id="recipe_title"]/text()')[0]
        list.append(name)
    except:
        print('获取菜品名失败')
        return ''

    try:
        img_demo = html.xpath('//*[@id="recipe_De_imgBox"]/a/img/@src')[0]
        html_img = requests.get(img_demo, headers = headers)
        path = 'D:\PythonWork\mypython\menu\media\dish\\'
        filename = img_demo.split('/')[-2].split('?')[0]
        fp = open(path + filename, 'wb')
        fp.write(html_img.content)
        fp.close()
        img = ('dish/' + filename)
        list.append(img)
    except:
        print('获取菜品图片失败')
        return ''

    try:
        if len(html.xpath('//*[@id="block_txt1"]/text()')) == 0:
            desc = ''
        else:
            desc = html.xpath('//*[@id="block_txt1"]/text()')[0]
        list.append(desc)

        if len(html.xpath('//div[@class="recipeTip"]/text()')) == 0:
            details = ''
        else:
            details = ''.join(html.xpath('//div[@class="recipeTip"]/text()'))
        list.append(details)
    except:
        print("获取菜品介绍或小窍门失败")
        return ''

    try:
        other = html.xpath('//div[@class="recipeCategory_sub_R mt30 clear"]/ul/li/span[1]/a/text()')
        taste = other[0]
        list.append(taste)
        skill = other[1]
        list.append(skill)
        time = other[2]
        list.append(time)
        degree = other[3]
        list.append(degree)
    except:
        print("获取菜品技艺等失败")
        return ''

    try:
        step_list2 = []
        for step in html.xpath('//div[@class="recipeStep"]//ul/li'):
            step_list1 = []
            textStep1 = step.xpath('./div[2]/div/text()')[0]
            textStep2 = step.xpath('./div[2]/text()')[0]

            step_img = step.xpath('./div[1]/img/@src')[0]
            html_step_img = requests.get(step_img, headers=headers)
            path = 'D:\PythonWork\mypython\menu\media\dishStep\\'
            filename = step_img.split('/')[-2].split('?')[0]
            fp = open(path + filename, 'wb')
            fp.write(html_step_img.content)
            fp.close()
            imgStep = ('dishStep/' + filename)

            step_list1.append(textStep1)
            step_list1.append(textStep2)
            step_list1.append(imgStep)

            step_list2.append(step_list1)
        list.append(step_list2)
    except:
        print('获取步骤失败')
        return ''

    try:
        main_list2 = []
        for main in html.xpath('/html/body/div[5]/div/div[1]/div[2]/div/fieldset[1]/div/ul/li'):
            main_list1 = []

            main_text = main.xpath('./span[1]//b/text()')[0]
            main_number = main.xpath('./span[2]/text()')[0]
            main_list1.append(main_text)
            main_list1.append(main_number)

            main_list2.append(main_list1)
        list.append(main_list2)
    except:
        print('获取主料失败')
        return ''

    try:
        auxi_list2 = []
        for auxi in html.xpath('/html/body/div[5]/div/div[1]/div[2]/div/fieldset[2]/div/ul/li'):
            auxi_list1 = []

            auxi_text = auxi.xpath('./span[1]//b/text()')[0]
            auxi_number = auxi.xpath('./span[2]/text()')[0]
            auxi_list1.append(auxi_text)
            auxi_list1.append(auxi_number)

            auxi_list2.append(auxi_list1)
        list.append(auxi_list2)
    except:
        print('获取辅料失败')
        return ''

    try:
        dish_cate = html.xpath('//div[@class="recipeTip mt16"][3]/a/text()')
        list.append(dish_cate)
    except:
        print('获取菜品分类失败')
        return ''

    return(list)


if __name__ == '__main__':
    result1 = spiderLink()
    num = 570
    for link in result1:
        result2 = spiderMenu(link)
        result3 = connect(result2, num)
        if result3 == "no":
            num -= 1
        num += 1
        time.sleep(5)

