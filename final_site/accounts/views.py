from django.shortcuts import render

def register(request):
    return render(request,'user/register.html')


def login(request):
    return render(request,'user/login.html')

def logout(request):
    return 