import json
from pathlib import Path
from typing import Any

import aiohttp
from bs4 import BeautifulSoup


BASE_URL = "https://mw2.wiki"
CACHE_DIR = Path(__file__).resolve().parents[1] / "data" / "skills"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

_skills_cache: dict[str, dict[str, list[dict[str, str]]]] = {}


async def get_skills(
    class_slug: str,
    force_refresh: bool = False,
) -> dict[str, list[dict[str, str]]]:
    if class_slug in _skills_cache and not force_refresh:
        return _skills_cache[class_slug]

    cache_file = CACHE_DIR / f"{class_slug}.json"
    if cache_file.exists() and not force_refresh:
        with cache_file.open("r", encoding="utf-8") as file:
            data: Any = json.load(file)
        if isinstance(data, dict):
            _skills_cache[class_slug] = data
            return data

    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(f"{BASE_URL}/lu4/class/{class_slug}/all") as response:
            response.raise_for_status()
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    result: dict[str, list[dict[str, str]]] = {}

    for accordion in soup.select(".accordion-item"):
        title = accordion.select_one(".accordion-header .mr-auto")
        if title is None:
            continue

        category = title.get_text(strip=True)
        result[category] = []
        for link in accordion.select(".accordion-body a[href*='/skill/']"):
            href = link.get("href")
            if not isinstance(href, str):
                continue

            title_tag = link.select_one(".item-name__content")
            name = title_tag.contents[0].strip() if title_tag and title_tag.contents else ""
            level_tag = link.select_one(".item-name__additional")
            description_tag = link.select_one(".skill_description")
            result[category].append(
                {
                    "name": name,
                    "slug": href.rstrip("/").split("/")[-2],
                    "level": level_tag.get_text(strip=True) if level_tag else "",
                    "description": (
                        description_tag.get_text("\n", strip=True)
                        if description_tag
                        else ""
                    ),
                    "url": f"{BASE_URL}{href}",
                }
            )

    with cache_file.open("w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    _skills_cache[class_slug] = result
    return result


async def refresh_skills(
    class_slug: str,
) -> dict[str, list[dict[str, str]]]:
    return await get_skills(class_slug, force_refresh=True)


def clear_skills_cache() -> None:
    _skills_cache.clear()
