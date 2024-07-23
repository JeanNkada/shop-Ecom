from django.contrib import admin

from .models import *

class AdminClient(admin.ModelAdmin):
    list_display = ('name', 'email')
    
    
class AdminProduit(admin.ModelAdmin):
    list_display = ('name', 'categorie', 'price', 'digital', 'image', 'date_ajout')
    
    
class AdminCatégory(admin.ModelAdmin):
    list_display = ('name', 'description') 
    

class AdminCommande(admin.ModelAdmin):
    list_display = ('client', 'date_commande', 'complete', 'transaction_id', 'status', 'total_trans')
    
    
class AdminCommandeArticle(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'date_added')
    

class AdminAddressChipping(admin.ModelAdmin):
    list_display = ('client', 'commande', 'addresse', 'ville', 'zipcode', 'date_ajout')
    


admin.site.register(Client, AdminClient)
admin.site.register(Produit, AdminProduit)
admin.site.register(Category, AdminCatégory)
admin.site.register(Commande, AdminCommande)
admin.site.register(CommandeArticle, AdminCommandeArticle)
admin.site.register(AddressChipping, AdminAddressChipping)