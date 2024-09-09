from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),
    path('login/', views.login_fx),
    path('logout/', views.logout_fx),
    path('documents/', views.fetch_docs),
    path('myresume/', views.fetch_resume),
    path('myportfs/', views.fetch_portfolios)
]
