from datetime import date
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import APIException, NotFound
from .models import DailySale, Product

class StockConflict(APIException):
    status_code = 409
    default_code = "estoque_insuficiente"

@transaction.atomic
def register_sale(product_id: int, quantity: int, sale_date: date):
    product = Product.objects.select_for_update().filter(pk=product_id, active=True).first()
    if product is None:
        raise NotFound("Produto não encontrado.")
    if quantity > product.stock:
        raise StockConflict({"erro": "estoque_insuficiente", "mensagem": f"Estoque insuficiente. Disponível: {product.stock} unidades.", "estoque_atual": product.stock})
    product.stock = F("stock") - quantity
    product.save(update_fields=["stock"])
    sale, created = DailySale.objects.get_or_create(product=product, date=sale_date, defaults={"quantity": quantity})
    if not created:
        DailySale.objects.filter(pk=sale.pk).update(quantity=F("quantity") + quantity)
    product.refresh_from_db()
    return product

@transaction.atomic
def register_restock(product_id: int, quantity: int):
    product = Product.objects.select_for_update().filter(pk=product_id, active=True).first()
    if product is None:
        raise NotFound("Produto não encontrado.")
    Product.objects.filter(pk=product.pk).update(stock=F("stock") + quantity)
    product.refresh_from_db()
    return product
