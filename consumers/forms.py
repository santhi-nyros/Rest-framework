from django import forms
# from wtforms import SelectField, TextField, PasswordField, IntegerField,validators, DateField, TextAreaField
from django.core import validators
from consumers.models import Consumer_profile
from providers.models import Category

class ConsumerForm(forms.Form):
    error_css_class = 'error'
    username = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'User name'}))
    email =forms.EmailField(max_length=25,required=True,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'Email'}))
    password = forms.CharField(max_length=25,min_length=6,required=True,widget=forms.PasswordInput(attrs={'class': "form-control","placeholder":'Password'}))



class ConsumerProfileForm(forms.Form):
    error_css_class = 'error'
    categories = Category.objects.all()
    CATEGORY_CHOICES= ((category.id,category.category) for category in categories)

    first_name = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'First name'}))
    last_name = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'Last name'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': "form-control","placeholder":'Image'}))
    category =forms.ChoiceField(choices = CATEGORY_CHOICES, required=True,widget=forms.Select   (attrs={'class': "form-control","placeholder":'Category'}))
    location = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'Location'}))

