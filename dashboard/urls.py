from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('data', views.get_data, name='data'),
    path('nlu', views.get_nlu, name='nlu')
]
