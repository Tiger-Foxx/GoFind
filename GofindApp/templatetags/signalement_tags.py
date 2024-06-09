# File: GofindApp/templatetags/signalement_tags.py

from django import template

from GofindApp.models import *

register = template.Library()

@register.filter
def signalement_type(signalement):
    if isinstance(signalement, SignalementColloc):
        return 'Colocation'
    elif isinstance(signalement, SignalementTrajet):
        return 'Trajet'
    elif isinstance(signalement, SignalementObjet):
        return 'Objet'
    return 'Inconnu'
