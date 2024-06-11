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
    path('',index,name='index'),
    #path('profile/<str:id>',profile,name='profile'),
    path('logout/',deconnexion,name='logout'),
    path('liste_colocations',liste_colocations,name='liste_colocations'),
     path('liste_trajets',liste_trajets,name='liste_trajets'),
      path('liste_objets',liste_objets,name='liste_objets'),
    path('Signalements/',Signalements,name='Signalements'),
    path('inscription/',inscription,name='inscription'),
    path('connexion/',connexion,name='connexion'),
     path('get_colocations/', get_colocations, name='get_colocations'),
     path('get_trajets/', get_trajets, name='get_trajets'),
    path('Recherche/',Recherche,name='Recherche'),
    path('notifications/',notifications,name='notifications'),
    #path('Apropos/',Apropos,name='Apropos'),
    path('SupprimerSignal/<str:id>',SupprimerSignal,name='SupprimerSignal'),
    path('SignalerObjet/',SignalerObjet,name='SignalerObjet'),
   path('signaler_colloc/', signaler_colloc, name='signaler_colloc'),
    path('SignalerTrajet/',SignalerTrajet,name='SignalerTrajet'),
    path('detail_objet/<str:id>',detail_objet,name='detail_objet'),
    path('DetailTrajet/<str:id>',DetailTrajet,name='DetailTrajet'),
    path('DetailColloc/<str:id>',DetailColloc,name='DetailColloc'),
    path('register/', inscription, name='register'),
    path('inscription/confirmation/', confirmation, name='confirmation'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('update-fcm-token/', update_fcm_token, name='update_fcm_token'),
    path('about/', about, name='about'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
