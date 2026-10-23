from django.db.models import Sum
from rest_framework import serializers
from .forecast import calculate_forecast
from .models import DailySale, Product, Store

class StoreSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="name")
    class Meta:
        model = Store
        fields = ["id", "nome"]

    def validate_nome(self, value):
        matches = Store.objects.filter(name__iexact=value.strip())
        if self.instance:
            matches = matches.exclude(pk=self.instance.pk)
        if matches.exists():
            raise serializers.ValidationError("Já existe uma cidade ou estoque com esse nome.")
        return value.strip()

class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField()
    nome = serializers.CharField(source="name")
    estoque_atual = serializers.IntegerField(source="stock", min_value=0)
    prazo_reposicao_dias = serializers.IntegerField(source="restock_days", min_value=0, required=False)
    store_id = serializers.PrimaryKeyRelatedField(source="store", queryset=Store.objects.all())
    media_diaria = serializers.SerializerMethodField()
    dias_restantes = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    pedir_ate = serializers.SerializerMethodField()
    reposicao_atrasada = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "sku", "nome", "estoque_atual", "prazo_reposicao_dias", "store_id", "media_diaria", "dias_restantes", "status", "pedir_ate", "reposicao_atrasada"]

    def validate(self, attrs):
        store = attrs.get("store", getattr(self.instance, "store", None))
        sku = attrs.get("sku", getattr(self.instance, "sku", "")).strip()
        matches = Product.objects.filter(store=store, sku__iexact=sku)
        if self.instance:
            matches = matches.exclude(pk=self.instance.pk)
        if matches.exists():
            raise serializers.ValidationError({"sku": "Este SKU já está cadastrado neste estoque."})
        return attrs

    def forecast(self, obj):
        days = int(self.context.get("days", 14))
        totals = getattr(obj, "sold_total", None)
        if totals is None:
            totals = DailySale.objects.filter(product=obj, date__gte=self.context["start"], date__lte=self.context["today"]).aggregate(total=Sum("quantity"))["total"] or 0
        return calculate_forecast(obj.stock, totals, days, obj.restock_days, self.context["today"])

    def get_media_diaria(self, obj): return self.forecast(obj)["media_diaria"]
    def get_dias_restantes(self, obj): return self.forecast(obj)["dias_restantes"]
    def get_status(self, obj): return self.forecast(obj)["status"]
    def get_pedir_ate(self, obj): return self.forecast(obj)["pedir_ate"]
    def get_reposicao_atrasada(self, obj): return self.forecast(obj)["reposicao_atrasada"]

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySale
        fields = ["date", "quantity"]
