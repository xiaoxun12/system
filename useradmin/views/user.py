from django.shortcuts import render, redirect
from useradmin import models
from useradmin.utils.pagination import Pagination
from useradmin.utils.form import UserModelForm


def user_list(request):
    """用户管理"""

    # 获取搜友用户列表
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """ 添加用户 """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    # 校验失败
    else:
        return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """编辑用户"""

    if request.method == "GET":
        # 更具ID去数据库获取要编辑的哪一行数据
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
