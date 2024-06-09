import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from GofindApp.models import*
from Comptes.models import *
import json
from django.db.models import Q
from django.http import JsonResponse
from .models import SignalementColloc

# Create your views here.


# File: GofindApp/views.py


def index(request):
    mettre_a_jour_trajets()
    return render(request, 'GofindApp/index.html')

def get_colocations(request):
    ville = request.GET.get('ville', '')
    if ville:
        colocations = SignalementColloc.objects.filter(lieu__icontains=ville)[:5]
        if colocations.count() < 5:
            additional_colocs = SignalementColloc.objects.exclude(lieu__icontains=ville)[:(5 - colocations.count())]
            colocations = list(colocations) + list(additional_colocs)
    else:
        colocations = SignalementColloc.objects.all()[:5]
    
    colocation_data = []
    for colocation in colocations:
        colocation_data.append({
            'id': colocation.id,
            'titre': colocation.titre,
            'lieu': colocation.lieu,
            'prix': colocation.prix,
            'details': colocation.details,
            'photo_url': colocation.Photo1.url,
        })
    
    return JsonResponse({'colocations': colocation_data})





def DetailColloc(request, id):
    colocation = get_object_or_404(SignalementColloc, id=id)
    photos = [colocation.Photo1.url]
    if colocation.Photo2:
        photos.append(colocation.Photo2.url)
    else:
        photos.append(colocation.Photo1.url)
    if colocation.Photo3:
        photos.append(colocation.Photo3.url)
    else:
        photos.append(colocation.Photo1.url)

    bailleur_whatsapp = colocation.Auteur.whatsapp

    # Rechercher des appartements similaires
    similar_colocs = SignalementColloc.objects.filter(
        Q(nombre=colocation.nombre) | 
        Q(lieu__icontains=colocation.lieu) |
        Q(prix__range=(colocation.prix - 1000, colocation.prix + 1000))
    ).exclude(id=colocation.id)[:5]

    # Compléter avec d'autres colocations si moins de 5 trouvées
    if similar_colocs.count() < 5:
        additional_colocs = SignalementColloc.objects.exclude(id__in=similar_colocs).exclude(id=colocation.id)[:(5 - similar_colocs.count())]
        similar_colocs = list(similar_colocs) + list(additional_colocs)

    return render(request, 'GofindApp/detail-Coloc.html', {
        'colocation': colocation,
        'photos': photos,
        'bailleur_whatsapp': bailleur_whatsapp,
        'similar_colocs': similar_colocs
    })
    
# File: GofindApp/views.py



def signaler_colloc(request):
    if request.method == 'POST':
        titre = request.POST.get("titre")
        lieu = request.POST.get("lieu")
        prix = request.POST.get("prix")
        personnes = request.POST.get("personnes")
        description = request.POST.get("description")
        photo1 = request.FILES.get("photo1")
        photo2 = request.FILES.get("photo2")
        photo3 = request.FILES.get("photo3")
        
        # Vérifier les champs obligatoires
        if not all([titre, lieu, prix, personnes, description, photo1]):
            return JsonResponse({"success": False, "message": "Tous les champs obligatoires doivent être remplis."})

        auteur = request.user
        
        # Vérifier si un signalement similaire existe déjà
        if SignalementColloc.objects.filter(Auteur=auteur, lieu=lieu, prix=prix).exists():
            return JsonResponse({"success": False, "message": "Ce signalement existe déjà."})
        
        # Créer et sauvegarder le nouveau signalement
        SignalementColloc.objects.create(
            titre=titre,
            lieu=lieu,
            prix=prix,
            nombre=personnes,
            details=description,
            Photo1=photo1,
            Photo2=photo2,
            Photo3=photo3,
            Auteur=auteur
        )
        
        return JsonResponse({"success": True, "redirect_url": "/"})
    else:
        return render(request, 'GofindApp/SignalerColloc.html')


def liste_colocations(request):
    colocations = SignalementColloc.objects.all()
    return render(request, 'GofindApp/Collocations.html', {'colocations': colocations})

def liste_trajets(request):
    trajets = SignalementTrajet.objects.all()
    return render(request, 'GofindApp/Trajets.html', {'trajets': trajets})


