from datetime import timedelta
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.urls import path
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import DailySale, Product, Store
from .serializers import ProductSerializer, SaleSerializer, StoreSerializer
from .services import register_restock, register_sale

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    search_fields = ["name", "sku"]
    ordering_fields = ["name", "stock", "sku"]

    def get_queryset(self):
        return Product.objects.filter(active=True).select_related("store").annotate(
            sold_total=Coalesce(Sum("sales__quantity", filter=Q(sales__date__gte=self.forecast_start(), sales__date__lte=timezone.localdate())), 0)
        )

    def forecast_days(self):
        try:
            value = int(self.request.query_params.get("janela", 14))
        except (TypeError, ValueError):
            raise ValidationError({"mensagem": "A janela deve ser 7, 14 ou 30 dias."})
        if value not in (7, 14, 30):
            raise ValidationError({"mensagem": "A janela deve ser 7, 14 ou 30 dias."})
        return value

    def forecast_start(self):
        return timezone.localdate() - timedelta(days=self.forecast_days() - 1)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(days=self.forecast_days(), today=timezone.localdate(), start=self.forecast_start())
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        store_id = request.query_params.get("store_id")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        products = list(self.get_serializer(queryset, many=True).data)
        selected_status = request.query_params.get("status")
        if selected_status:
            products = [p for p in products if p["status"] == selected_status]
        products.sort(key=lambda p: p["dias_restantes"] if p["dias_restantes"] is not None else 10**9)
        return Response(products)

    def perform_destroy(self, instance):
        instance.active = False
        instance.save(update_fields=["active"])

    @action(detail=True, methods=["get", "post"])
    def sales(self, request, pk=None):
        product = self.get_object()
        if request.method == "POST":
            try:
                quantity = int(request.data.get("quantity", request.data.get("quantidade", 0)))
            except (TypeError, ValueError):
                raise ValidationError({"mensagem": "A quantidade precisa ser um número inteiro positivo."})
            if quantity <= 0:
                raise ValidationError({"mensagem": "A quantidade precisa ser um número inteiro positivo."})
            try:
                sale_date = request.data.get("date", request.data.get("data"))
                from datetime import date
                sale_date = date.fromisoformat(sale_date) if sale_date else timezone.localdate()
            except (TypeError, ValueError):
                raise ValidationError({"mensagem": "A data informada é inválida."})
            product = register_sale(product.id, quantity, sale_date)
            return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)
        try:
            days = max(1, min(int(request.query_params.get("days", 30)), 365))
        except (TypeError, ValueError):
            days = 30
        today = timezone.localdate()
        sales = {sale.date: sale.quantity for sale in DailySale.objects.filter(product=product, date__gte=today - timedelta(days=days - 1), date__lte=today)}
        return Response([{"data": today - timedelta(days=offset), "quantidade": sales.get(today - timedelta(days=offset), 0)} for offset in reversed(range(days))])

    @action(detail=True, methods=["post"])
    def restock(self, request, pk=None):
        product = self.get_object()
        try:
            quantity = int(request.data.get("quantity", request.data.get("quantidade", 0)))
        except (TypeError, ValueError):
            raise ValidationError({"mensagem": "A quantidade precisa ser um número inteiro positivo."})
        if quantity <= 0:
            raise ValidationError({"mensagem": "A quantidade precisa ser um número inteiro positivo."})
        product = register_restock(product.id, quantity)
        return Response(self.get_serializer(product).data, status=status.HTTP_200_OK)

@api_view(["GET"])
def dashboard(request):
    try:
        days = int(request.GET.get("janela", 14))
        if days not in (7, 14, 30):
            raise ValueError
    except ValueError:
        return Response({"mensagem": "A janela deve ser 7, 14 ou 30 dias."}, status=400)
    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    products = Product.objects.filter(active=True).select_related("store").annotate(
        sold_total=Coalesce(Sum("sales__quantity", filter=Q(sales__date__gte=start, sales__date__lte=today)), 0)
    )
    if request.GET.get("store_id"):
        products = products.filter(store_id=request.GET["store_id"])
    rows = ProductSerializer(products, many=True, context={"days": days, "start": start, "today": today}).data
    counts = {key: sum(1 for row in rows if row["status"] == key) for key in ("critico", "atencao", "ok", "sem_giro", "esgotado")}
    urgent = sorted(rows, key=lambda row: row["dias_restantes"] if row["dias_restantes"] is not None else 10**9)[:5]
    return Response({"janela": days, "status": counts, "produtos_criticos": urgent})
