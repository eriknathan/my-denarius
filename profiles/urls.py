from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfileDetailView.as_view(), name='detail'),
    path('editar/', views.ProfileUpdateView.as_view(), name='update'),
]
