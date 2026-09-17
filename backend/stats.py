def calculate_kda(kills, deaths, assists):
    safe_deaths = deaths if deaths > 0 else 1
    return round((kills + assists) / safe_deaths, 2)


def calculate_average_kda(matches):
    if not matches:
        return 0

    return round(
        sum(match["kda"] for match in matches) / len(matches),
        2,
    )


def get_best_and_worst_matches(matches):
    if not matches:
        return None, None

    best_match = max(matches, key=lambda match: match["kda"])
    worst_match = min(matches, key=lambda match: match["kda"])

    return best_match, worst_match
