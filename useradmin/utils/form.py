from django import forms
from useradmin import models
from django.core.validators import ValidationError
from useradmin.utils.bootstrap import BootstrapModelForm
from useradmin.utils.encrypt import md5


class UserModelForm(BootstrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]

        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.TextInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        #     "account": forms.TextInput(attrs={"class": "form-control"}),
        #     "create_time": forms.DateTimeInput(attrs={"class": "form-control"}),
        #     "depart": forms.Select(attrs={"class": "form-control"}),
        #     "gender": forms.Select(attrs={"class": "form-control"}),
        # }


class PrettyModelForm(BootstrapModelForm):
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式错误")]
    # )

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # exclude = ["level"] 排除的字段
        fields = "__all__"  # 表示所有字段

        # widgets = {
        #     "mobile": forms.TextInput(attrs={"class": "form-control"}),
        #     "price": forms.TextInput(attrs={"class": "form-control"}),
        #     "level": forms.Select(attrs={"class": "form-control"}),
        #     "status": forms.Select(attrs={"class": "form-control"}),
        # }

    # 验证方式
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exits = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        elif exits:
            raise ValidationError("手机号已经存在")
        return txt_mobile


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        # render_value=True 表示密码错误后，重新输入时，密码内容不置空
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        return md5(self.cleaned_data.get("password"))

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


# 登录
class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True
    )

    # filter = ["username", "password"]

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

