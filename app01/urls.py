from django.urls import path

from app01 import views

urlpatterns = [
    # 首页：直接重定向到用户信息管理
    path("", views.index),
    # 登录页：演示请求对象 / 表单 / Session / 重定向
    path("login/", views.login),
    path("logout/", views.logout),
    # 用户信息管理：ORM 增删查
    path("user/list/", views.user_list),
    path("user/add/", views.user_add),
    path("user/delete/", views.user_delete),
    # 模板语法演示页
    path("tpl/", views.tpl),
    # 成都天气：外部 API 调用演示
    path("weather/", views.weather),
]
