from django.contrib import admin

from GofindApp.models import *

# Register your models here.
admin.site.register(Signalement)
admin.site.register(SignalementTrajet)
admin.site.register(SignalementColloc)
admin.site.register(SignalementObjet)