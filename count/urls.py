
from django.urls import path, include
from . import views


app_name = 'count'

urlpatterns = [
    path('frequency/', views.home, name='frequency'),
    path('result/', views.count, name='result'),
]
