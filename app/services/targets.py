from app.services.dcp_api import dcp_api


def get_targets() -> list:
    return dcp_api.get_targets()


def get_rosters_with_targets() -> dict:
    targets = get_targets()

    rosters = {}

    for target in targets:
        for pack in target.get("packs", []):
            roster_id = pack.get("rosterId")
            roster_name = pack.get("rosterName")
            pack_kind = pack.get("packKind")

            if not roster_id or not roster_name:
                continue

            if roster_id not in rosters:
                rosters[roster_id] = {
                    "name": roster_name,
                    "targets": [],
                }

            rosters[roster_id]["targets"].append(
                {
                    "id": target.get("id"),
                    "enemy_clan": target.get(
                        "enemyClanName",
                        "Unknown",
                    ),
                    "nickname": target.get(
                        "nickname",
                        "Unknown",
                    ),
                    "character_class": target.get(
                        "characterClass",
                        "Unknown",
                    ),
                    "composition": target.get(
                        "composition",
                        "Unknown",
                    ),
                    "pack_kind": pack_kind or "Unknown",
                }
            )

    return rosters


def get_roster_targets(roster_id: str) -> dict | None:
    rosters = get_rosters_with_targets()

    return rosters.get(roster_id)