from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check/', views.check_interactions, name='check_interactions'),
    path('search/', views.search_drug, name='search_drug'),
]