from typing import Any
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError



class RegisterForm(forms.Form):
    username=forms.CharField(label='Enter Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='Enter valid email',  widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='Enter password',  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    re_password=forms.CharField(label='Enter confirm password',  widget=forms.PasswordInput(attrs={'class':'form-control'}))
 
    def clean(self):
       cd= super().clean()
       p1=cd.get('password')
       p2=cd.get('re_password')
       if p1 and p2 and p1 != p2:
           raise ValidationError('passwords must match ')
       
    def clean_username(self):
        username=self.cleaned_data['username']
        user=User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username already exist! try another one')
        return username
    
    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exist! try another one')
        return email
    




class LoginForm(forms.Form):
    username=forms.CharField(label='Enter Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='Enter password',  widget=forms.PasswordInput(attrs={'class':'form-control'}))




