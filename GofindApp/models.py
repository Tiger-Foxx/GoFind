from django.db import models

from Comptes.models import Utilisateur







# Create your models here.
class Signalement(models.Model):
    date=models.DateField(auto_now=True,editable=False)
    Auteur=models.ForeignKey(Utilisateur,on_delete=models.CASCADE)


class SignalementColloc(Signalement):
    titre=models.CharField(max_length=128)
    Photo1=models.ImageField(upload_to='imagesMaisons')
    Photo2=models.ImageField(blank=True,upload_to='imagesMaisons',null=True)
    Photo3=models.ImageField(blank=True,upload_to='imagesMaisons',null=True)
    details=models.TextField()
    lieu=models.CharField(max_length=128,default="YAOUNDE") 
    prix=models.IntegerField() 
    nombre = models.IntegerField()  
    def __str__(self):
        return f"COLOCATION | SIGNALEMENT DE  : {self.Auteur} LE {self.date}"

class SignalementTrajet(Signalement):
    Depart=models.CharField(max_length=128)
    Arrive=models.CharField(max_length=128)
    Photo1=models.ImageField(upload_to='imagesVoiture')
    Photo2=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    Photo3=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    commentaire=models.TextField()
    lieu=models.CharField(max_length=128,default="YAOUNDE") 
    prix=models.IntegerField() 
    places = models.IntegerField()  
    dateDepart=models.DateTimeField()
    modeleVoiture=models.CharField(max_length=200)
    def __str__(self):
        return f"TRAJET | SIGNALEMENT DE  : {self.Auteur} LE {self.date} TRAJET {self.Depart} - {self.Arrive}"    

class SignalementObjet(Signalement):
    Code=models.CharField(max_length=328)
    nom=models.CharField(max_length=328)
    Photo1=models.ImageField(upload_to='imagesVoiture')
    Photo2=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    Photo3=models.ImageField(blank=True,upload_to='imagesVoiture',null=True)
    description=models.TextField()
    lieu=models.CharField(max_length=128,default="YAOUNDE") 
    cathegorie=models.CharField(max_length=200)
    def __str__(self):
        return f"OBJETS VOLE | SIGNALEMENT DE  : {self.Auteur} LE {self.date} OBJET {self.nom}" 