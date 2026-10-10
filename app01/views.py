import json
import urllib.request

from django.shortcuts import redirect, render

from . import models


def index(request):
    """首页：演示最简单的视图 + 重定向"""
    return redirect("/user/list/")


def login(request):
    """
    登录页：演示 请求对象(GET/POST)、表单提交、Session、重定向。
    访问 /login/ 输入账号密码，成功跳转用户信息管理页。
    """
    if request.method == "GET":
        return render(request, "app01/login.html", {"error": ""})

    name = request.POST.get("name")
    pwd = request.POST.get("password")
    user = models.UserInfo.objects.filter(name=name, password=pwd).first()
    if user:
        request.session["username"] = user.name
        return redirect("/user/list/")
    return render(request, "app01/login.html", {"error": "用户名或密码错误"})


def logout(request):
    """退出登录：清除 Session 并回到登录页"""
    request.session.flush()
    return redirect("/login/")


def user_list(request):
    """用户信息管理：演示 ORM 查询、模板 for 循环、if 判断、外键取值"""
    queryset = models.UserInfo.objects.all()
    return render(request, "app01/user_list.html", {"user_list": queryset})


def user_add(request):
    """添加用户：演示 POST 表单提交 + ORM 新增"""
    if request.method == "GET":
        departments = models.Department.objects.all()
        roles = models.Role.objects.all()
        return render(
            request,
            "app01/user_add.html",
            {"departments": departments, "roles": roles},
        )

    name = request.POST.get("name")
    pwd = request.POST.get("password")
    age = request.POST.get("age")
    email = request.POST.get("email")
    department_id = request.POST.get("department_id")
    role_id = request.POST.get("role_id")
    models.UserInfo.objects.create(
        name=name,
        password=pwd,
        age=int(age) if age else 0,
        email=email,
        department_id=int(department_id) if department_id else None,
        role_id=int(role_id) if role_id else None,
    )
    return redirect("/user/list/")


def user_delete(request):
    """删除用户：演示 GET 传参 + ORM 删除 + 重定向"""
    nid = request.GET.get("nid")
    if nid:
        models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def tpl(request):
    """模板语法演示页：变量渲染、for 循环、if/elif/else、字典取值"""
    name = "皮皮"
    roles = ["管理员", "普通用户", "访客"]
    user_dict = {"name": "小明", "age": 20}
    return render(
        request,
        "app01/tpl.html",
        {"name": name, "roles": roles, "user_dict": user_dict},
    )


def weather(request):
    """
    成都天气：演示外部 API 调用。
    使用免费接口 wttr.in（无需 key）；网络不可用时展示示例数据，保证页面可演示。
    """
    data = None
    error = None
    try:
        url = "https://wttr.in/Chengdu?format=j1&lang=zh"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        cur = payload["current_condition"][0]
        area = payload.get("nearest_area", [{}])[0]
        data = {
            "city": area.get("areaName", [{}])[0].get("value", "成都"),
            "temp": cur.get("temp_C"),
            "feels": cur.get("FeelsLikeC"),
            "humidity": cur.get("humidity"),
            "text": cur.get("lang_zh", [{}])[0].get(
                "value", cur.get("weatherDesc", [{}])[0].get("value", "")
            ),
            "wind": cur.get("windspeedKmph"),
            "updated": cur.get("observation_time"),
        }
    except Exception as exc:  # 网络不可用时使用示例数据
        data = {
            "city": "成都",
            "temp": "26",
            "feels": "27",
            "humidity": "58",
            "text": "多云（示例数据：外部 API 暂不可用）",
            "wind": "8",
            "updated": "本地示例",
        }
        error = str(exc)
    return render(request, "app01/weather.html", {"data": data, "error": error})
