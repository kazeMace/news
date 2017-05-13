from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form


def len_validator(request):
    if len(request) < 4:
        raise ValidationError('不能少于4个字')
    if len(request) > 200:
        raise ValidationError('不能超过200个字')


class CommentForm(forms.Form):
    # username = forms.CharField(max_length=100)
    comment = forms.CharField(
        max_length=500,
        widget=forms.Textarea(),
        error_messages={
        'required': '内容不能为空',
        },
        validators=[len_validator],
    )


class UserInfoForm(forms.Form):
    修改昵称 = forms.CharField(max_length=14)

    # 用户头像
    修改头像 = forms.ImageField()

    # 用户个性签名
    个性签名 = forms.CharField(max_length=250)

    # 用户生日
    生日 = forms.DateField()

    # 用户性别
    SEX_TAG = (
        ('男', '男'),
        ('女', '女'),

    )
    性别 = forms.ChoiceField(required=False, widget=forms.Select(), choices=SEX_TAG)

    #用户邮箱
    电子邮箱 = forms.EmailField(max_length=100)

    #用户所在地区
    所在地区 = forms.CharField(max_length=50)

    #毕业院校
    毕业院校 = forms.CharField(max_length=50)

    #职业
    职业 = forms.CharField(max_length=50)

    # 用户兴趣
    CHECKBOX_CHOICES = (
        ('国内', '国内'),
        ('国际', '国际'),
        ('社会', '社会'),
        ('军事', '军事'),
        ('体育', '体育'),
        ('科技', '科技'),
        ('财经', '财经'),
        ('搞笑', '搞笑'),
    )
    兴趣 = forms.MultipleChoiceField(
        required=False,
        choices=CHECKBOX_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
    )
class shijianform(forms.Form):
    data = forms.CharField()



