from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


GITHUB_API_URL = "https://api.github.com/search/repositories"


def search_github(query: str, sort: str = "stars", limit: int = 5) -> dict[str, Any]:
    """Search public GitHub repositories by keyword, topic, or entity."""
    query = (query or "").strip()
    if not query:
        return {"tool": "HuyThu", "query": "", "items": [], "total_count": 0}

    try:
        limit_val = int(limit)
    except (ValueError, TypeError):
        limit_val = 5
    limit_val = max(1, min(limit_val, 30))

    valid_sorts = {"stars", "forks", "updated"}
    sort_val = sort if sort in valid_sorts else "stars"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "AI20k-Day03-Research-Agent/1.0",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {
        "q": query,
        "sort": sort_val,
        "per_page": limit_val,
    }

    try:
        response = requests.get(GITHUB_API_URL, params=params, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        raw_items = data.get("items", [])
        items = [
            {
                "name": item.get("name", ""),
                "full_name": item.get("full_name", ""),
                "url": item.get("html_url", ""),
                "description": item.get("description") or "",
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "language": item.get("language") or "",
            }
            for item in raw_items[:limit_val]
        ]
        return {
            "tool": "HuyThu",
            "query": query,
            "items": items,
            "total_count": data.get("total_count", len(items)),
        }
    except Exception as exc:
        return err("HuyThu", exc)

