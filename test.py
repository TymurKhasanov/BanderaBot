import asyncio
from pprint import pprint

from app.services.wiki_skills import get_skills


async def main() -> None:
    skills = await get_skills("13-necromancer")
    pprint(skills.get("Physical", [None])[0])


if __name__ == "__main__":
    asyncio.run(main())
