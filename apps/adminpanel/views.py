import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
  return render(request, 'dashboard.html')
  
@login_required
def settings(request):
  return render(request, 'settings.html')