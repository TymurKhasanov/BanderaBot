import json
from functools import lru_cache
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mw2.wiki"

CACHE_DIR = Path("app/data/skills")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=None)
def get_skills(class_slug: str, force_refresh: bool = False):
    cache_file = CACHE_DIR / f"{class_slug}.json"

    if cache_file.exists() and not force_refresh:
        with cache_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    url = f"{BASE_URL}/lu4/class/{class_slug}/all"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    result = {}

    for accordion in soup.select(".accordion-item"):

        title = accordion.select_one(".accordion-header .mr-auto")

        if title is None:
            continue

        category = title.get_text(strip=True)

        result[category] = []

        for link in accordion.select(".accordion-body a[href*='/skill/']"):

            href = link.get("href")

            if not href:
                continue

            slug = href.rstrip("/").split("/")[-2]

            title = link.select_one(".item-name__content")

            if title:
                name = title.contents[0].strip()
            else:
                name = ""

            level_tag = link.select_one(".item-name__additional")
            level = (
                level_tag.get_text(strip=True)
                if level_tag
                else ""
            )

            description_tag = link.select_one(".skill_description")

            description = (
                description_tag.get_text("\n", strip=True)
                if description_tag
                else ""
            )

            result[category].append(
                {
                    "name": name,
                    "slug": slug,
                    "level": level,
                    "description": description,
                    "url": BASE_URL + href,
                }
            )

    with cache_file.open("w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2,
        )

    return result


def refresh_skills(class_slug: str):
    get_skills.cache_clear()
    return get_skills(class_slug, force_refresh=True)


def clear_skills_cache():
    get_skills.cache_clear()