"""
Live FX rate feed — Frankfurter API (free, no key required).
https://www.frankfurter.app

Used by daily health checks to test the V0 pipeline against
real market data rather than hardcoded values.
"""
import requests

_BASE_URL = "https://api.frankfurter.app"


def fetch_fx_rate(from_currency: str, to_currency: str) -> dict:
    """
    Fetch the latest FX rate between two currencies.
    Returns rate, date, and both currency codes.
    """
    response = requests.get(
        f"{_BASE_URL}/latest",
        params={"from": from_currency, "to": to_currency},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "from": from_currency,
        "to": to_currency,
        "rate": data["rates"][to_currency],
        "date": data["date"],
    }


def fetch_historical_rate(from_currency: str, to_currency: str, date: str) -> dict:
    """
    Fetch FX rate for a specific date (YYYY-MM-DD).
    Useful for replaying past test runs against the same market data.
    """
    response = requests.get(
        f"{_BASE_URL}/{date}",
        params={"from": from_currency, "to": to_currency},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "from": from_currency,
        "to": to_currency,
        "rate": data["rates"][to_currency],
        "date": data["date"],
    }
