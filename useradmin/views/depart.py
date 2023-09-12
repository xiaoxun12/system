from django.shortcuts import render, redirect
from useradmin import models
from useradmin.utils.pagination import Pagination


def depart_list(request):
    """部门列表"""

    # 从数据库中获取所有部门列表
    # 列表的形式传递
    queryset = models.Department.objects.all()
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    """ 新建部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户通过POST提交过来的数据
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向到部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()

    # 重定向到部门列表
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 编辑部门 """
    if request.method == "GET":
        # 根据nid获取当前数据第一个值
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
