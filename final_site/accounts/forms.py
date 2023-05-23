from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'رمز را وارد کنید',
        'class':'form-control',
    }))   
    confirm_password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'تکرار رمز',
        
    }))   
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
        
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'نام خود را وارد کنید'
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی خود را وارد کنید'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'شماره تلفن خود را وارد کنید'
        self.fields['email'].widget.attrs['placeholder'] = 'ایمیل خود را وارد کنید'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'