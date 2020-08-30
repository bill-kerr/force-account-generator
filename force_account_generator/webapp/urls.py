from django.urls import path

from . import views

app_name = 'webapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate, name='generate'),
    path('packages/<uuid:task_id>', views.packages, name='packages'),
    path('about/', views.about, name='about'),
    path('demo/', views.demo, name='demo')
]
