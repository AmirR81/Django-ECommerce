from django import forms 
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name')

    def clean_password2(self):
        psw1 = self.cleaned_data.get["password1"]
        psw2 = self.cleaned_data.get["password2"]
        if psw1 and psw2 and psw1 != psw2 :
            raise ValidationError('passwords must match!')
        return psw2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.changed_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="change your password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegisterForm(forms.Form):
    full_name = forms.CharField(label='full name', max_length=120)
    phone_number = forms.CharField(max_length=11)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists!')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number already exists!')
        return phone
    

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()