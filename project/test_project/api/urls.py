from django.urls import path, include, re_path
from django.conf.urls import url
# from rest_framework.routers import DefaultRouter

from . import views


# router = DefaultRouter()
# router.register('calculate', views.CalculateView)

urlpatterns = [
    path('calculate/', views.CalculateView.as_view(), name='calculate')
]
