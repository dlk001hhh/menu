from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views
from myApp.views import RegisterView, UserActiveView, LoginView, \
    Base1View, BaseView, IndexView, \
    MenuView, DishView, \
    IngrePriceView, IngreShowView, IngreDescsView, IngreDetailsView,\
    HealthView, HealthArticleView, \
    CommunityView, \
    UserCreateView, UserCollectionView, UserCommentView, UserCartView, UserOderView, CartUpdateView, CartAddView, CartDeleteView


# app_name = 'myApp'

urlpatterns = [
    url('^login/$', LoginView.as_view(), name='login'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url('^user/active/(?P<token>.*)/$', UserActiveView.as_view(), name='userActive'),

    url('^base/$', BaseView.as_view(), name='base'),
    url('^base1/$', Base1View.as_view(), name='base1'),
    url('^index/$', IndexView.as_view(), name='index'),

    url('^menu/$', MenuView.as_view(), name='menu1'),
    url('^menu/(\w+)/$', MenuView.as_view(), name='menu2'),
    url('^menu/(\w+)/(\w+)/$', MenuView.as_view(), name='menu3'),
    url('^menu/(\w+)/(\w+)/(\d+)/$', MenuView.as_view(), name='menu4'),
    url('^dish/(\d+)/$', DishView.as_view(), name='dish'),

    url('^ingre/$', IngrePriceView.as_view(), name='ingre'),
    url('^ingre/price/$', IngrePriceView.as_view(), name='ingre_price'),
    url('^ingre/show/$', IngreShowView.as_view(), name='ingre_show'),
    url('^ingre/descs/$', IngreDescsView.as_view(), name='ingre_descs'),
    url('^ingre/details/$', IngreDetailsView.as_view(), name='ingre_details'),
    url('^ingre/price/(\w+)/$', IngrePriceView.as_view(), name='ingre_price2'),
    url('^ingre/show/(\w+)/$', IngreShowView.as_view(), name='ingre_show2'),
    url('^ingre/descs/(\w+)/$', IngreDescsView.as_view(), name='ingre_descs2'),
    url('^ingre/details/(\w+)/$', IngreDetailsView.as_view(), name='ingre_details2'),

    url('^health/$', HealthView.as_view(), name='health1'),
    url('^health/(\d+)/$', HealthView.as_view(), name='health2'),
    url('^health/(\d+)/(\d+)$', HealthView.as_view(), name='health3'),
    url('^health/article/(\d+)$', HealthArticleView.as_view(), name='health_article'),

    url('^community/$', CommunityView.as_view(), name='community'),

    url('^user/$', UserCreateView.as_view(), name='user'),
    url('^user/create/$', UserCreateView.as_view(), name='user_create'),
    url('^user/create/(\d+)/$', UserCreateView.as_view(), name='user_create2'),
    url('^user/collection/$', UserCollectionView.as_view(), name='user_collection'),
    url('^user/collection/(\d+)/$', UserCollectionView.as_view(), name='user_collection2'),
    url('^user/comment/$', UserCommentView.as_view(), name='user_comment'),
    url('^user/cart/$', UserCartView.as_view(), name='user_cart'),
    url('^user/order/$', UserOderView.as_view(), name='user_order'),
    url('^add/$', CartAddView.as_view(), name='cart_add'),
    url('^update/$', CartUpdateView.as_view(), name='cart_update'),
    url('^delete/$', CartDeleteView.as_view(), name='cart_delete'),
    # url('^addimg/$', views.add)
    # url('^collection/$', Collection.as_view(), name='collection'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # url('^uploadImg/$', views.uploadImg),
    # url('^showImg/$', views.showImg),