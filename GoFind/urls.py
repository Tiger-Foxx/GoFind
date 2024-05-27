"""
URL configuration for GoFind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Comptes.views import *
from GoFind import settings
from django.conf.urls.static import static
from GofindApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',index,name='index'),
    #path('profile/<str:id>',profile,name='profile'),
    #path('logout/',deconnexion,name='logout'),
    #path('Signalements/<str:id>',Signalements,name='Signalements'),
    #path('inscription/',inscription,name='inscription'),
    #path('connexion/',connexion,name='connexion'),
    #path('Recherche/<str:sujet>',Recherche,name='Recherche'),
    #path('notifications/<str:id>',notifications,name='notifications'),
    #path('Apropos/',Apropos,name='Apropos'),
    #path('SupprimerSignal/<str:id>',SupprimerSignal,name='SupprimerSignal'),
    #path('SignalerObjet/',SignalerObjet,name='SignalerObjet'),
    #path('SignalerApart/',SignalerApart,name='SignalerApart'),
    #path('SignalerTrajet/',SignalerTrajet,name='SignalerTrajet'),
    #path('DetailObjet/<str:id>',DetailObjet,name='DetailObjet'),
    #path('DetailTrajet/<str:id>',DetailTrajet,name='DetailTrajet'),
    #path('DetailColloc/<str:id>',DetailColloc,name='DetailColloc'),


   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
