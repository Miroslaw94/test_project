from django.urls import path

from . import views


urlpatterns = [
    path('calculate-excel/', views.CalculateView.as_view(), name='calculate-excel')
]
