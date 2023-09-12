from django.shortcuts import render, redirect
from useradmin import models
from useradmin.utils.form import LoginForm


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 数据库校验用户名密码是否正确, 如果用户名密码有错误，则admin_object对象为空
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 主动添加错误
            # form.add_error("password", "用户名或者密码错误")
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})

        # 用户名和密码验证正确
        # 网站生成随机字符串；写道用户浏览器的cookie中；再写入到session中；
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        return redirect("/admin/list")
    return render(request, 'login.html', {"form": form})


def logout(request):
    """注销"""

    # 清除当前的session
    request.session.clear()
