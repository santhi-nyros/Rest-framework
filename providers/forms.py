from django import forms
# from wtforms import SelectField, TextField, PasswordField, IntegerField,validators, DateField, TextAreaField
from django.core import validators

class LoginForm(forms.Form):
    error_css_class = "error"
    username =forms.CharField(max_length=25,required=True,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'username'}))
    password = forms.CharField(max_length=25,min_length=6,widget=forms.PasswordInput(attrs={'class': "form-control","placeholder":'Password'}))


class PackageForm(forms.Form):
    error_css_class = 'error'
    pack_name = forms.CharField(max_length=25,required=True,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'Pacakge name'}))
    location = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'Location'}))
    business_type = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class': "form-control","placeholder":'Business Type'}))


