from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from .models import User


class LoginView(View):
    """Вход в систему"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_full_name()}!')
                return redirect('accounts:dashboard')
        messages.error(request, 'Неверный логин или пароль')
        return render(request, 'accounts/login.html', {'form': form})


class RegisterView(View):
    """Регистрация нового пользователя"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'  # По умолчанию новый пользователь - студент
            user.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Профиль пользователя"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    """Главная панель (перенаправление в зависимости от роли)"""
    user = request.user
    
    if user.is_admin() or user.is_superuser:
        return render(request, 'dashboard_admin.html')
    elif user.is_teacher():
        return render(request, 'dashboard_teacher.html')
    else:  # student
        return render(request, 'dashboard_student.html')
