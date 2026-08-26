# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernized 2024.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how worn the service interval is, as a percentage (0–100+)."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True if this car has reached or exceeded the service warning threshold.

    A car with no recorded last-service reading is treated as unknown, not as
    brand-new — it is NOT flagged.
    """
    if "last_service_km" not in car:
        return False
    km_since = car["odometer"] - car["last_service_km"]
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car in the fleet that needs a service; return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
