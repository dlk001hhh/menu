from django.contrib import admin


from myApp.models import Dish, Skill, Taste, Degree, Time, Step,  Auxi, Main, Dish_Cate, Dish_Cate2, Ingre, Ingre_Cate, User, Menu, \
    CreateDish, Comment, Collection, Cart, Order, Feedback, Img, Article, Article_Cate, Community


class AuxiInfo(admin.TabularInline):
    model = Auxi
    extra = 4


class MainInfo(admin.TabularInline):
    model = Main
    extra = 4


class StepInfo(admin.TabularInline):
    model = Step
    extra = 6


class MenuInfo(admin.TabularInline):
    model = Menu
    extra = 4


class DishAdmin(admin.ModelAdmin):
    inlines = [AuxiInfo, MainInfo, StepInfo, MenuInfo]
    list_display = ['id', 'name', 'img', 'descs', 'details', 'user', 'skill', 'taste', 'degree', 'time', 'is_show']
    list_per_page = 10
    search_fields = ['name']
    list_filter = ['name']


class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10


class TasteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10


class DegreeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10


class TimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10


class StepAdmin(admin.ModelAdmin):
    list_display = ['id', 'textStep1', 'textStep2', 'imgStep', 'dish']
    list_per_page = 10


class MainAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number', 'dish']
    list_per_page = 10


class AuxiAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number', 'dish']
    list_per_page = 10


class Dish_Cate2Admin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10
    list_filter = ['name']
    search_fields = ['name']


class Dish_CateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dish_cate2']
    list_per_page = 10
    list_filter = ['name']
    search_fields = ['name']


class Ingre_CateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10
    list_filter = ['name']
    search_fields = ['name']


class IngreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img', 'descs', 'details', 'price', 'cate', 'is_show']
    list_per_page = 10
    list_filter = ['name']
    search_fields = ['name']


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img', 'email', 'password', 'addTime']
    list_per_page = 10
    search_fields = ['name']
    list_filter = ['name']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'img', 'details', 'is_show']
    list_per_page = 10
    search_fields = ['title']
    list_filter = ['title']


class Article_CateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img']
    list_per_page = 10
    search_fields = ['name']
    list_filter = ['name']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'dish_cate', 'dish']
    list_per_page = 10


class CreateDishAdmin(admin.ModelAdmin):
    list_display = ['id', 'ingre', 'dish']
    list_per_page = 10


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish']
    list_per_page = 10


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish', 'comment']
    list_per_page = 10


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ingre']
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ingre', 'count', 'amount']
    list_per_page = 10


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ingre']
    list_per_page = 10


class CommunityAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish']
    list_per_page = 10


class ImgAdmin(admin.ModelAdmin):
    list_display = ['id', 'img_url']


admin.site.register(Dish, DishAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Taste, TasteAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Main, MainAdmin)
admin.site.register(Auxi, AuxiAdmin)
admin.site.register(Dish_Cate, Dish_CateAdmin)
admin.site.register(Dish_Cate2, Dish_Cate2Admin)

admin.site.register(Ingre, IngreAdmin)
admin.site.register(Ingre_Cate, Ingre_CateAdmin)

admin.site.register(User, UserAdmin)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Article_Cate, Article_CateAdmin)


admin.site.register(Menu, MenuAdmin)
admin.site.register(CreateDish, CreateDishAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Community, CommunityAdmin)


# admin.site.register(Img, ImgAdmin)