from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog.views import blog_home, post_detail, create_post, signup_view, login_view, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_home, name='blog_home'),
    path('signup/', signup_view, name='signup'),  # Fixed import name
    path('login/', login_view, name='login'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
    path('logout/', user_logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
