const input = document.getElementById("account-id")
const button = document.getElementById("search-button")

const playerOverview =
    document.getElementById("player-overview")

const heroesTrack =
    document.getElementById("heroes-track")

const matchesList =
    document.getElementById("matches-list")

const bestMatchContainer =
    document.getElementById("best-match")

const worstMatchContainer =
    document.getElementById("worst-match")

const statusMessage =
    document.getElementById("status-message")

const heroesPrev =
    document.getElementById("heroes-prev")

const heroesNext =
    document.getElementById("heroes-next")

const matches_value = 
    document.getElementById("last-matches-value")

const showMoreMatchButton = document.getElementById("show-more-matches")


const API_URL = ""


const HERO_ALIASES = {
    "Anti-Mage": "antimage",
    "Outworld Destroyer": "obsidian_destroyer",
    "Windranger": "windrunner",
    "Necrophos": "necrolyte",
    "Clockwerk": "rattletrap",
    "Nature's Prophet": "furion",
    "Queen of Pain": "queenofpain",
    "Wraith King": "skeleton_king",
    "Zeus": "zuus",
    "Io": "wisp",
    "Timbersaw": "shredder",
    "Underlord": "abyssal_underlord",
    "Centaur Warrunner": "centaur",
    "Doom": "doom_bringer",
    "Lifestealer": "life_stealer",
    "Magnus": "magnataur",
    "Treant Protector": "treant",
    "Shadow Fiend": "nevermore",
    "Vengeful Spirit": "vengefulspirit"
}


