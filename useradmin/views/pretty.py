from django.shortcuts import render, redirect
from useradmin import models
from useradmin.utils.pagination import Pagination
from useradmin.utils.form import PrettyModelForm


# 靓号
def pretty_list(request):
    """靓号列表"""

    data_dict = {}
    select_data = request.GET.get("q", "")
    if select_data:
        data_dict["mobile__contains"] = select_data
    queryset = models.PrettyNum.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "select_data": select_data,
        "page_string": page_object.html()
    }
    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """添加靓号"""

    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    else:
        return render(request, 'pretty_add.html', {"form": form})


def pretty_edit(request, nid):
    """编辑靓号"""
    if request.method == "GET":
        row_object = models.PrettyNum.objects.filter(id=nid).first()
        form = PrettyModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})

    row_object = models.PrettyNum.objects.filter(id=nid).first()
    form = PrettyModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    else:
        return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list')
