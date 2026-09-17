from backend.api import make_request



def get_player(account_id):
    return make_request(
        f"https://api.opendota.com/api/players/{account_id}"
    )


def prepare_player(data):
    profile = data.get("profile") or {}

    competitive_mmr = data.get("competitive_rank")
    turbo_mmr = data.get("mmr_estimate", {}).get("estimate")

    if competitive_mmr is not None:
        competitive_mmr = round(competitive_mmr)

    if turbo_mmr is not None:
        turbo_mmr = round(turbo_mmr)

    return {
        "nickname": profile.get("personaname", "Unknown"),
        "steam_id": str(profile.get("account_id", "")),
        "competitive_mmr": competitive_mmr,
        "turbo_mmr": turbo_mmr,
        "last_login": profile.get("last_login"),
    }
