
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from ..home.models import UserLogs, AnalystLogs
from datetime import datetime


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                exdata = UserLogs()
                exdata.user_id = user.username
                exdata.event_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                exdata.event = "Login"

                exdata.save()
                if user.is_staff is True:
                    return redirect("/index")
                else:
                    exdata1 = AnalystLogs()
                    exdata1.user_id = user.username
                    exdata1.break_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    exdata1.break_code = 'Login'
                    exdata1.break_chk = '0'
                    exdata1.save()
                    return redirect("/break_add")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def logout_user(request):
    user = request.user
    logout(request)
    exdata = UserLogs()
    exdata.user_id = user.username
    exdata.event_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    exdata.event = "Logout"

    exdata.save()
    return redirect('login')
