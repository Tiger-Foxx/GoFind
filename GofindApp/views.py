import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from GofindApp.models import*
from Comptes.models import *
import json

# Create your views here.


def index(request):
    
    return render(request, 'GofindApp/index.html')