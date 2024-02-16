from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_explorer, name='file_explorer'),
    path('upload/<int:folder_id>/', views.file_explorer, name='upload_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('verification-required/', views.verification_required, name='verification_required'),
]
