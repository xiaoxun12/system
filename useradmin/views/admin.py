from django.shortcuts import render, redirect
from useradmin import models
from useradmin.utils.pagination import Pagination
from useradmin.utils.form import AdminModelForm


def admin_list(request):
    """管理员列表"""

    #  检查用户是否已经登录，已经登录，继续走下去，未登录，就跳转回登录页面
    # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。如果是登录的，session有值
    # info = request.session.get("info")
    # if info:
    #     return redirect('/login')

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    # queryset = models.Admin.objects.all()

    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    """添加管理员"""
    if request.method == "GET":
        form = AdminModelForm
        return render(request, 'change.html', {"form": form, "title": "新建管理员"})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form": form, "title": "新建管理员"})


def admin_edit(request, nid):
    """添加管理员"""

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list')
    title = "编辑管理员"
    if request.method == "GET":
        form = AdminModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {"from": form, "title": title})


def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list')
