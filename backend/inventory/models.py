from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="products")
    sku = models.CharField(max_length=64)
    name = models.CharField(max_length=180)
    stock = models.PositiveIntegerField(default=0)
    restock_days = models.PositiveIntegerField(default=7)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["store", "sku"], name="unique_sku_per_store"), models.CheckConstraint(condition=models.Q(stock__gte=0), name="product_stock_nonnegative")]

    def __str__(self):
        return f"{self.name} ({self.sku})"

class DailySale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    date = models.DateField()
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ["date"]
        constraints = [models.UniqueConstraint(fields=["product", "date"], name="unique_product_sale_day"), models.CheckConstraint(condition=models.Q(quantity__gt=0), name="sale_quantity_positive")]
        indexes = [models.Index(fields=["product", "date"], name="sale_product_date_idx")]
