from django.urls import path
from .views import upload_project, project_list,home

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_project, name='upload_project'),
    path('projects/', project_list, name='project_list'),
]
from django.shortcuts import render

def home(request):
    return render(request, 'projects/home.html')  # Create this template
