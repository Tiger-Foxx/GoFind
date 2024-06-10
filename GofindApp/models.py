from django.db import models

from Comptes.models import Utilisateur



# Create your models here.
class Signalement(models.Model):
    date=models.DateField(auto_now=True,editable=False)
    Auteur=models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    lieu=models.CharField(max_length=128,default="YAOUNDE") 
    def __str__(self):
        return f"SIGNALEMENT DE  : {self.Auteur.nom} LE {self.date}"

class SignalementColloc(Signalement):
    titre=models.CharField(max_length=128)
    Photo1=models.ImageField(upload_to='imagesMaisons')
    Photo2=models.ImageField(blank=True,upload_to='imagesMaisons',null=True)
    Photo3=models.ImageField(blank=True,upload_to='imagesMaisons',null=True)
    details=models.TextField()
    
    prix=models.IntegerField() 
    nombre = models.IntegerField()  
    def __str__(self):
        return f"COLOCATION | SIGNALEMENT DE  : {self.Auteur.nom} LE {self.date}"

class SignalementTrajet(Signalement):
    Depart=models.CharField(max_length=128)
    Arrive=models.CharField(max_length=128)
    Photo1=models.ImageField(upload_to='imagesVoiture')
    Photo2=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    Photo3=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    commentaire=models.TextField()
    prix=models.IntegerField() 
    places = models.IntegerField()  
    dateDepart=models.DateTimeField()
    modeleVoiture=models.CharField(max_length=200)
    def __str__(self):
        return f"TRAJET | SIGNALEMENT DE  : {self.Auteur.nom} LE {self.date} TRAJET {self.Depart} - {self.Arrive}"    

class SignalementObjet(Signalement):
    Code=models.CharField(max_length=328)
    nom=models.CharField(max_length=328)
    Photo1=models.ImageField(upload_to='imagesVoiture')
    Photo2=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    Photo3=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    description=models.TextField()
    cathegorie=models.CharField(max_length=200)
    def __str__(self):
        return f"OBJETS VOLE | SIGNALEMENT DE  : {self.Auteur.nom} LE {self.date} OBJET {self.nom}" 
    
    
class Notification(models.Model):
    declancheur=models.CharField(max_length=128,null=True, blank=True)  # si jamais la notification a etee declanchee par un autre utilisateur comme dans le cas d'une recherche , il sa'agit du whatsapp du declancheur
    date=models.DateField(auto_now=True,editable=False)
    Receveur=models.ForeignKey(Utilisateur,on_delete=models.CASCADE,null=True,blank=True)
    Objet=models.ForeignKey(SignalementObjet,on_delete=models.CASCADE,null=True,blank=True)
    message=models.TextField(blank=True , null=True)
    lieu=models.CharField(max_length=128,null=True, blank=True) # si jamais la notif est declanchee par la saisie exacte du code d'un objet vole
    def __str__(self):
        return f"NOTIFICATION DE  : {self.Receveur.nom} LE {self.date}"