function getHeroImageByName(heroName) {

    if (!heroName) {
        return ""
    }

    const internalName =
        HERO_ALIASES[heroName] ||
        heroName
            .toLowerCase()
            .replace(/'/g, "")
            .replace(/-/g, "_")
            .replace(/\s+/g, "_")

    return (
        "https://cdn.cloudflare.steamstatic.com" +
        `/apps/dota2/images/dota_react/heroes/${internalName}.png`
    )
}


function getMatchImage(match) {

    if (match.image) {
        return match.image
    }

    return getHeroImageByName(match.hero_name)
}


function formatKda(value) {

    const number = Number(value)

    if (Number.isNaN(number)) {
        return "0.00"
    }

    return number.toFixed(2)
}


function isWin(result) {

    return String(result)
        .toLowerCase()
        .includes("поб")
}


function setLoading(loading) {

    button.disabled = loading

    button.textContent =
        loading
            ? "Loading..."
            : "Search"
}


function showError(message) {

    statusMessage.textContent = message
    statusMessage.hidden = false

    setTimeout(() => {
        statusMessage.hidden = true
    }, 5000)
}


function renderPlayer(data) {

    playerOverview.classList.remove("empty-state")

    playerOverview.innerHTML = `

        <div class="player-top">

            <div class="player-avatar">
                <img
                    src="${getHeroImageByName(
                        data.heroes?.[0]?.hero_name || "Invoker"
                    )}"
                    alt=""
                >
            </div>

            <div class="player-meta">

                <h2>
                    ${data.player.nickname}
                </h2>

                <p>
                    STEAM ID:
                    ${data.player.steam_id}
                </p>

            </div>

        </div>


        <div class="player-stats">

            <div class="stat-box">

                <strong>
                    ${data.winrate.winrate}%
                </strong>

                <span>
                    Winrate
                </span>

            </div>


            <div class="stat-box">

                <strong>
                    ${data.winrate.games}
                </strong>

                <span>
                    Matches
                </span>

            </div>


            <div class="stat-box">

                <strong>
                    ${formatKda(data.average_kda)}
                </strong>

                <span>
                    Average KDA
                </span>

            </div>

        </div>
    `
}


function renderHeroes(heroes) {

    if (!heroes || heroes.length === 0) {

        heroesTrack.innerHTML =
            '<div class="loading-card">No hero statistics found</div>'

        return
    }


    heroesTrack.innerHTML =
        heroes
            .map(hero => `

                <article class="hero-card">

                    <div class="hero-image-wrap">

                        <img
                            class="hero-image"
                            src="${
                                hero.image ||
                                getHeroImageByName(hero.hero_name)
                            }"
                            alt="${hero.hero_name}"
                            loading="lazy"
                        >

                    </div>


                    <div class="hero-card-body">

                        <h3>
                            ${hero.hero_name}
                        </h3>

                        <p>
                            ${hero.games} games ·
                            ${hero.wins} wins
                        </p>

                        <p class="hero-winrate">
                            ${hero.winrate}% WR
                        </p>

                    </div>

                </article>
            `)
            .join("")
}

let visibleMatches = 10
function renderMatches(matches) {

    if (!matches || matches.length === 0) {

        matchesList.innerHTML =
            '<div class="loading-card">No recent matches found</div>'

        return
    }


    matchesList.innerHTML =
        matches.slice(0,visibleMatches)
            .map(match => `

                <article class="match-row">

                    <div class="match-hero">

                        <div class="match-hero-image">

                            <img
                                src="${getMatchImage(match)}"
                                alt="${match.hero_name}"
                                loading="lazy"
                            >

                        </div>


                        <div class="match-hero-name">
                            ${match.hero_name}
                        </div>

                    </div>


                    <div
                        class="
                            result-pill
                            ${isWin(match.result) ? "win" : "loss"}
                        "
                    >
                        ${match.result}
                    </div>


                    <div class="match-kda-line">

                        ${match.kills}
                        /
                        ${match.deaths}
                        /
                        ${match.assists}

                    </div>


                    <div class="match-rating">

                        KDA
                        ${formatKda(match.kda)}

                    </div>


                    <div class="match-id">

                        Match ID:
                        ${match.match_id}

                    </div>

                </article>
            `)
            .join("")
        if (visibleMatches>=matches.length) {
            showMoreMatchButton.hidden = true
        } else {
            showMoreMatchButton.hidden = false
        }
}


function renderHighlight(match, type) {

    const isBest = type === "best"

    const title =
        isBest
            ? "🏆 Best Match"
            : "☠ Worst Match"


    if (!match) {

        return `
            <div class="loading-card">
                ${title} is unavailable
            </div>
        `
    }


    return `

        <h2 class="highlight-title">
            ${title}
        </h2>


        <div class="highlight-content">

            <div class="highlight-image">

                <img
                    src="${getMatchImage(match)}"
                    alt="${match.hero_name}"
                >

            </div>


            <div class="highlight-info">

                <h3>
                    ${match.hero_name}
                </h3>


                <span
                    class="
                        result-pill
                        ${isWin(match.result) ? "win" : "loss"}
                    "
                >
                    ${match.result}
                </span>


                <p class="big-kda">

                    ${match.kills}
                    /
                    ${match.deaths}
                    /
                    ${match.assists}

                </p>


                <p>
                    KDA
                    ${formatKda(match.kda)}
                </p>


                <p>
                    Match ID:
                    ${match.match_id}
                </p>

            </div>

        </div>
    `
}

let current_matches = []
async function loadPlayer() {

    const accountID =
        input.value.trim()


    if (!accountID) {

        showError(
            "Enter Steam Account ID"
        )

        return
    }
    visibleMatches = 10


    setLoading(true)


    try {

        const response =
            await fetch(
                `${API_URL}/summary/${encodeURIComponent(accountID)}?count=${matches_value.value}`
            )


        const data =
            await response.json()


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to load player statistics"
            )
        }


        renderPlayer(data)

        renderHeroes(data.heroes)

        current_matches = data.recent_matches
        renderMatches(current_matches)

        bestMatchContainer.innerHTML =
            renderHighlight(
                data.best_match,
                "best"
            )


        worstMatchContainer.innerHTML =
            renderHighlight(
                data.worst_match,
                "worst"
            )

    } catch (error) {

        console.error(error)

        showError(
            error.message ||
            "Unable to connect to backend"
        )

    } finally {

        setLoading(false)
    }
}


button.addEventListener(
    "click",
    loadPlayer
)


input.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {
            loadPlayer()
        }

    }
)


heroesPrev.addEventListener(
    "click",
    () => {

        heroesTrack.scrollBy({
            left: -600,
            behavior: "smooth"
        })

    }
)


heroesNext.addEventListener(
    "click",
    () => {

        heroesTrack.scrollBy({
            left: 600,
            behavior: "smooth"
        })

    }
)
showMoreMatchButton.addEventListener(
    "click",
    ()=> {
        visibleMatches += 10
        renderMatches(current_matches)
        console.log("visible:",visibleMatches)
        console.log("all_matches", current_matches.length)
    }
)
