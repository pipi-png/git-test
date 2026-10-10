from django.db import models


# 部门表：演示最基本的单表模型
class Department(models.Model):
    title = models.CharField(max_length=32, verbose_name="部门名称")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门"


# 角色表：演示单表模型 + 字符串方法
class Role(models.Model):
    title = models.CharField(max_length=32, verbose_name="角色名称")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"


# 用户信息表：演示外键关联（ForeignKey）、常用字段类型
class UserInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    password = models.CharField(max_length=64, verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    email = models.CharField(max_length=64, verbose_name="邮箱")
    # 外键关联部门（一对一可选），SET_NULL：部门删除后该字段置空
    department = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门"
    )
    # 外键关联角色
    role = models.ForeignKey(
        Role, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="角色"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"
