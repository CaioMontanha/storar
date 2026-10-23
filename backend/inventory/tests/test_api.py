from rest_framework.test import APITestCase
from inventory.models import DailySale, Product, Store

class InventoryApiTests(APITestCase):
    def setUp(self):
        self.store = Store.objects.create(name="Porto de Galinhas")
        self.product = Product.objects.create(store=self.store, sku="TSH-01", name="Camiseta Porto", stock=12)

    def test_store_and_product_list_are_persistent_and_scoped(self):
        response = self.client.get("/api/products/", {"store_id": self.store.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["sku"], "TSH-01")

    def test_sale_updates_stock_and_creates_daily_record(self):
        response = self.client.post(f"/api/products/{self.product.id}/sales/", {"quantidade": 3})
        self.assertEqual(response.status_code, 201)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)
        self.assertEqual(DailySale.objects.get(product=self.product).quantity, 3)

    def test_overselling_returns_conflict_without_mutation(self):
        response = self.client.post(f"/api/products/{self.product.id}/sales/", {"quantidade": 20})
        self.assertEqual(response.status_code, 409)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 12)

    def test_restock_updates_stock(self):
        response = self.client.post(f"/api/products/{self.product.id}/restock/", {"quantidade": 5})
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 17)

    def test_store_rename(self):
        response = self.client.patch(f"/api/stores/{self.store.id}/", {"nome": "Recife Centro"})
        self.assertEqual(response.status_code, 200)
        self.store.refresh_from_db()
        self.assertEqual(self.store.name, "Recife Centro")
