from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import BotInventory, Event
from bots.models import Bot
from flatpickr import DatePickerInput, DateTimePickerInput
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField(label='loginemail', widget=forms.TextInput(attrs={'class':'form-control', 'id':'loginemail'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password', 'placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)  # 验证用户名密码是否在数据库中
        if user is None:
            raise forms.ValidationError('用户名或密码错误！')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, min_length=3, widget=forms.TextInput(attrs={'class':'form-control', 'id':'username', 'placeholder':'请输入用户名'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'id':'email', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='再输入一次密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'double', 'placeholder':'再输入一次密码'}))

    
    # 验证用户名
    def clean_username(self):
        username = self.cleaned_data['username']
        # 用户名不能重复
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在！")
        return username
    # 验证邮箱
    def clean_email(self):
        email = self.cleaned_data['email']
        # 用户名不能重复
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在！")
        return email
    # 验证密码两遍是否一致
    def clean_password(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        # 用户名不能重复
        if password != password_again:
            raise forms.ValidationError("两次输入密码不一致！")
        return password

class TimezoneForm(forms.Form):  
    SELVALUE = (
        ('GMT+8','GMT+8(Asia)'),
        ('GMT-4','GMT-4(North America)'),
        ('GMT+1','GMT+1(Europe)')
    )
    timezone = forms.ChoiceField(widget=forms.Select(),choices=SELVALUE,initial=SELVALUE[0])

class RequestVerifyForm(forms.Form):
    SELVALUE = (
        ('Dashe','Dashe'),
        ('Balko','Balko'),
    )
    bot = forms.ChoiceField(label='Bot',choices=SELVALUE,initial=SELVALUE[0])
    key = forms.CharField(label='Key',max_length=200,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Key'}))
    nickname = forms.CharField(label='Nickname',max_length=200,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Set Key Nickname'}))

class ChangeNicknameForm(forms.Form):
    nickname = forms.CharField(label='Nickname',max_length=200,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Set Key Nickname'}))

class GeneralListingForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'start_date', 'end_date',
        ]
        widgets = {
            'start_date':     DatePickerInput().start_of('event active days'),
            'end_date':       DatePickerInput().end_of('event active days'),
        }

class CustomListingForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'start_datetime', 'end_datetime',
        ]
        widgets = {
            'start_datetime': DateTimePickerInput().start_of('event datetime'),
            'end_datetime':   DateTimePickerInput().end_of('event datetime')
        }