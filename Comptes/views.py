import datetime
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model,login,logout,authenticate
import django.contrib.auth.models
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from Comptes.models import *
from GofindApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

User=get_user_model()


# Create your views here.

############################## AUTHENTIFICATION ##############################
##############################################################################


"""
Vue qui se charge de l'inscription de nouveaux utilisateurs 

"""


def inscription(request):
    if request.method == 'POST':
        passwordConfirm = request.POST.get("Confpassword")
        password = request.POST.get("password")
        name = request.POST.get("nom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        ville = request.POST.get("ville")
        Remember = request.POST.get("remember-me")

        if password == passwordConfirm:
            try:
                user = Utilisateur.objects.create_user(username=email, nom=name, password=password, whatsapp=telephone, ville=ville, email=email) # type: ignore
                user.is_active = False  # Désactiver le compte jusqu'à la vérification de l'email
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Activez votre compte.'
                message = render_to_string('Comptes/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email])

                return JsonResponse({"success": True, "redirect_url": "confirmation/"})
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)})
        else:
            return JsonResponse({"success": False, "message": "Les mots de passe ne correspondent pas."})
    else:
        return render(request, "Comptes/Register.html")

def confirmation(request):
    return render(request, 'Comptes/confirmation_message.html') 
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Utilisateur.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'Comptes/activation_invalid.html')

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

# File: GofindApp/views.py


@login_required
def profile(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    
    if request.user.id != utilisateur.id:
        return redirect('connexion')
    
    if request.method == 'POST':
        name = request.POST.get("nom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        ville = request.POST.get("ville")
        password = request.POST.get("password")
        
        utilisateur.nom = name
        utilisateur.username = telephone  # assuming username is telephone number
        utilisateur.whatsapp = telephone
        utilisateur.ville = ville
        utilisateur.email = email

        if password:
            utilisateur.password = make_password(password)
        
        utilisateur.save()
        return redirect('index')
    
    return render(request, 'GofindApp/profile.html', {'utilisateur': utilisateur})





def deconnexion(request):
    logout(request)
    return render(request,'Comptes/Login.html')

############################## AUTHENTIFICATION ##############################
##############################################################################