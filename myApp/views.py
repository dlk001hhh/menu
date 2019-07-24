from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import re
import os
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Secret
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as UserRe
from utils.mixin import LoginRequireMixin
from django_redis import get_redis_connection
from alipay import AliPay


# Create your views here.
from django.urls import reverse


from myApp.models import Dish, Skill, Taste, Degree, Time, Step, Auxi, Main, Dish_Cate, Dish_Cate2, Ingre, Ingre_Cate, \
    User, Menu, \
    CreateDish, Comment, Collection, Cart, Order, Feedback, Article, Article_Cate, Community, Img


class RegisterView(View):
    def get(self, request):
        return render(request, 'myApp/register.html')

    def post(self, request):
        # 获取用户输入数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # 判断用户名是否存在
        try:
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'myApp/register.html', {'errmsg': "用户名重复"})

        # 判断邮箱是否被注册
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'myApp/register.html', {'errmsg': "该邮箱已被注册"})

        # 判断数据是否完整
        if not all([username, password, email]):
            return render(request, 'myApp/register.html', {'errmsg': "数据不完整"})

        # 判断邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'myApp/register.html', {'errmsg': "邮箱格式不正确"})

        # 用户注册信息存入数据库
        auth_user = UserRe.objects.create_user(username, email, password)
        user = User()
        user.name = auth_user.username
        user.email = auth_user.email
        user.password = password
        user.save()

        # 向用户发送邮件
        secret = Secret(settings.SECRET_KEY, 3000)
        info = {'id': user.id}
        token = secret.dumps(info)
        token = token.decode()

        subject = '美食网站欢迎信息'
        message = ''
        sender = settings.EMAIL_FROM
        receiver = [email]
        html_message = '<h1>欢迎您：%s</h1>请点击下面链接激活您的账户<br/>' \
                       '<a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
                       username, token, token)

        send_mail(subject, message, sender, receiver, html_message=html_message)

        return redirect(reverse('myApp:index'))


class UserActiveView(View):
    def get(self, request, token):
        secret = Secret(settings.SECRET_KEY, 3000)
        try:
            info = secret.loads(token)
            print(info)
            user_id = info['id']
            print(user_id)
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('myApp:login'))
        except SignatureExpired as e:
            return HttpResponse("激活链接已过期")


class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        context = {
            "username": username,
            "checked": checked
        }
        return render(request, 'myApp/login.html', context)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not all([username, password]):
            return render(request, 'myApp/login.html', {'errmsg': '数据不完整'})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                next_url = request.GET.get('next', reverse('myApp:index'))
                response = redirect(next_url)

                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(request, 'myApp/login.html', {'errmsg': '用户未激活'})
        else:
            return render(request, 'myApp/login.html', {'errmsg': '用户名或密码错误'})


class BaseView(View):
    def get(self, request):
        # print('***************************')
        # for dish_cate in dish_cate2:
        #     dish_cate = dish_cate.dish_cate_set.all()
        #     for dish in dish_cate:
        #         print(dish.name)
        dish_cate2 = Dish_Cate2.objects.all()
        ingre_cate = Ingre_Cate.objects.all()

        context = {
            'dish_cate2': dish_cate2,
            'ingre_cate': ingre_cate
        }

        return render(request, 'myApp/base.html', context)


class Base1View(View):
    def get(self, request):
        dish_cate2 = Dish_Cate2.objects.all()
        ingre_cate = Ingre_Cate.objects.all()

        context = {
            'dish_cate2': dish_cate2,
            'ingre_cate': ingre_cate
        }

        return render(request, 'myApp/base1.html', context)


class IndexView(View):
    def get(self, request):
        dish_cate2 = Dish_Cate2.objects.all()
        ingre_cate = Ingre_Cate.objects.all()

        dish = Dish.objects.filter(is_show=True)[0:4]
        ingre = Ingre.objects.filter(is_show=True)[0:4]
        article = Article.objects.filter(is_show=True)[0:4]

        slideshow = Dish.objects.filter(is_show=True)[4:9]

        context = {
            "dish": dish,
            "ingre": ingre,
            "article": article,
            "slideshow": slideshow,

            "dish_cate2": dish_cate2,
            "ingre_cate": ingre_cate
        }
        return render(request, 'myApp/index.html', context)


