from django.shortcuts import render

from . models import *

# Create your views here.


def home(request, *args, **kwargs):
    
    context = {}
    return render(request, 'base.html', context)

def shop(request, *args, **kwargs):
    produits = Produit.objects.all()
    
    context = {
        'produits' : produits
    }
    
    return render(request, 'shop/index.html', context)



#afficher les articles de l'utlisateur connecté
def panier(request, *args, **kwargs):
    
    if request.user.is_authenticated:
        
        client = request.user.client
        
        #récupération de la commande en cours ou création d'une nouvelle commande si elle n'existe pas déjà
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        #liste des article liés a cette commande
        articles = commande.commandearticle_set.all()
    else:
        articles = []
        
        commande = {
        'get_panier_total':0,
        'get_panier_article':0
        }
    context = {
    'articles':articles,
    'commande':commande

    }
    return render(request, 'shop/panier.html', context)



def commande(request, *args, **kwargs):
    """ Commande """
    if request.user.is_authenticated:
        
        client = request.user.client
        
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        articles = commande.commandearticle_set.all()
        
    else:
        
        articles = []
        
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }
        
    context = {
        'articles':articles,
        'commande':commande
    }

    return render(request, 'shop/commande.html', context)