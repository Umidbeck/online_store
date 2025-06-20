from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from .models import UserProfile
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.db import IntegrityError


class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}!")
            return redirect('profile')
        messages.error(request, "Email yoki parol noto'g'ri.")
        return render(request, 'accounts/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f"Ro'yxatdan o'tdingiz, {user.first_name}!")
                return redirect('profile')
            except IntegrityError:
                messages.error(request, "Bu email yoki username allaqachon ro'yxatdan o'tgan.")
                return render(request, 'accounts/register.html', {'form': form})
        messages.error(request, "Ro'yxatdan o'tishda xato yuz berdi. Iltimos, ma'lumotlarni tekshiring.")
        return render(request, 'accounts/register.html', {'form': form})


class PasswordResetView(DjangoPasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form, 'user': request.user})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil ma'lumotlari yangilandi.")
            return redirect('profile')
        messages.error(request, "Ma'lumotlarni yangilashda xato yuz berdi.")
        return render(request, 'accounts/profile.html', {'form': form, 'user': request.user})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Siz tizimdan chiqdingiz.")
        return redirect('login')