class MenuView(View):
    def get(self, request, cate2Name="家常菜谱", cateName= "家常菜", num=1):
        num = int(num)
        cate2All = Dish_Cate2.objects.all()

        cate2Get = Dish_Cate2.objects.get(name=cate2Name)
        cateAll = cate2Get.dish_cate_set.all()

        cateGet = Dish_Cate.objects.get(name=cateName)
        dishAll = cateGet.cate_dish.all()
        paginator = Paginator(dishAll, 16)
        page = paginator.page(num)
        numberPages = paginator.num_pages
        if numberPages < 5:
            page_list = range(1, numberPages+1)
        elif num < 3:
            page_list = range(1, 6)
        elif numberPages - num <= 2:
            page_list = range(numberPages - 2, numberPages + 1)
        else:
            page_list = range(num - 2, num + 3)

        return render(request, 'myApp/menu.html',
                      {"cate2All": cate2All, "cateAll": cateAll, "cate2Name": cate2Name, "cateName": cateName, "page": page,
                       "page_list": page_list, 'num': num, "paginator": paginator})


class DishView(View):
    def get(self, request, id=1):
        dish_id_list = []
        con = get_redis_connection('default')
        dict = con.hgetall('key_%s' % request.user.username)
        for key in dict:
            dish_id = int(key.decode())
            dish_id_list.append(dish_id)

        dish = Dish.objects.get(id=id)
        main = dish.main_set.all()
        auxi = dish.auxi_set.all()
        step = dish.step_set.all()
        commentAll = Comment.objects.filter(dish_id=id)
        user = User.objects.all()[0]

        context = {
            'dish': dish,
            'step': step,
            'main': main,
            'auxi': auxi,
            'commentAll': commentAll,
            'user': user,
            'dish_id_list': dish_id_list
        }
        return render(request, 'myApp/dish.html', context)

    def post(self, request, dish_id):
        # 从前端获取数据，用户id，菜品id，评论内容
        user = User.objects.get(name=request.user.username)
        dish_id = dish_id
        comment = request.POST.get('comment')
        print(user.id, dish_id, comment)

        # 校验数据

        # 将数据保存到数据库
        commentObj = Comment()
        commentObj.dish_id = dish_id
        commentObj.user_id = user.id
        commentObj.comment = comment
        commentObj.save()

        # 页面跳转
        return redirect(reverse('myApp:dish', args=(dish_id)))


class IngrePriceView(View):
    def get(self, request, name="猪肉"):
        ingre = Ingre.objects.get(name=name)
        context = {
            'ingre': ingre
        }

        return render(request, 'myApp/ingre_price.html', context)


class IngreShowView(View):
    def get(self, request, name="猪肉"):
        ingre = Ingre.objects.get(name=name)
        dish = ingre.create.all()
        context = {
            'ingre': ingre,
            'dish': dish
        }

        return render(request, 'myApp/ingre_show.html', context)


class IngreDescsView(View):
    def get(self, request, name="猪肉"):
        ingre = Ingre.objects.get(name=name)
        ingre_descs = Ingre.objects.get(id=1).descs.split('\n')
        context = {
            'ingre': ingre,
            'ingre_descs': ingre_descs
        }

        return render(request, 'myApp/ingre_descs.html', context)


class IngreDetailsView(View):
    def get(self, request, name="猪肉"):
        ingre = Ingre.objects.get(name=name)
        ingre_details = Ingre.objects.get(id=1).details.split('\n')
        context = {
            'ingre': ingre,
            'ingre_details': ingre_details
        }

        return render(request, 'myApp/ingre_details.html', context)


class HealthView(View):
    def get(self, request, id=1, num=1):
        article_cateAll = Article_Cate.objects.all()
        article_cate = Article_Cate.objects.get(id=id)
        article = article_cate.article_set.all()

        paginator = Paginator(article, 16)
        page = paginator.page(num)
        numberPages = paginator.num_pages
        if numberPages < 5:
            page_list = range(1, numberPages+1)
        elif num < 3:
            page_list = range(1, 6)
        elif numberPages - num <= 2:
            page_list = range(numberPages - 2, numberPages + 1)
        else:
            page_list = range(num - 2, num + 3)

        context = {
            "id": id,
            "article_cateAll": article_cateAll,
            "article_cate": article_cate,
            "paginator": paginator,
            "article": page,
            "page_list": page_list
        }

        return render(request, 'myApp/health.html', context)


class HealthArticleView(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)
        details = article.details.split('\n')

        context = {
            'article': article,
            'details': details
        }

        return render(request, 'myApp/health_article.html', context)


