import aiohttp
from bs4 import BeautifulSoup


BASE_URL = "https://mw2.wiki"


async def get_classes() -> dict[str, list[dict[str, str]]]:
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(f"{BASE_URL}/lu4/classes") as response:
            response.raise_for_status()
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    races: dict[str, list[dict[str, str]]] = {
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
        race = race_map.get(str(race_div.get("id", "")))
        if not race:
            continue

        for link in race_div.select("a[href*='/class/']"):
            href = link.get("href")
            if not isinstance(href, str):
                continue
            races[race].append(
                {
                    "name": link.get_text(strip=True),
                    "slug": href.rstrip("/").split("/")[-1],
                    "url": f"{BASE_URL}{href}",
                }
            )

    return races
