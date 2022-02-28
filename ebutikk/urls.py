from django.urls import path
from . import views

urlpatterns = [
    path('', views.butikk, name='butikk'),
    path('handlevogn/', views.handlevogn, name='handlevogn'),
    path('utsjekk/', views.utsjekk, name='utsjekk'),

    path('oppdater/', views.oppdaterElementer, name ='oppdater'),
    path('behandling/', views.behandlingAvOrder, name = 'behandling'),

    path('registrering/', views.registrerKunde, name ='registrering'),
    path('logginn/', views.logginn, name ='logginn'),
    path('loggut/', views.loggut, name ='loggut'),
    
]