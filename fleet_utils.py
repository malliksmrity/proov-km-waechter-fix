# fleet_utils.py
# Helpers for KM-Waechter. Modernized 2024.
# Dead code removed: parse_service_date (2014 garage form, retired),
# chunk_list (never called), is_due (duplicate of needs_service).

KM_PER_MILE = 1.609344          # exact: 1 mile = 1.609344 km
MILES_PER_KM = 1 / KM_PER_MILE  # ≈ 0.6214 — previously had 1.609 here (wrong direction)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles.

    Note: used by the nightly run for the UK partner report. Do not remove.
    """
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list of floats, or 0.0 for an empty list.

    Note: statistics.mean exists since Python 3.4 and is preferred for new code.
    """
    if not values:
        return 0.0
    return sum(values) / len(values)
