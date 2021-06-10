from django.conf.urls import url
from . import views

urlpatterns = [
    # 面包屑
    url(r'categories/(?P<pk>\d+)/$', views.CategoryView.as_view()),
    # 商品列表页
    url(r'categories/(?P<category_id>\d+)/skus/$', views.SKUListView.as_view()),

]