class CommunityView(View):
    def get(self, request):
        user1 = User.objects.get(name="dlk001hhh")
        dish1 = user1.community_set.all()

        user2 = User.objects.get(name="dlk002hhh")
        dish2 = user2.community_set.all()

        user3 = User.objects.get(name="dlk003hhh")
        dish3 = user3.community_set.all()

        user4 = User.objects.get(name="dlk004hhh")
        dish4 = user4.community_set.all()

        context = {
            'user1': user1,
            'dish1': dish1,
            'user2': user2,
            'dish2': dish2,
            'user3': user3,
            'dish3': dish3,
            'user4': user4,
            'dish4': dish4,
        }

        return render(request, 'myApp/community.html', context)


class UserCreateView(LoginRequireMixin, View):
    def get(self, request, num=1):
        num = int(num)
        user = User.objects.get(id=1)
        dishAll = user.dish_set.all()
        paginator = Paginator(dishAll, 16)
        page = paginator.page(num)
        numberPages = paginator.num_pages
        if numberPages < 5:
            page_list = range(1, numberPages+1)
        elif num < 3:
            page_list = range(1, 6)
        elif numberPages - num <= 2:
            page_list = range(numberPages - 2, numberPages + 1)
        else:
            page_list = range(num - 2, num + 3)
        context = {
            'user': user,
            'dish': page,
            'paginator': paginator,
            'page_list': page_list
        }
        return render(request, 'myApp/user_create.html', context)


class UserCollectionView(LoginRequireMixin, View):
    def get(self, request, num=1):
        num = int(num)
        status = 1
        user = User.objects.get(name=request.user.username)
        dishAll = []
        con = get_redis_connection('default')
        dict = con.hgetall('key_%s' % request.user.username)
        for key in dict:
            dish_id = int(key.decode())
            dish = Dish.objects.get(id=dish_id)
            dishAll.append(dish)
        paginator = Paginator(dishAll, 16)
        page = paginator.page(num)
        numberPages = paginator.num_pages
        if numberPages < 5:
            page_list = range(1, numberPages+1)
        elif num < 3:
            page_list = range(1, 6)
        elif numberPages - num <= 2:
            page_list = range(numberPages - 2, numberPages + 1)
        else:
            page_list = range(num - 2, num + 3)
        context = {
            'user': user,
            'dish': page,
            'page_list': page_list,
            'paginator': paginator,
            'status': status
        }
        return render(request, 'myApp/user_collection.html', context)

    def post(self, request):
        dish_id = str(request.POST.get('dish_id'))

        key = 'key_%s' % request.user.username
        con = get_redis_connection()
        bool = con.hget(key, dish_id)
        if bool:
            con.hdel(key, dish_id)
            return JsonResponse({'res': 0})
        else:
            con.hset(key, dish_id, 1)
            return JsonResponse({'res': 1})


class UserCommentView(LoginRequireMixin, View):
    def get(self, request):
        user = User.objects.get(name=request.user.username)
        commentAll = Comment.objects.filter(user_id=user.id)


        context = {
            'commentAll': commentAll,
            'user': user
        }
        return render(request, 'myApp/user_comment.html', context)


class UserCartView(LoginRequireMixin, View):
    def get(self, request):
        user = User.objects.get(name=request.user.username)
        con = get_redis_connection('default')
        ingre_dict = con.hgetall(user.name)

        ingres = []
        for ingre_id, count in ingre_dict.items():
            ingre = Ingre.objects.get(id=ingre_id)
            price = ingre.price
            amount = price * int(count)
            ingre.amount = amount
            ingre.count = int(count)
            ingres.append(ingre)

        context = {
            'user': user,
            'ingres': ingres
        }
        return render(request, 'myApp/user_cart.html', context)


