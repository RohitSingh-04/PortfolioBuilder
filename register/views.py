from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden, JsonResponse
from json import loads

# Create your views here.
def home(request):
    return render(request, 'index.html')

def newUser(request):
    if request.method == 'POST':
        data = request.POST
        if User.objects.filter(username = data['username']).exists():
            data = {i:data[i] for i in data if i != 'username'}
            return render(request, 'newRegistration.html', {'data': data, 'error':'invalid Username', 'hidden': 'false'})
        
        if User.objects.filter(email = data['email']).exists():
            data = {i:data[i] for i in data if i != 'email'}
            return render(request, 'newRegistration.html', {'data': data, 'error':'invalid Email', 'hidden': 'false'})

        User.objects.create_user(username=data['username'], first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password = data['password'])


        return redirect('/login/')
    return render(request, 'newRegistration.html', {'hidden': 'true'})

def UserExists(request):
    if request.method == 'POST':
        data = request.body
        data = loads(data)

        if User.objects.filter(username = data['username']).exists():
            return JsonResponse({"exist":True})
        else:
            return JsonResponse({"exist": False})
        
    return HttpResponseForbidden()
    

def createResume(request):
    ...
    
    