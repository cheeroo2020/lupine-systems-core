"""
Live FX rate feed — multi-source fallback chain.

Sources (in priority order):
  1. exchangerate.host        — updates every few minutes
  2. open.er-api.com           — hourly updates, no key
  3. jsdelivr currency-api     — daily snapshots, public CDN
  4. Frankfurter (ECB)         — daily reference rates

Each source is tried in order. Network errors cascade through the chain
so a single source outage never breaks the system. All sources are free
and require no API key.
"""
from __future__ import annotations

from datetime import datetime, timezone

import requests

_TIMEOUT = 8


def _from_exchangerate_host(frm: str, to: str) -> dict | None:
    try:
        r = requests.get(
            "https://api.exchangerate.host/latest",
            params={"base": frm, "symbols": to},
            timeout=_TIMEOUT,
        )
        r.raise_for_status()
        d = r.json()
        rate = d.get("rates", {}).get(to)
        if rate is None:
            return None
        return {
            "from": frm, "to": to, "rate": float(rate),
            "date": d.get("date", ""), "source": "exchangerate.host",
        }
    except Exception:
        return None


def _from_open_er_api(frm: str, to: str) -> dict | None:
    try:
        r = requests.get(f"https://open.er-api.com/v6/latest/{frm}", timeout=_TIMEOUT)
        r.raise_for_status()
        d = r.json()
        rate = d.get("rates", {}).get(to)
        if rate is None:
            return None
        # time_last_update_utc is RFC-2822 ("Sat, 02 May 2026 00:00:00 +0000");
        # the Unix field is a clean integer we can format ourselves.
        ts = d.get("time_last_update_unix")
        date_iso = (
            datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")
            if ts else ""
        )
        return {
            "from": frm, "to": to, "rate": float(rate),
            "date": date_iso,
            "source": "open.er-api.com",
        }
    except Exception:
        return None


def _from_jsdelivr(frm: str, to: str) -> dict | None:
    try:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{frm.lower()}.json"
        r = requests.get(url, timeout=_TIMEOUT)
        r.raise_for_status()
        d = r.json()
        rate = d.get(frm.lower(), {}).get(to.lower())
        if rate is None:
            return None
        return {
            "from": frm, "to": to, "rate": float(rate),
            "date": d.get("date", ""), "source": "jsdelivr currency-api",
        }
    except Exception:
        return None


def _from_frankfurter(frm: str, to: str) -> dict | None:
    try:
        r = requests.get(
            "https://api.frankfurter.app/latest",
            params={"from": frm, "to": to},
            timeout=_TIMEOUT,
        )
        r.raise_for_status()
        d = r.json()
        rate = d.get("rates", {}).get(to)
        if rate is None:
            return None
        return {
            "from": frm, "to": to, "rate": float(rate),
            "date": d.get("date", ""), "source": "Frankfurter (ECB)",
        }
    except Exception:
        return None


_SOURCES = (_from_exchangerate_host, _from_open_er_api, _from_jsdelivr, _from_frankfurter)


def fetch_fx_rate(from_currency: str, to_currency: str) -> dict:
    """Try each source in priority order; return the first successful result."""
    errors: list[str] = []
    for fn in _SOURCES:
        result = fn(from_currency, to_currency)
        if result:
            return result
        errors.append(fn.__name__)
    raise RuntimeError(
        f"All FX sources failed for {from_currency}/{to_currency}: "
        + ", ".join(errors)
    )


def fetch_historical_rate(from_currency: str, to_currency: str, date: str) -> dict:
    """Historical rate for a specific YYYY-MM-DD (Frankfurter is reliable for this)."""
    r = requests.get(
        f"https://api.frankfurter.app/{date}",
        params={"from": from_currency, "to": to_currency},
        timeout=_TIMEOUT,
    )
    r.raise_for_status()
    d = r.json()
    return {
        "from": from_currency,
        "to": to_currency,
        "rate": float(d["rates"][to_currency]),
        "date": d["date"],
    }
