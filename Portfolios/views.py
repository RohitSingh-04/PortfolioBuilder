from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'home.html')

def login_fx(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {"error": "Username or Password is Incorrect!"})
            
    return render(request, 'login.html', {"hidden": "true"})

def logout_fx(request):
    logout(request)
    return redirect('/login/')

def fetch_docs(request):

    return render(request, 'listdocs.html', {"data_type": "Documents", "show_resume": True, "show_portfolio":True})

def fetch_resume(request):
    return render(request, 'listdocs.html', {"data_type": "Resumes", "show_resume": True, "show_portfolio":False})

def fetch_portfolios(request):
    return render(request, 'listdocs.html', {"data_type": "Portfolios", "show_resume": False, "show_portfolio":True})