def SignalerTrajet(request):
    if request.method == 'POST':
        depart = request.POST.get("depart")
        destination = request.POST.get("destination")
        places = request.POST.get("places")
        prix = request.POST.get("prix")
        date = request.POST.get("date")
        voiture = request.POST.get("voiture")
        commentaire = request.POST.get("Commentaire")
        photo1 = request.FILES.get("photo1")
        photo2 = request.FILES.get("photo2")
        photo3 = request.FILES.get("photo3")
        
        auteur = request.user
        
        SignalementTrajet.objects.create(
            Depart=depart,
            Arrive=destination,
            places=places,
            lieu=depart,
            prix=prix,
            dateDepart=date,
            modeleVoiture=voiture,
            commentaire=commentaire,
            Photo1=photo1,
            Photo2=photo2,
            Photo3=photo3,
            Auteur=auteur
        )
        
        return redirect('index')
    else:
        return render(request, 'GofindApp/SignalerTrajet.html')


# File: GofindApp/views.py

def DetailTrajet(request, id):
    trajet = get_object_or_404(SignalementTrajet, id=id)
    similaires = SignalementTrajet.objects.filter(Q(Arrive__contains=trajet.Arrive[0:5]) | Q(Depart__contains=trajet.Depart[0:5])) 
      
    photos = [trajet.Photo1.url]
    if trajet.Photo2:
        photos.append(trajet.Photo2.url)
    else:
        photos.append(trajet.Photo1.url)
    if trajet.Photo3:
        photos.append(trajet.Photo3.url)
    else:
        photos.append(trajet.Photo1.url)

    return render(request, 'GofindApp/detail-Trajet.html', {
        'trajet': trajet,
        'similaires':similaires,
        'photos': photos
    })



from django.db.models import Avg

def get_trajets(request):
    ville = request.GET.get('ville', '')
    if ville:
        trajets = SignalementTrajet.objects.filter(Depart__icontains=ville)[:5]
        if not trajets:
            print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeemptyyyyyyyyyyy")
        else:
            print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOT eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeemptyyyyyyyyyyy")
        if trajets.count() < 5:
            additional_trajets = SignalementTrajet.objects.exclude(Depart__icontains=ville)[:(5 - trajets.count())]
            trajets = list(trajets) + list(additional_trajets)
            
    else:
        trajets = SignalementTrajet.objects.all()[:5]
    
    prix_moyen = SignalementTrajet.objects.filter(Depart__icontains=ville).aggregate(Avg('prix'))['prix__avg']
    
    trajet_data = []
    for trajet in trajets:
        trajet_data.append({
            'id': trajet.id,
            'Depart': trajet.Depart,
            'Arrive': trajet.Arrive,
            'prix': trajet.prix,
            'places': trajet.places,
            'dateDepart': trajet.dateDepart.strftime("%Y-%m-%d %H:%M"),
            'photo_url': trajet.Photo1.url,
        })
    
    return JsonResponse({'trajets': trajet_data, 'prix_moyen': prix_moyen})

def mettre_a_jour_trajets():
    # Supprimer les trajets dont la date est déjà passée
    SignalementTrajet.objects.filter(dateDepart__lt=timezone.now()).delete()
    return JsonResponse({"success": True})


def Recherche(request):
    sujet=request.POST.get('sujet')
    sujet = sujet.lower()
    colocs = SignalementColloc.objects.filter(
        Q(lieu__icontains=sujet) | Q(details__icontains=sujet)
    )
    trajets = SignalementTrajet.objects.filter(
        Q(Depart__icontains=sujet) | Q(Arrive__icontains=sujet)
    )
    objets = SignalementObjet.objects.filter(
        Q(Code__iexact=sujet) | Q(nom__icontains=sujet)
    )
    
    return render(request, 'GofindApp/Resultats.html', {
        'colocs': colocs,
        'trajets': trajets,
        'objets': objets,
        'sujet': sujet,
    })
    

def Signalements(request):
    # Récupérer les signalements de l'utilisateur connecté
    user = request.user
    signalements_colloc = SignalementColloc.objects.filter(Auteur=user).order_by('-date')
    signalements_trajet = SignalementTrajet.objects.filter(Auteur=user).order_by('-date')
    signalements_objet = SignalementObjet.objects.filter(Auteur=user).order_by('-date')

    signalements = list(signalements_colloc) + list(signalements_trajet) + list(signalements_objet)
    

    return render(request, 'GofindApp/Signalements.html', {'signalements': signalements})
def SupprimerSignal(request, signalement_id):
    # Supprimer un signalement
    signalement = get_object_or_404(Signalement, id=signalement_id, Auteur=request.user)
    if request.user==signalement.Auteur :
        signalement.delete()
    else:
        return redirect('index')
    return redirect('user_signalements')