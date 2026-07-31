import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mw2.wiki"


def get_classes():
    response = requests.get(
        f"{BASE_URL}/lu4/classes",
        timeout=10,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    races = {
        "human": [],
        "elf": [],
        "dark_elf": [],
        "orc": [],
        "dwarf": [],
    }

    race_map = {
        "race-0": "human",
        "race-1": "elf",
        "race-2": "dark_elf",
        "race-3": "orc",
        "race-4": "dwarf",
    }

    for race_div in soup.select("div.tab-pane"):
        race = race_map.get(race_div.get("id"))

        if not race:
            continue

        for link in race_div.select("a[href*='/class/']"):
            href = link["href"]

            slug = href.rstrip("/").split("/")[-1]

            races[race].append(
                {
                    "name": link.get_text(strip=True),
                    "slug": slug,
                    "url": BASE_URL + href,
                }
            )

    return races