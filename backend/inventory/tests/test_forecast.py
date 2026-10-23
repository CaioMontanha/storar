from datetime import date
from django.test import SimpleTestCase
from inventory.forecast import calculate_forecast

class ForecastTests(SimpleTestCase):
    def test_zero_sales_is_no_turnover(self):
        result = calculate_forecast(12, 0, 14, 7, date(2026, 10, 11))
        self.assertEqual(result["status"], "sem_giro")
        self.assertIsNone(result["dias_restantes"])

    def test_zero_stock_is_depleted(self):
        self.assertEqual(calculate_forecast(0, 10, 14, 7)["status"], "esgotado")

    def test_days_without_sales_remain_in_average(self):
        self.assertAlmostEqual(calculate_forecast(50, 10, 14, 7)["media_diaria"], 10 / 14)

    def test_status_thresholds(self):
        self.assertEqual(calculate_forecast(7, 7, 7, 0)["status"], "critico")
        self.assertEqual(calculate_forecast(8, 7, 7, 0)["status"], "atencao")
        self.assertEqual(calculate_forecast(21, 7, 7, 0)["status"], "atencao")
        self.assertEqual(calculate_forecast(22, 7, 7, 0)["status"], "ok")

    def test_late_restock(self):
        result = calculate_forecast(3, 14, 14, 7, date(2026, 10, 11))
        self.assertTrue(result["reposicao_atrasada"])
