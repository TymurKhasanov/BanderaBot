# app/services/wiki.py

import requests
from bs4 import BeautifulSoup

WIKI_URL = "https://masterwork.wiki/lu4/main"

EPICS = {
    "Core",
    "Queen Ant",
    "Orfen",
    "Zaken",
    "Baium",
    "Antharas",
    "Valakas",
}


def get_epics():
    response = requests.get(WIKI_URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    result = []

    for event in soup.select("a.calendar_event"):
        title = event.select_one(".calendar_event_title").get_text(strip=True)

        if title not in EPICS:
            continue

        date = event.select_one(".calendar_event_date span").get_text(strip=True)

        timestamp = event.select_one(".calendar_event_date span")["title"]

        url = event["href"]

        if url.startswith("/"):
            url = "https://masterwork.wiki" + url

        result.append({
            "name": title,
            "date": date,
            "timestamp": timestamp,
            "url": url,
        })

    return result