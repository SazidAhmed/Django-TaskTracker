import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def about(request):
  return render(request, 'about.html')

def contact(request):
  return render(request, 'contact.html')