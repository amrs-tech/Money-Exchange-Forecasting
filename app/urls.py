from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.data, name='data'),
    path('graph/', views.graph, name='graph'),
]