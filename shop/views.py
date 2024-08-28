from django.shortcuts import render

from . models import *

from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required

from datetime import datetime

from .utiles import panier_cookie, data_cookie

# Create your views here.


def home(request, *args, **kwargs):
    
    context = {}
    return render(request, 'base.html', context)


def shop(request, *args, **kwargs):
    
    produits = Produit.objects.all()
    data = data_cookie(request)
    nombre_article = data['nombre_article']
    
    context = {
        'produits' : produits,
        'nombre_article':nombre_article
    }
    
    return render(request, 'shop/index.html', context)



#afficher les articles de l'utlisateur connecté
def panier(request, *args, **kwargs):
    
    data = data_cookie(request)  
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']
        
    context = {
    'articles':articles,
    'commande':commande,
    'nombre_article':nombre_article,

    }
    return render(request, 'shop/panier.html', context)



def commande(request, *args, **kwargs):
    """ Commande """
    data = data_cookie(request)  
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']
        
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


def commandeAnonyme(request, data):
    
    name = data['form']['name']
    username = data['form']['username']
    email = data['form']['email']
    phone = data['form']['phone']
    
    cookie_panier = panier_cookie(request)
    articles = cookie_panier['articles']
    client, created = Client.objects.get_or_create(
        email = email
    )
    
    client.name = name
    client.save()
    
    commande = Commande.objects.create(
        client=client
    ) 
    for article in articles:
        produit = Produit.objects.get(id=article['produit']['id'])
        CommandeArticle.objects.create(
            produit=produit,
            commande = commande,
            quantite = article['quantite']
        )
    return client, commande

from decimal import Decimal
def traitement_commande(request, *args, **kwargs):
    """ traitement, validation de la commande et verification de l'integrite des donnees(detection de fraude)"""
    data = json.loads(request.body)
    transaction_id = datetime.now().timestamp()
    
    if request.user.is_authenticated:
        
        client = request.user.client
        
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        
    else:
        client, commande = commandeAnonyme(request, data)
        
    total = float(data['form']['total'])
    print(data)
        
        # verification si le total au frontend est égale au total au backend
        
    commande.transaction_id = data['payment_info']['transaction_id']
    
    commande.total_trans = Decimal(data['payment_info'] ['total'])   
    
    if commande.get_panier_total == Decimal(total):
        
        commande.complete = True
        commande.status = data['payment_info']['status']
    
    else:
        commande.status = 'REFUSE'
        
        return JsonResponse('Attention Traitement refusé Fraude detecté', safe=False)
    
    commande.save()    
    

        
    if commande.produit_physique:
        
        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse=data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode'],
        )
        
    return JsonResponse('Traitement complet', safe=False)