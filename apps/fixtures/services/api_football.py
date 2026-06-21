import requests

from django.conf import settings


BASE_URL = "https://v3.football.api-sports.io"


class ApiFootballError(Exception):
    pass


def api_football_get(endpoint, params=None):
    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers={
            "x-apisports-key": settings.API_FOOTBALL_KEY.strip(),
        },
        params=params or {},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise ApiFootballError(data["errors"])

    return data