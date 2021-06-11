from django.urls import path

from . import views


urlpatterns = [
    path('calculate/', views.CalculateView.as_view(), name='calculate')
]
