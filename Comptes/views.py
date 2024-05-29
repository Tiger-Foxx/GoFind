import datetime
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model,login,logout,authenticate
import django.contrib.auth.models
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

import random
import string
from Comptes.models import *
from GofindApp.models import *
User=get_user_model()


# Create your views here.

############################## AUTHENTIFICATION ##############################
##############################################################################


"""
Vue qui se charge de l'inscription de nouveaux utilisateurs 

"""

def inscription(request):
    
    if request.method == 'POST':
        # traiter le formulaire
        passwordConfirm =request.POST.get("Confpassword")
        password =request.POST.get("password")
        name =request.POST.get("nom")
        email =request.POST.get("email")
        telephone=request.POST.get("telephone")
        ville=request.POST.get("ville")
        Remember=request.POST.get("remember-me")
        
        print(f"REMEMBER : {Remember}")
        
        if password==passwordConfirm:
            try:
                    
                user=User.objects.create_user(username=email,nom=name,password=password,whatsapp=telephone,ville=ville,email=email) # type: ignore

                login(request,user)
                if Remember :
                    
                    request.session.set_expiry(1209600) # 2 semaines
                else:
                  print("not remember")
                  request.session.set_expiry(0)
                #apres inscription on le redirige
                if user.is_authenticated:
                    return JsonResponse({"success": True, "redirect_url": "/"}) # Renvoyer une réponse JSON avec un indicateur de succès et l'URL de redirection
                else : 
                    print(f"L'ERREUR EST INCONNUE ")
                    return JsonResponse({"success": False, "message": "ERREUR ou l'UTILISATEUR EXISTE DEJA"}) # Renvoyer une réponse JSON avec un indicateur d'échec et un message d'erreur
            except Exception as e:
                print(f"L'ERREUR EST : {e} ")
                return JsonResponse({"success": False, "message": e}) # Renvoyer une réponse JSON avec un indicateur d'échec et un message d'erreur

        
        else:
            return JsonResponse({"success": False, "message": "Les mots de passe ne correspondent pas."}) # Renvoyer une réponse JSON avec un indicateur d'échec et un message d'erreur
    else :
        return render(request,"Comptes/Register.html")
 
 
"""
Vue qui se charge de la connexion au compte des utilisateurs

"""   

def connexion(request):
    if request.method == 'POST':
        # conecter l'utilisateur
        email = request.POST.get("email")
        password =request.POST.get("password")
        Remember =request.POST.get("remember-me")
        print("le mdp est : "+password)
        print("l'email est : "+email)
        
        user=authenticate(username=email, password=password) 
        if user:
            login(request,user)
            request.session.set_expiry(1209600) # 2 weeks
            if not Remember:
                print("ok")
                request.session.set_expiry(0)
            return JsonResponse({"success": True, "redirect_url": "/"})#apres inscription on le redirige
        else:    
            return JsonResponse({"success": False, "message": "Nom d'utilisateur ou mot de passe incorrect !"}) # Renvoyer une réponse JSON avec un indicateur d'échec et un message d'erreur

    else :
        return render(request,'Comptes/Login.html')
    

"""
Vue qui se charge de consulter et modifier le profile d'un utilisateur

"""       

def profile(request,nom):
    if  not request.user.is_authenticated:
        return redirect('connexion')
    if  request.user.username !=nom:
        return redirect('connexion')
    if request.method == 'POST':
        utilisateur = get_object_or_404(Utilisateur,id=request.user.id)
         # traiter le formulaire
        password =request.POST.get("password")
        name =request.POST.get("nom")
        email =request.POST.get("email")
        telephone=request.POST.get("telephone")
        ville=request.POST.get("ville")
        utilisateur.nom=name
        utilisateur.username=email
        utilisateur.whatsapp=telephone
        utilisateur.ville=ville
        utilisateur.email=email
        if password and password !="":
            
            hashed_password = make_password(password)
            utilisateur.password=hashed_password
        utilisateur.save()
        
        return redirect('index')
    #notificationss=Notification.objects.all().order_by('-date')[:4]
    return render(request,'SmartInvestApp/profile.html')




def deconnexion(request):
    logout(request)
    return render(request,'Comptes/Login.html')

############################## AUTHENTIFICATION ##############################
##############################################################################