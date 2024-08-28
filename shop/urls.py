from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.home, name='home'),
    path('shop', views.shop, name='shop'),
    path('panier', views.panier, name='panier'),
    path('commande', views.commande, name='commande'),
    path('update_article/', views.update_article, name='update-article'),
    path('traitement_commande/', views.traitement_commande, name='traitement_commande'),
    path('commandeAnonyme/', views.commandeAnonyme, name='commandeAnonyme')
]