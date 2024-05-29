from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models



class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, telephone, **extra_fields):
        if not telephone:
            raise ValueError('Le numéro de téléphone doit être défini')
        user = self.model(telephone=telephone, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telephone, password, **extra_fields)

class Utilisateur(AbstractUser):
    username = models.CharField(max_length=13, unique=True) # il s'agit ici en realite de son numero de telephone
    email = models.EmailField()
    password = models.CharField(max_length=500)
    nom=models.CharField(max_length=200,null=True,blank=True)
    ville=models.CharField(max_length=100,null=True,blank=True)
    whatsapp = models.CharField(max_length=13,null=True,blank=True)
    #champs non editables
    date=models.DateField(auto_now=True,editable=False)
    def __str__(self):
        return f"Utilisateur | nom: {self.nom} | telphone: {self.whatsapp}"

