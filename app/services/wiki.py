import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from playwright.async_api import Browser, Playwright, async_playwright


WIKI_URL = "https://masterwork.wiki/lu4-b-w-c/main"
WIKI_ORIGIN = "https://masterwork.wiki"
CACHE_SECONDS = 300
CACHE_FILE = Path(__file__).resolve().parents[1] / "data" / "epics_cache.json"

logger = logging.getLogger("banderabot")
_epics_cache: list[dict[str, Any]] = []
_cache_expires_at = 0.0
_cache_lock = asyncio.Lock()

EPICS = {
    "Core",
    "Queen Ant",
    "Orfen",
    "Zaken",
    "Baium",
    "Antharas",
    "Valakas",
}


async def _load_page(playwright: Playwright) -> str:
    browser: Browser = await playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-renderer-backgrounding",
            "--disable-background-timer-throttling",
            "--single-process",
            "--no-zygote",
            "--renderer-process-limit=1",
            "--js-flags=--max-old-space-size=128",
        ],
    )
    try:
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/141.0.0.0 Safari/537.36"
            ),
            viewport={"width": 800, "height": 600},
        )
        try:
            page = await context.new_page()
            response = await page.goto(
                WIKI_URL,
                wait_until="domcontentloaded",
                timeout=30_000,
            )
            if response is not None and response.status >= 500:
                raise RuntimeError(f"Wiki returned HTTP {response.status}")

            await page.wait_for_selector("a.calendar_event", timeout=20_000)
            return await page.content()
        finally:
            await context.close()
    finally:
        await browser.close()


def _read_disk_cache() -> list[dict[str, Any]]:
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (OSError, json.JSONDecodeError):
        logger.exception("Failed to read epic cache")
        return []
    return data if isinstance(data, list) else []


def _write_disk_cache(events: list[dict[str, Any]]) -> None:
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        temporary_file = CACHE_FILE.with_suffix(".tmp")
        temporary_file.write_text(
            json.dumps(events, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary_file.replace(CACHE_FILE)
    except OSError:
        logger.exception("Failed to persist epic cache")


async def get_epics() -> list[dict[str, Any]]:
    global _cache_expires_at, _epics_cache

    now = time.monotonic()
    if _epics_cache and now < _cache_expires_at:
        return [event.copy() for event in _epics_cache]

    async with _cache_lock:
        now = time.monotonic()
        if _epics_cache and now < _cache_expires_at:
            return [event.copy() for event in _epics_cache]

        try:
            async with async_playwright() as playwright:
                html = await _load_page(playwright)
        except Exception:
            cached = _epics_cache or _read_disk_cache()
            if cached:
                logger.exception("Live epic refresh failed; using cached calendar")
                return [event.copy() for event in cached]
            raise

        soup = BeautifulSoup(html, "html.parser")
        result: list[dict[str, Any]] = []

        for event in soup.select("a.calendar_event"):
            title_tag = event.select_one(".calendar_event_title")
            date_tag = event.select_one(".calendar_event_date span")
            if title_tag is None or date_tag is None:
                continue

            title = title_tag.get_text(strip=True)
            if title not in EPICS:
                continue

            href = event.get("href", "")
            url = (
                href
                if isinstance(href, str) and href.startswith("http")
                else f"{WIKI_ORIGIN}{href}"
            )
            result.append(
                {
                    "name": title,
                    "date": date_tag.get_text(strip=True),
                    "timestamp": date_tag.get("title", ""),
                    "url": url,
                }
            )

        if not result:
            raise RuntimeError("Wiki calendar did not contain supported epic events")

        _epics_cache = result
        _cache_expires_at = time.monotonic() + CACHE_SECONDS
        _write_disk_cache(result)
        return [event.copy() for event in result]
