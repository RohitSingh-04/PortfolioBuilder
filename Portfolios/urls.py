from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home),
    path('login/', views.login_fx),
    path('logout/', views.logout_fx),
    path('documents/', views.fetch_docs),
    path('myresume/', views.fetch_resume),
    path('myportfs/', views.fetch_portfolios),
    path('show/<int:id>/', views.show_resume),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete)
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)