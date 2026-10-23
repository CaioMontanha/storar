from datetime import date, timedelta

def calculate_forecast(stock: int, sold: int, days: int, restock_days: int, today: date | None = None) -> dict:
    today = today or date.today()
    average = sold / days if days else 0
    remaining = 0 if stock == 0 else (int(stock / average) if average else None)
    if stock == 0:
        status = "esgotado"
    elif average == 0:
        status = "sem_giro"
    elif remaining <= 7:
        status = "critico"
    elif remaining <= 21:
        status = "atencao"
    else:
        status = "ok"
    order_by = today + timedelta(days=remaining - restock_days) if remaining is not None else None
    return {"media_diaria": average, "dias_restantes": remaining, "status": status, "pedir_ate": order_by, "reposicao_atrasada": bool(order_by and order_by < today)}
