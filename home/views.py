from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return JsonResponse({'message': 'Welcome to the Home Page!'})

def loading(request):
    return JsonResponse({'message': 'loading page'})