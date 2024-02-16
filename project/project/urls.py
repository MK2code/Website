from django.contrib import admin
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth
from .router import router
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
 
    ##### user related path########################## 
    path('', include('user.urls')),
    path('login/', user_view.Login, name ='login'),
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    path('register/', user_view.register, name ='register'),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('verify_otp/', user_view.verify_otp, name='verify_otp'),
    
    ##### file manager related path##################
    path('file_explorer/', include('file_manager.urls')),
    ]