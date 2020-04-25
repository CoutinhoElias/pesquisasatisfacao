from django.db import models
from pesquisasatisfacao.core.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

# Create your models here.
# class ConsumoManager(models.Manager):
#     # FALTA RESOLVER ESSE PROBLEMA
#     def add_item(self, table, product, quantity,_user):
#         
#         consumo, created = self.get_or_create(table=table, 
#                                               product=product,
#                                               quantity=quantity, 
#                                               created_on=datetime.date.today(),
#                                               user=_user)
#         if not created:
#             print('Não Existe <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')  
#             consumo.quantity += 1
#             consumo.save()
#         # else:
#         #     print('Existe <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')    
#         return consumo    

class Consumo(models.Model):
    table = models.PositiveIntegerField('Mesa') 
    product = models.ForeignKey(Product, related_name="product_consumo_item", on_delete=models.CASCADE,
                                verbose_name="Produto")
    quantity = models.DecimalField('Quantidade', max_digits=10, decimal_places=2, default='0', )
    # models.PositiveIntegerField('Quantidade')                       
    data_pagamento = models.DateField(null=True, blank=True)
    # valor_vendido = models.DecimalField('Valor Vendido', max_digits=15, decimal_places=2)
    user = models.ForeignKey(User, related_name='Consumo_Usuario', on_delete=models.CASCADE)
    created_on = models.DateField(
        'Criado em.',
        auto_now_add=True,
        auto_now=False
    )
    pay = models.BooleanField('Conta Paga', default=False)

    # objects = ConsumoManager()    

    class Meta:
        verbose_name = 'Consumo Detalhe'
        verbose_name_plural = 'Consumo Detalhes'
        unique_together = (('table', 'product', 'created_on', 'pay'),)
        