from django.urls import path
from electrodes import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
