from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            send_otp_code(cd['phone_number'], random_code)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_registeration_info'] = {
                'phone_number':cd['phone_number'],
                'full_name':cd['full_name'],
                'email':cd['email'],
                'password':cd['password']
            }
            messages.success(request, 'we sent you a code.', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form':form})


class UserRegisterVerifyCode(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form':form})
    
    def post(self, request):
        user_session = request.session['user_registeration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['full_name'], 
                                         user_session['email'], user_session['password'])

                code_instance.delete()
                messages.success(request, 'you registered successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'code is wrong!', 'danger')
                return redirect('accounts:verify_code')  
        return redirect('home:home')
        





            