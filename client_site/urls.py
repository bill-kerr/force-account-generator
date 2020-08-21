from django.urls import path

from . import views

app_name = 'client_site'
urlpatterns = [
    path('', views.index, name='index')
]
