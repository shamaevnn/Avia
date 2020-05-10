from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', TemplateView.as_view(template_name='info.html'))
]