# mysite — Django 学习项目

一个用于学习 **Python Web 开发 / Django 框架 / ORM / 模板语法 / Git** 的入门级实战项目。

本项目以「用户信息管理」为主线，逐步覆盖了 Django 的 URL 路由、视图函数、模板渲染、模板语法、ORM 增删改查、静态资源、请求对象 (GET/POST)、外部 API 调用、登录表单与重定向等核心知识点，可作为从零学习 Django 的随堂练习代码。

- 远程仓库主页：https://github.com/pipi-png/git-test
- 克隆地址（SSH）：`git@github.com:pipi-png/git-test.git`

---

## 目录

1. [项目简介](#1-项目简介)
2. [技术栈与环境](#2-技术栈与环境)
3. [项目结构](#3-项目结构)
4. [功能模块与页面一览](#4-功能模块与页面一览)
5. [URL 路由表](#5-url-路由表)
6. [数据模型 (Model)](#6-数据模型-model)
7. [环境准备与运行](#7-环境准备与运行)
8. [页面使用说明](#8-页面使用说明)
9. [关键知识点注释](#9-关键知识点注释)
10. [Git 使用](#10-git-使用)
11. [常见问题排查](#11-常见问题排查)
12. [部署与安全提醒](#12-部署与安全提醒)

---

## 1. 项目简介

`mysite` 是一个 Django 5.2 项目，内含一个业务应用 `app01`。项目围绕用户数据 (UserInfo) 的展示、添加、删除等操作展开，同时演示了 Django 的各类基础能力：

- **模板语法**：变量渲染、for 循环、if/elif/else 判断、字典取值等 (tpl.html)；
- **ORM 增删改查**：用户列表查询、表单添加、链接删除 (UserInfo / Department / Role)；
- **请求对象**：GET 展示表单、POST 提交数据、QueryDict 取值；
- **登录与 Session**：登录表单校验、写入 Session、退出登录、页面重定向；
- **外部 API 调用**：调用免费天气接口 (wttr.in) 展示成都实时天气，网络不可用时自动降级为示例数据；
- **静态资源**：统一样式表 (style.css) 通过 `{% static %}` 加载。

## 2. 技术栈与环境

| 技术 | 版本 / 说明 |
|---|---|
| Python | 3.10（本项目使用 conda 环境 `lenet_5`） |
| Django | 5.2.18 |
| 数据库 | SQLite（Django 默认，开箱即用） |
| 前端 | HTML + CSS（原生模板，不引入前端框架） |
| 天气接口 | wttr.in（免费、无需 API key） |

### 依赖清单

见仓库根目录 `requirements.txt`：

```
django==5.2.18
```

## 3. 项目结构

```
git-test/                     # 仓库根目录（同时也是 Django 项目根）
├── mysite/                   # 项目配置
│   ├── settings.py           # 全局配置（应用注册、语言时区、数据库）
│   ├── urls.py               # 根路由：include 应用路由
│   ├── wsgi.py / asgi.py     # 部署入口
├── app01/                    # 业务应用
│   ├── models.py             # 数据模型：UserInfo / Department / Role
│   ├── views.py              # 视图函数：登录、用户管理、天气、模板演示
│   ├── urls.py               # 应用路由表
│   ├── migrations/           # 数据库迁移文件
│   ├── templates/app01/      # 模板：base / login / user_list / user_add / tpl / weather
│   └── static/app01/         # 静态资源：style.css
├── manage.py                 # Django 管理命令入口
├── requirements.txt          # 依赖清单
├── .gitignore                # Git 忽略规则
├── 1.txt / 2.txt / 3.txt     # 最初的 Git 命令练习文件
└── README.md
```

## 4. 功能模块与页面一览

| 模块 | 路由 | 说明 |
|---|---|---|
| 用户信息管理 | `/user/list/` | 展示全部用户（含部门、角色），支持删除 |
| 添加用户 | `/user/add/` | 表单提交新增用户（演示 POST + ORM 新增） |
| 登录 / 退出 | `/login/` `/logout/` | 账号密码校验、Session、重定向 |
| 成都天气 | `/weather/` | 外部 API 调用，展示实时天气 |
| 模板语法演示 | `/tpl/` | 变量 / 循环 / 判断 / 字典取值 / 过滤器 |
| 首页 | `/` | 自动重定向到用户信息管理 |

## 5. URL 路由表

`mysite/urls.py` → `app01/urls.py`：

| 路由 | 视图 | 方法 |
|---|---|---|
| `/` | `app01.views.index` | GET（重定向） |
| `/login/` | `app01.views.login` | GET / POST |
| `/logout/` | `app01.views.logout` | GET |
| `/user/list/` | `app01.views.user_list` | GET |
| `/user/add/` | `app01.views.user_add` | GET / POST |
| `/user/delete/` | `app01.views.user_delete` | GET（`?nid=` 传参） |
| `/tpl/` | `app01.views.tpl` | GET |
| `/weather/` | `app01.views.weather` | GET |
| `/admin/` | Django 自带后台 | — |

## 6. 数据模型 (Model)

| 模型 | 字段 | 说明 |
|---|---|---|
| Department（部门） | `title` | 单表模型，演示基础 CharField |
| Role（角色） | `title` | 单表模型 |
| UserInfo（用户信息） | `name` / `password` / `age` / `email` | 常用字段类型演示 |
| | `department`（外键） | ForeignKey → Department，`SET_NULL` |
| | `role`（外键） | ForeignKey → Role，`SET_NULL` |

## 7. 环境准备与运行

### 7.1 安装 Python 与依赖

```bash
# 建议使用 conda 环境（Python 3.10）
conda create -n django_env python=3.10 -y
conda activate django_env

# 安装依赖
pip install -r requirements.txt
```

### 7.2 配置数据库

项目默认使用 SQLite，无需额外配置。若需切换数据库，修改 `mysite/settings.py` 中的 `DATABASES` 配置。

### 7.3 生成迁移并运行

```bash
# 进入项目根目录
python manage.py makemigrations
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

浏览器访问 http://127.0.0.1:8000/ 即可。

### 7.4 插入演示数据（可选）

```bash
python manage.py shell -c "
from app01 import models as m
m.Department.objects.get_or_create(title='技术部')
m.Department.objects.get_or_create(title='产品部')
m.Department.objects.get_or_create(title='人事部')
m.Role.objects.get_or_create(title='管理员')
m.Role.objects.get_or_create(title='普通用户')
m.Role.objects.get_or_create(title='访客')
m.UserInfo.objects.get_or_create(name='admin', defaults={'password':'123456','age':25,'email':'admin@mysite.com','department_id':1,'role_id':1})
"
```

演示账号：`admin / 123456`

## 8. 页面使用说明

### 8.1 登录页 `/login/`

- GET：展示登录表单；
- POST：校验 `UserInfo` 表中用户名密码是否匹配，成功则写入 Session 并跳转 `/user/list/`，失败提示错误。

### 8.2 成都天气 `/weather/`

调用 `wttr.in/Chengdu?format=j1&lang=zh` 获取实时天气并解析 JSON 展示。若网络不可用，自动使用示例数据，页面仍可正常演示。

### 8.3 用户信息管理 `/user/list/`

- 列表展示全部用户及所属部门、角色（外键取值：`user.department.title`）；
- 每行提供「删除」链接（`/user/delete/?nid=xx`），删除后跳回列表。

### 8.4 模板语法演示 `/tpl/`

集中演示：`{{ 变量 }}` 渲染、`{% for %}` 循环、`{% if / elif / else %}` 判断、字典点语法与下标取值、过滤器（`default`、`length`）。

## 9. 关键知识点注释

| 知识点 | 位置 | 说明 |
|---|---|---|
| URL 路由与 include | `mysite/urls.py` | 项目根路由分发到应用 |
| 视图函数与请求对象 | `app01/views.py` | `request.method`、`request.POST.get()` |
| ORM 增删改查 | `app01/views.py` | `all()` / `filter()` / `create()` / `delete()` |
| 外键关联 | `app01/models.py` | `ForeignKey` + `on_delete=models.SET_NULL` |
| 模板语法 | `app01/templates/app01/tpl.html` | 变量 / 循环 / 判断 / 过滤器 |
| CSRF 防护 | 所有表单 | `{% csrf_token %}` 模板标签 |
| Session | `app01/views.py` | `request.session["username"]` / `flush()` |
| 静态资源 | `app01/static/app01/style.css` | `{% load static %}` + `{% static %}` |
| 外部 API | `app01/views.py` 的 `weather` | `urllib.request` + `json` 解析 |

## 10. Git 使用

本仓库同时用于 Git 练习（根目录的 1.txt / 2.txt / 3.txt 即命令练习产物）。常用命令：

```bash
# 克隆
git clone git@github.com:pipi-png/git-test.git
# 提交推送
git status
git add .
git commit -m "描述"
git push origin main
# 拉取
git pull origin main
```

## 11. 常见问题排查

| 问题 | 处理 |
|---|---|
| `ModuleNotFoundError: No module named 'django'` | 确认激活了安装过 Django 的环境，或 `pip install -r requirements.txt` |
| 页面 403 Forbidden | 表单缺少 `{% csrf_token %}`，或请求未携带 CSRF Cookie |
| 迁移失败 / 表已存在 | 删除 `app01/migrations` 下旧迁移与 `db.sqlite3`，重新 `makemigrations && migrate` |
| 天气页显示示例数据 | 外网不可达时正常降级；可稍后刷新或换用其他天气 API |
| 端口被占用 | `python manage.py runserver 127.0.0.1:8001` 换端口 |

## 12. 部署与安全提醒

- 项目当前为 **DEBUG 学习模式**（`DEBUG = True`），仅用于本地学习；
- 部署上线前必须：`DEBUG = False`、配置 `ALLOWED_HOSTS`、更换 `SECRET_KEY`；
- 生产环境请改用 PostgreSQL / MySQL，并使用真实密码存储方案（如 Django 自带 `make_password` / 第三方库）；
- 天气接口为公共免费接口，仅供演示，生产请申请稳定 API 并配置密钥（密钥不得提交到仓库）；
- 本仓库提交的 `SECRET_KEY` 仅用于学习演示，不可直接用于生产。
