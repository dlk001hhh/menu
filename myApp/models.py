from django.db import models


# Create your models here.


from django.db.models.fields.files import ImageFieldFile
import time


# 菜品表
class Dish(models.Model):
    name = models.CharField(u'名字', max_length=25)
    img = models.ImageField(u'图片', upload_to='dish')
    descs = models.TextField(u'描述', null=True)
    details = models.TextField(u'小窍门', null=True)
    addTime = models.DateField(default='2019-02-26')
    number = models.IntegerField(u'收藏数', null=True, default=0)
    is_show = models.BooleanField(default=False)

    user = models.ForeignKey('User', default=1, on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', default=1, on_delete=models.CASCADE)
    taste = models.ForeignKey('Taste', default=1, on_delete=models.CASCADE)
    degree = models.ForeignKey('Degree', default=1, on_delete=models.CASCADE)
    time = models.ForeignKey('Time', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dish'
        unique_together = ("name", "img")


# 菜品_工艺表
class Skill(models.Model):
    name = models.CharField(u'工艺名', max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dish_skill'


# 菜品_口味表
class Taste(models.Model):
    name = models.CharField(u'口味名', max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dish_taste'


# 菜品_时间表
class Time(models.Model):
    name = models.CharField(u'所需时间', max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dish_time'


# 菜品_难度
class Degree(models.Model):
    name = models.CharField(u'难度', max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dish_degree'


# 菜品_步骤表
class Step(models.Model):
    textStep1 = models.CharField(u'步骤序号', max_length=5, default=1)
    textStep2 = models.TextField(u'步骤内容')
    imgStep = models.ImageField(u'步骤图片', upload_to='dishStep')
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'dish_Step'
        # unique_together = ("textStep1", "imgStep")


# 菜品_主料表
class Main(models.Model):
    name = models.CharField(max_length=10, default="主料名")
    number = models.CharField(max_length=10)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'dish_main'


# 菜品_辅料表
class Auxi(models.Model):
    name = models.CharField(max_length=10, default="辅料名")
    number = models.CharField(max_length=10)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'dish_auxi'


# 菜品_一级分类表
class Dish_Cate(models.Model):
    name = models.CharField(u'分类名', max_length=10)
    dish_cate2 = models.ForeignKey('Dish_Cate2', on_delete=models.CASCADE)
    cate_dish = models.ManyToManyField(Dish, through='Menu', related_name='cateDish')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dish_cate'


# 菜品_二级分类表
class Dish_Cate2(models.Model):
    name = models.CharField(u'分类名', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Dish_Cate2'


# 食材表
class Ingre(models.Model):
    name = models.CharField(u'食材名', max_length=10, unique=True)
    img = models.ImageField(u'图片', upload_to='ingre')
    descs = models.TextField(u'选购技巧', null=True)
    details = models.TextField(u'营养功效', null=True)
    price = models.IntegerField(u'价格', null=True, default=30)
    is_show = models.BooleanField(default=False)
    create = models.ManyToManyField(Dish, through='CreateDish', related_name='createDish')
    cate = models.ForeignKey('Ingre_Cate', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Ingre'


# 食材_分类表
class Ingre_Cate(models.Model):
    name = models.CharField(u'分类名', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Ingre_Cate'


# 用户表
class User(models.Model):
    name = models.CharField(u'姓名', max_length=25, unique=True)
    img = models.ImageField(u'头像', default="img/user.png", upload_to='img')
    email = models.EmailField(u'邮箱', max_length=25, unique=True)
    password = models.CharField(u'密码', max_length=25)
    address = models.CharField(u'地址', default='暂无地址', max_length=50)
    addTime = models.DateTimeField(u'创建时间', auto_now_add=True)
    is_active = models.IntegerField(u'是否激活', default=0)

    user_collection = models.ManyToManyField(Dish, through='Collection',  related_name='userCollection')
    user_comment = models.ManyToManyField(Dish, through='Comment', related_name='userComment')
    user_cart = models.ManyToManyField(Ingre, through='Cart', related_name='userCart')
    user_oder = models.ManyToManyField(Ingre, through='Order', related_name='userOrder')
    user_feedback = models.ManyToManyField(Ingre, through='Feedback', related_name='userFeedback')
    user_Community = models.ManyToManyField(Dish, through='Community',  related_name='userCommunity')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'user'


#文章表
class Article(models.Model):
    title = models.CharField(u'文章名', max_length=50)
    img = models.ImageField(u'插图', upload_to='article')
    details = models.TextField(u'正文')
    is_show = models.BooleanField(default=False)
    article_cate = models.ForeignKey('Article_Cate', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'


# 文章分类表
class Article_Cate(models.Model):
    name = models.CharField(u'文章分类', max_length=10)
    img = models.ImageField(u'插图', default='articleCate/1.png', upload_to='articleCate')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'article_cate'


# @1菜品一级分类与菜品对应表
class Menu(models.Model):
    dish_cate = models.ForeignKey('Dish_Cate', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'Menu'
        unique_together = ("dish_cate", "dish")


# @2原料与菜品对应表
class CreateDish(models.Model):
    ingre = models.ForeignKey('ingre', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'createdish'


# @3收藏表（用户与菜品）
class Collection(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'collection'


# @4菜品评论表（用户与菜品）
class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=255)
    addTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'


# @5购物车表（用户与食材）
class Cart(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ingre = models.ForeignKey('Ingre', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart'


# @6订单表（用户与食材）
class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ingre = models.ForeignKey('Ingre', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    class Meta:
        db_table = 'order'


# @7用户反馈表（用户与食材）
class Feedback(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ingre = models.ForeignKey('Ingre', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)

    class Meta:
        db_table = 'feedback'


# @8美食社区表（用户与菜品）
class Community(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'community'


# 图片试验表
class Img(models.Model):
    img_url = models.ImageField(upload_to='img', max_length=255)


class demo(models.Model):
    text11 = models.TextField()
    addTime = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'demo'





