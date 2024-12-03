from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from register.models import UserResumeDetails
from django.http import HttpResponseBadRequest, JsonResponse
from register.models import *
 

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
    # to add logic for all the documents

def fetch_resume(request):
    
    resultSet = UserResumeDetails.objects.filter(user = request.user).all()

    return render(request, 'listdocs.html', {"data_type": "Resumes", "show_resume": True, "show_portfolio":False, "resultset":resultSet})

def fetch_portfolios(request):
    return render(request, 'listdocs.html', {"data_type": "Portfolios", "show_resume": False, "show_portfolio":True})

def show_resume(request, id):

    if request.method == "GET":

        userdetail = UserResumeDetails.objects.filter(id = id).first()
        if userdetail.is_global or userdetail.user == request.user:

            ##for template 1
            if userdetail.template.id == 1:
                if userdetail:
                    return render(request, 'template1.html', {'userdetail': userdetail})
            if userdetail.template.id == 2:
                if userdetail:
                    return render(request, 'template3.html', {'userdetail': userdetail})
                
        else:
            #not authorized
            ...
            
    else:
        return HttpResponseBadRequest()