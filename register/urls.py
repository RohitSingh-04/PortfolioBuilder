from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),
    path('register/', views.newUser),
    path('usernameExist', views.UserExists),
    path('createResume/', views.createResume)

]
