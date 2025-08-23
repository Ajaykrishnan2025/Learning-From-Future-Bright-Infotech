from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import ContactForm, LoginForm,RegisterForm, ResetPasswordForm
import logging



from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from .forms import ForgotPasswordForm


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django import forms



# Create your views here.

# first part in django section creating a blog
def index(request):
    return render(request,'blog/index.html')



# def detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/detail.html', {'post': post})

def service(request):
    return render(request,'blog/service.html')


def contact(request):
    return render(request, 'blog/contact.html')

import logging  # Place this at the top of your views.py

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.set_password(form.cleaned_data ['password'])
            user.save()
            # print('Register Sucess !')
            messages.success(request, 'Registration Sucessfull. You can Log in ')
            return redirect("blog:login")

    else:
        form = RegisterForm()        
    return render(request, 'blog/register.html', {'form': form})


def contact_view(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if name and email:
            success_message = "✅ Thank you for contacting us! We'll get back to you soon."

    return render(request, 'blog/contact.html', {
        'success_message': success_message
    })

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        # login form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None :
                auth_login(request, user)
                print("Login SUCCESEE")
                return redirect("blog:contact") #redirect to dashboard
            
    return render(request, 'blog/login.html', {'form': form})

# def dashboard(request):
#     blog_tittle = "My Posts"
#     return render(request, 'blog/dashboard.html', {"blog_tittle": blog_tittle} )

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

from django.contrib.auth.models import User
from django.core.mail import send_mail

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            users = User.objects.filter(email=email)
            if not users.exists():
                messages.error(request, "⚠️ No account found with this email.")
                return render(request, 'blog/forgot_password.html', {'form': form})

            user = users.first()  # pick the first user if multiple exist

            # Generate reset token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain

            # Subject + email body
            subject = "Reset Your Password"
            message = render_to_string('blog/reset_password_email.html', {
                'domain': domain,
                'uid': uid,
                'token': token,
                'user': user,
            })

            # Send the reset email
            send_mail(
                subject,
                message,
                'noreply@gmail.com',  # change to your sender email
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "✅ Password reset email has been sent to your inbox.")
            return redirect("blog:login")

    return render(request, 'blog/forgot_password.html', {'form': form})

def reset_password(request, uidb64, token):
    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # ✅ Use field names from the form
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password != confirm_password:
                messages.error(request, "❌ Passwords do not match.")
                return render(request, 'blog/reset_password.html', {'form': form})

            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, "✅ Your password has been reset successfully!")
                return redirect('blog:login')
            else:
                messages.error(request, "❌ The password reset link is invalid.")

    return render(request, 'blog/reset_password.html', {'form': form})
