from typing import Any

from app.services.dcp_api import dcp_api


async def get_targets() -> list[dict[str, Any]]:
    return await dcp_api.get_targets()


async def get_rosters_with_targets() -> dict[str, dict[str, Any]]:
    targets = await get_targets()
    rosters: dict[str, dict[str, Any]] = {}

    for target in targets:
        for pack in target.get("packs", []):
            roster_id = pack.get("rosterId")
            roster_name = pack.get("rosterName")
            if roster_id is None or not roster_name:
                continue

            roster_key = str(roster_id)
            if roster_key not in rosters:
                rosters[roster_key] = {
                    "name": str(roster_name),
                    "targets": [],
                }

            rosters[roster_key]["targets"].append(
                {
                    "id": target.get("id"),
                    "enemy_clan": target.get("enemyClanName") or "Unknown",
                    "nickname": target.get("nickname") or "Unknown",
                    "character_class": target.get("characterClass") or "Unknown",
                    "composition": target.get("composition") or "Unknown",
                    "pack_kind": pack.get("packKind") or "Unknown",
                }
            )

    return rosters


async def get_roster_targets(roster_id: str) -> dict[str, Any] | None:
    rosters = await get_rosters_with_targets()
    return rosters.get(str(roster_id))
