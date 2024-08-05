from django.shortcuts import render

from . models import *

from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required

from datetime import datetime

# Create your views here.


def home(request, *args, **kwargs):
    
    context = {}
    return render(request, 'base.html', context)


def shop(request, *args, **kwargs):
    produits = Produit.objects.all()
    
    if request.user.is_authenticated:
        
        client = request.user.client
        
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        nombre_article = commande.get_panier_article
        
    else:
        
        articles = []
        
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }
        nombre_article = commande['get_panier_article']
        
    context = {
        'produits' : produits,
        'nombre_article':nombre_article
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
        
        nombre_article = commande.get_panier_article
    else:
        articles = []
        
        commande = {
        'get_panier_total':0,
        'get_panier_article':0
        }
        nombre_article = commande['get_panier_article']
    context = {
    'articles':articles,
    'commande':commande,
    'nombre_article':nombre_article,

    }
    return render(request, 'shop/panier.html', context)



def commande(request, *args, **kwargs):
    """ Commande """
    if request.user.is_authenticated:
        
        client = request.user.client
        
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        articles = commande.commandearticle_set.all()
        
        nombre_article = commande.get_panier_article
        
    else:
        
        articles = []
        
        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }
        nombre_article = commande['get_panier_article']
        
    context = {
        'articles':articles,
        'commande':commande,
        'nombre_article':nombre_article
    }

    return render(request, 'shop/commande.html', context)


# fonction pour modifier un produit dans le panier

@login_required()
def update_article(request, *args, **kwargs):
    
    data = json.loads(request.body)
    
    produit_id = data['produit_id']
    
    action = data['action']
    
    client = request.user.client
    
    produit = Produit.objects.get(id=produit_id)
    
    commande, created = Commande.objects.get_or_create(client=client, complete=False)
    
    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)
    
    if action == 'add':
        
        commande_article.quantite += 1
        
    if action == 'remove':
        
        commande_article.quantite -= 1
        
    commande_article.save()
        
    if commande_article.quantite <= 0:
        
        commande_article.delete()
    
    return JsonResponse("Panier modifier", safe=False)


def traitement_commande(request, *args, **kwargs):
    """ traitement, validation de la com;ande et verification de l'integrite des donnees(detection de fraude)"""
    data = json.loads(request.body)
    transaction_id = datetime.now().timestamp()
    
    if request.user.is_authenticated:
        
        client = request.user.client
        
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
        total = float(data['form']['total'])
        
        # verification si le total au frontend est égale au total au backend
        
        commande.transaction_id = transaction_id
        
        if commande.get_panier_total == total:
            
            commande.complete = True
            
        commande.save()
            
        if commande.produit_physique:
            
            AddressChipping.objects.create(
                client=client,
                commande=commande,
                addresse=data['shipping']['address'],
                ville=data['shipping']['city'],
                zipcode=data['shipping']['zipcode'],
            )
        
    else:
        print("utilisateur non authentifie")


    return JsonResponse('Traitement complet', safe=False)