class UserOderView(LoginRequireMixin, View):
    def get(self, request):
        user = User.objects.get(name=request.user.username)
        order = Order.objects.all()
        context = {
            'user': user,
            'order': order
        }
        return render(request, 'myApp/user_order.html', context)

    def post(self, request):
        ingre_id = '666'
        amount = request.POST.get('amount')
        float(eval(amount))

        if not request.user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})


        # 调用python SDK调用支付宝接口
        alipay = AliPay(
            appid="2016092600599760",
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, 'myApp/app_private_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'myApp/alipay_public_key.pem'),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认False
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=ingre_id,
            total_amount=amount,
            subject="美食网站",
            return_url=None,
            notify_url=None,  # 可选, 不填则使用默认notify url
        )
        url_pay = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        user = User.objects.get(name=request.user.username)

        con = get_redis_connection('default')
        dict = con.hgetall('dlk001hhh')
        for key, value in dict.items():
            order = Order()
            ingre = Ingre.objects.get(id=key.decode())
            order.user = user
            order.ingre = ingre
            order.count = value.decode()
            order.amount = ingre.price *int(value.decode())
            order.save()
        con.delete('dlk001hhh')

        return JsonResponse({'res': 2, 'url_pay': url_pay})


class CartAddView(View):
    def post(self, request):
        # 接收数据
        ingre_id = request.POST.get('ingre_id')
        count = request.POST.get('count')

        # 校验数据
        if not request.user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        if not all([ingre_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不全'})

        try:
            ingre = Ingre.objects.get(id=ingre_id)
        except:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 往redis存放数据
        con = get_redis_connection('default')
        cart_key = request.user.username
        cart_count = con.hget(cart_key, ingre_id)
        if cart_count:
            count = int(count)+int(cart_count)
        con.hset(cart_key, ingre_id, count)

        # 向页面返回数据
        return JsonResponse({'res': 3, 'message': '添加成功'})


class CartUpdateView(View):
    def post(self, request):
        # 接收数据
        ingre_id = request.POST.get('ingre_id')
        count = request.POST.get('count')

        # 校验数据
        if not request.user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        if not all([ingre_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不全'})

        try:
            ingre = Ingre.objects.get(id=ingre_id)
        except:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 往redis更新数据
        con = get_redis_connection('default')
        cart_key = request.user.username
        con.hset(cart_key, ingre_id, count)

        # 向页面返回数据
        return JsonResponse({'res': 3, 'message': '添加成功'})


class CartDeleteView(View):
    def post(self, request):
        # 接收数据
        ingre_id = request.POST.get('ingre_id')
        # count = request.POST.get('count')

        # 校验数据
        if not request.user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        if not all([ingre_id]):
            return JsonResponse({'res': 1, 'errmsg': '数据不全'})

        try:
            ingre = Ingre.objects.get(id=ingre_id)
        except:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 往redis更新数据
        con = get_redis_connection('default')
        cart_key = request.user.username

        if con.hget(cart_key, ingre_id):
            con.hdel(cart_key, ingre_id)

        # 向页面返回数据
        return JsonResponse({'res': 3, 'message': '删除成功'})



def add(request):
        articleCate = Article_Cate.objects.all()
        for i in articleCate:
            i.img = 'articleCate/%d.png' % i.id
            i.save()
        return HttpResponse('1111')



# class Collection(View):
#     def post(self, request):
#         dish_id = request.POST.get('dish_id')
#
#         key = 'key_%s' % request.user.username
#         con = get_redis_connection()
#         bool = con.hget(key, dish_id)
#         print(bool, type(bool))
#         if bool:
#             con.hset(key, dish_id, 0)
#             return JsonResponse({'res': 0})
#         else:
#             con.hset(key, dish_id, 1)
#             return JsonResponse({'res': 1})


def uploadImg(request):  # 图片上传函数
    if request.method == 'POST':
        img = Img(img_url=request.FILES.get('img'))
        img.save()
    return render(request, 'myApp/uploadImg.html')
#
#
# def showImg(request):
#     imgs = Img.objects.all()  # 从数据库中取出所有的图片路径
#     context = {
#         'imgs': imgs
#     }
#     return render(request, 'myApp/showImg.html', context)

# class UserView(LoginRequireMixin, View):
#     def get(self, request):
#         print(request.user.is_authenticated)
#         print(request.user.username)
#
#         num = 1
#         user = User.objects.get(name=request.user.username)
#         dishAll = user.dish_set.all()
#         paginator = Paginator(dishAll, 16)
#         page = paginator.page(num)
#         numberPages = paginator.num_pages
#         if numberPages < 5:
#             page_list = range(1, numberPages)
#         elif num < 3:
#             page_list = range(1, 6)
#         elif numberPages - num <= 2:
#             page_list = range(numberPages - 2, numberPages + 1)
#         else:
#             page_list = range(num - 2, num + 3)
#         context = {
#             'user': user,
#             'dish': page,
#             'page_list': page_list
#         }
#         return render(request, 'myApp/user.html', context)


