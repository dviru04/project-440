from django.contrib import admin
from django.urls import path,include
from projects.views import  upload_project  # Import both views
from projects.views import home  # Import the home view

from django.urls import include

urlpatterns = [
    path('', home, name='home'),  # This sets the root URL
    path('admin/', admin.site.urls),
    path("api/upload_project/", upload_project, name="upload_project"),  # Correct URL
    # Add these routes for django-allauth
    path('accounts/', include('allauth.urls')),  # Handles allauth routes
    path('projects/', include('projects.urls')),
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
