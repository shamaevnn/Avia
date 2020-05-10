from django.shortcuts import render
from django.template.response import TemplateResponse

def index(request):
    return TemplateResponse(request, 'start.html')

def hangar(request):
    return TemplateResponse(request, 'info.html')