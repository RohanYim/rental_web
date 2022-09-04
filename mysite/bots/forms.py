from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from flatpickr import DatePickerInput

class SearchForm(forms.Form):
    start_date = forms.DateField(
        label="Start Date",
        widget=DatePickerInput(),
    )
    SELVALUE = (
        ('Any timezone','Any timezone'),
        ('GMT+8','GMT+8(Asia)'),
        ('GMT-4','GMT-4(North America)'),
        ('GMT+1','GMT+1(Europe)')
    )
    LEVELVALUE = (
        ('All levels','All levels'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5')
    )

    length = forms.IntegerField(min_value=1, max_value=365)
    user_timezone = forms.ChoiceField(widget=forms.Select(),choices=SELVALUE,initial=SELVALUE[0])
    user_level = forms.ChoiceField(widget=forms.Select(),choices=LEVELVALUE,initial=LEVELVALUE[0])
    user_refs = forms.IntegerField(min_value=0, max_value=10000)


    