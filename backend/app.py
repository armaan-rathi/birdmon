from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from typing import Dict, List

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


TIME_SLOTS = ["Dawn", "Midday", "Dusk", "Night"]
WEATHER_TYPES = ["Clear", "Overcast", "Rain", "Windy", "Fog"]


@dataclass
class Bird:
    id: str
    name: str
    category: str
    size: str
    habitats: List[str]
    active_times: List[str]
    weather: List[str]
    rarity: str
    temperament: str
    catch_rate: int
    traits: List[str]
    description: str
    stats: Dict[str, int]
    moves: List[Dict[str, object]]


BIRDS: List[Bird] = [
    Bird(
        id="northern-cardinal",
        name="Northern Cardinal",
        category="songbird",
        size="small",
        habitats=["woodland", "urban"],
        active_times=["Dawn", "Midday"],
        weather=["Clear", "Overcast"],
        rarity="common",
        temperament="bold",
        catch_rate=70,
        traits=["territorial", "melodic"],
        description="A vivid songbird that patrols clearings with sharp calls.",
        stats={
            "HP": 85,
            "Attack": 95,
            "Special Attack": 70,
            "Defense": 70,
            "Special Defense": 65,
            "Speed": 75,
        },
        moves=[
            {"name": "Scarlet Peck", "power": 70, "category": "physical"},
            {
                "name": "Sunburst Aria",
                "power": 0,
                "category": "special",
                "effect": "heal",
                "amount": 35,
            },
            {"name": "Wing Gust", "power": 65, "category": "physical"},
        ],
    ),
    Bird(
        id="great-blue-heron",
        name="Great Blue Heron",
        category="wader",
        size="large",
        habitats=["wetland"],
        active_times=["Dawn", "Dusk"],
        weather=["Clear", "Overcast", "Fog"],
        rarity="uncommon",
        temperament="patient",
        catch_rate=45,
        traits=["stillness", "piercing gaze"],
        description="A towering fisher that waits motionless before striking.",
        stats={
            "HP": 120,
            "Attack": 80,
            "Special Attack": 75,
            "Defense": 105,
            "Special Defense": 95,
            "Speed": 55,
        },
        moves=[
            {"name": "Harbor Spear", "power": 85, "category": "physical"},
            {"name": "Marsh Pulse", "power": 75, "category": "special"},
            {
                "name": "Stillwater Guard",
                "power": 0,
                "category": "special",
                "effect": "buff",
                "stat": "Defense",
                "amount": 20,
            },
        ],
    ),
    Bird(
        id="peregrine-falcon",
        name="Peregrine Falcon",
        category="raptor",
        size="medium",
        habitats=["cliff", "urban"],
        active_times=["Midday", "Dusk"],
        weather=["Clear", "Windy"],
        rarity="rare",
        temperament="fierce",
        catch_rate=25,
        traits=["aerial dive", "keen sight"],
        description="A swift raptor that dives like a bolt of lightning.",
        stats={
            "HP": 90,
            "Attack": 120,
            "Special Attack": 85,
            "Defense": 80,
            "Special Defense": 70,
            "Speed": 130,
        },
        moves=[
            {"name": "Sky Rend", "power": 95, "category": "physical"},
            {"name": "Thermal Strike", "power": 85, "category": "special"},
            {"name": "Stooping Dive", "power": 90, "category": "physical"},
        ],
    ),
    Bird(
        id="snowy-owl",
        name="Snowy Owl",
        category="raptor",
        size="large",
        habitats=["tundra"],
        active_times=["Night", "Dusk"],
        weather=["Clear", "Overcast", "Windy"],
        rarity="rare",
        temperament="silent",
        catch_rate=30,
        traits=["silent flight", "camouflage"],
        description="A pale hunter that blends with frost and shadow.",
        stats={
            "HP": 110,
            "Attack": 95,
            "Special Attack": 90,
            "Defense": 95,
            "Special Defense": 110,
            "Speed": 60,
        },
        moves=[
            {"name": "Frost Talon", "power": 85, "category": "physical"},
            {"name": "Moonlit Hex", "power": 90, "category": "special"},
            {"name": "Silent Glide", "power": 70, "category": "physical"},
        ],
    ),
    Bird(
        id="american-crow",
        name="American Crow",
        category="corvid",
        size="medium",
        habitats=["woodland", "urban", "farmland"],
        active_times=["Dawn", "Midday", "Dusk"],
        weather=["Clear", "Overcast", "Windy"],
        rarity="common",
        temperament="clever",
        catch_rate=60,
        traits=["mimicry", "problem-solving"],
        description="A clever corvid that remembers every encounter.",
        stats={
            "HP": 95,
            "Attack": 85,
            "Special Attack": 80,
            "Defense": 80,
            "Special Defense": 85,
            "Speed": 90,
        },
        moves=[
            {"name": "Caw Slash", "power": 75, "category": "physical"},
            {
                "name": "Riddle Cry",
                "power": 0,
                "category": "special",
                "effect": "buff",
                "stat": "Special Attack",
                "amount": 20,
            },
            {"name": "Shadow Feint", "power": 65, "category": "physical"},
        ],
    ),
    Bird(
        id="ruby-throated-hummingbird",
        name="Ruby-throated Hummingbird",
        category="nectar-feeder",
        size="tiny",
        habitats=["woodland", "garden"],
        active_times=["Dawn", "Midday"],
        weather=["Clear", "Overcast"],
        rarity="uncommon",
        temperament="hyper",
        catch_rate=50,
        traits=["hover", "iridescent"],
        description="A jewel that hovers in place and darts between flowers.",
        stats={
            "HP": 75,
            "Attack": 70,
            "Special Attack": 95,
            "Defense": 60,
            "Special Defense": 85,
            "Speed": 115,
        },
        moves=[
            {"name": "Nectar Beam", "power": 80, "category": "special"},
            {"name": "Ruby Jab", "power": 65, "category": "physical"},
            {
                "name": "Whirl Sip",
                "power": 0,
                "category": "special",
                "effect": "heal",
                "amount": 30,
            },
        ],
    ),
    Bird(
        id="belted-kingfisher",
        name="Belted Kingfisher",
        category="fisher",
        size="small",
        habitats=["wetland", "coast"],
        active_times=["Midday"],
        weather=["Clear", "Windy"],
        rarity="uncommon",
        temperament="alert",
        catch_rate=55,
        traits=["hover", "rattle call"],
        description="A fish hunter with a rattling call and sharp dives.",
        stats={
            "HP": 85,
            "Attack": 90,
            "Special Attack": 75,
            "Defense": 80,
            "Special Defense": 70,
            "Speed": 85,
        },
        moves=[
            {"name": "River Dart", "power": 80, "category": "physical"},
            {"name": "Rattle Shot", "power": 70, "category": "special"},
            {"name": "Splashline", "power": 65, "category": "physical"},
        ],
    ),
    Bird(
        id="scarlet-tanager",
        name="Scarlet Tanager",
        category="songbird",
        size="small",
        habitats=["woodland"],
        active_times=["Dawn", "Midday"],
        weather=["Clear"],
        rarity="rare",
        temperament="shy",
        catch_rate=35,
        traits=["canopy dweller", "bright plumage"],
        description="A flash of red high in the canopy, quick to vanish.",
        stats={
            "HP": 80,
            "Attack": 85,
            "Special Attack": 105,
            "Defense": 65,
            "Special Defense": 80,
            "Speed": 95,
        },
        moves=[
            {"name": "Crimson Pulse", "power": 90, "category": "special"},
            {"name": "Canopy Slice", "power": 75, "category": "physical"},
            {"name": "Sunflare Hymn", "power": 80, "category": "special"},
        ],
    ),
    Bird(
        id="osprey",
        name="Osprey",
        category="raptor",
        size="large",
        habitats=["coast", "wetland"],
        active_times=["Dawn", "Midday"],
        weather=["Clear", "Windy"],
        rarity="uncommon",
        temperament="focused",
        catch_rate=40,
        traits=["fish hunter", "hover dive"],
        description="A coastal hunter that locks onto fish with laser focus.",
        stats={
            "HP": 105,
            "Attack": 110,
            "Special Attack": 70,
            "Defense": 95,
            "Special Defense": 75,
            "Speed": 80,
        },
        moves=[
            {"name": "Harpoon Dive", "power": 90, "category": "physical"},
            {"name": "Salt Spray", "power": 70, "category": "special"},
            {"name": "Talon Clamp", "power": 75, "category": "physical"},
        ],
    ),
    Bird(
        id="sandhill-crane",
        name="Sandhill Crane",
        category="wader",
        size="large",
        habitats=["wetland", "farmland"],
        active_times=["Dawn", "Dusk"],
        weather=["Clear", "Overcast", "Fog"],
        rarity="uncommon",
        temperament="regal",
        catch_rate=45,
        traits=["trumpet call", "courtship dance"],
        description="A towering dancer whose calls echo across the marsh.",
        stats={
            "HP": 115,
            "Attack": 85,
            "Special Attack": 90,
            "Defense": 100,
            "Special Defense": 95,
            "Speed": 70,
        },
        moves=[
            {"name": "Marsh Waltz", "power": 80, "category": "special"},
            {"name": "Reed Lance", "power": 85, "category": "physical"},
            {
                "name": "Trumpet Shock",
                "power": 0,
                "category": "special",
                "effect": "buff",
                "stat": "Special Defense",
                "amount": 15,
            },
        ],
    ),
    Bird(
        id="bald-eagle",
        name="Bald Eagle",
        category="raptor",
        size="large",
        habitats=["coast", "woodland"],
        active_times=["Midday", "Dusk"],
        weather=["Clear", "Windy"],
        rarity="rare",
        temperament="dominant",
        catch_rate=30,
        traits=["soaring", "fearless"],
        description="A commanding raptor that surveys the land from above.",
        stats={
            "HP": 110,
            "Attack": 125,
            "Special Attack": 80,
            "Defense": 95,
            "Special Defense": 85,
            "Speed": 90,
        },
        moves=[
            {"name": "Liberty Strike", "power": 95, "category": "physical"},
            {"name": "Skybreaker", "power": 90, "category": "physical"},
            {"name": "Thunder Gaze", "power": 80, "category": "special"},
        ],
    ),
    Bird(
        id="pileated-woodpecker",
        name="Pileated Woodpecker",
        category="woodland",
        size="medium",
        habitats=["woodland"],
        active_times=["Dawn", "Midday"],
        weather=["Clear", "Overcast"],
        rarity="uncommon",
        temperament="relentless",
        catch_rate=55,
        traits=["drumming", "tree climber"],
        description="A powerful drummer that chisels resonant tree hollows.",
        stats={
            "HP": 90,
            "Attack": 110,
            "Special Attack": 70,
            "Defense": 85,
            "Special Defense": 70,
            "Speed": 85,
        },
        moves=[
            {"name": "Timber Strike", "power": 85, "category": "physical"},
            {"name": "Resonant Tap", "power": 70, "category": "special"},
            {"name": "Bark Split", "power": 80, "category": "physical"},
        ],
    ),
    Bird(
        id="barn-swallow",
        name="Barn Swallow",
        category="songbird",
        size="small",
        habitats=["farmland", "urban"],
        active_times=["Midday", "Dusk"],
        weather=["Clear", "Windy"],
        rarity="common",
        temperament="nimble",
        catch_rate=65,
        traits=["acrobat", "insect hunter"],
        description="A swift flier that skims fields with sharp turns.",
        stats={
            "HP": 80,
            "Attack": 75,
            "Special Attack": 80,
            "Defense": 65,
            "Special Defense": 70,
            "Speed": 115,
        },
        moves=[
            {"name": "Sky Stitch", "power": 70, "category": "physical"},
            {"name": "Jetstream", "power": 80, "category": "special"},
            {"name": "Needle Dive", "power": 75, "category": "physical"},
        ],
    ),
    Bird(
        id="red-tailed-hawk",
        name="Red-tailed Hawk",
        category="raptor",
        size="large",
        habitats=["woodland", "farmland"],
        active_times=["Midday", "Dusk"],
        weather=["Clear", "Windy", "Overcast"],
        rarity="uncommon",
        temperament="watchful",
        catch_rate=45,
        traits=["circling", "keen sight"],
        description="A patient hunter that circles fields before swooping in.",
        stats={
            "HP": 100,
            "Attack": 115,
            "Special Attack": 75,
            "Defense": 90,
            "Special Defense": 80,
            "Speed": 90,
        },
        moves=[
            {"name": "Thermal Dive", "power": 90, "category": "physical"},
            {"name": "Raptor Cry", "power": 75, "category": "special"},
            {"name": "Sky Talon", "power": 85, "category": "physical"},
        ],
    ),
    Bird(
        id="atlantic-puffin",
        name="Atlantic Puffin",
        category="seabird",
        size="small",
        habitats=["coast"],
        active_times=["Dawn", "Midday"],
        weather=["Clear", "Windy", "Overcast"],
        rarity="uncommon",
        temperament="playful",
        catch_rate=60,
        traits=["colorful beak", "diver"],
        description="A quirky cliff diver that rockets beneath the waves.",
        stats={
            "HP": 95,
            "Attack": 80,
            "Special Attack": 85,
            "Defense": 90,
            "Special Defense": 80,
            "Speed": 80,
        },
        moves=[
            {"name": "Cliff Skimmer", "power": 75, "category": "physical"},
            {"name": "Brine Burst", "power": 80, "category": "special"},
            {"name": "Pebble Peck", "power": 70, "category": "physical"},
        ],
    ),
    Bird(
        id="black-capped-chickadee",
        name="Black-capped Chickadee",
        category="songbird",
        size="tiny",
        habitats=["woodland", "urban"],
        active_times=["Dawn", "Midday"],
        weather=["Clear", "Overcast", "Windy"],
        rarity="common",
        temperament="curious",
        catch_rate=70,
        traits=["chirp", "caching"],
        description="A tiny explorer that chatters and hops between branches.",
        stats={
            "HP": 75,
            "Attack": 70,
            "Special Attack": 85,
            "Defense": 60,
            "Special Defense": 75,
            "Speed": 105,
        },
        moves=[
            {"name": "Chirp Dart", "power": 65, "category": "special"},
            {"name": "Seed Flick", "power": 70, "category": "physical"},
            {"name": "Quickstep", "power": 75, "category": "physical"},
        ],
    ),
    Bird(
        id="prairie-falcon",
        name="Prairie Falcon",
        category="raptor",
        size="medium",
        habitats=["cliff", "farmland"],
        active_times=["Midday", "Dusk"],
        weather=["Clear", "Windy"],
        rarity="rare",
        temperament="restless",
        catch_rate=30,
        traits=["wind rider", "swift dive"],
        description="A desert sprinter that thrives on rushing winds.",
        stats={
            "HP": 90,
            "Attack": 110,
            "Special Attack": 80,
            "Defense": 80,
            "Special Defense": 75,
            "Speed": 115,
        },
        moves=[
            {"name": "Sirocco Dive", "power": 90, "category": "physical"},
            {"name": "Sandflash", "power": 80, "category": "special"},
            {"name": "Horizon Slash", "power": 85, "category": "physical"},
        ],
    ),
    Bird(
        id="common-loon",
        name="Common Loon",
        category="seabird",
        size="large",
        habitats=["wetland", "coast"],
        active_times=["Dusk", "Night"],
        weather=["Clear", "Fog", "Overcast"],
        rarity="rare",
        temperament="mystic",
        catch_rate=35,
        traits=["haunting call", "deep diver"],
        description="A midnight diver whose calls echo across glassy water.",
        stats={
            "HP": 110,
            "Attack": 85,
            "Special Attack": 110,
            "Defense": 95,
            "Special Defense": 95,
            "Speed": 60,
        },
        moves=[
            {"name": "Echo Spiral", "power": 90, "category": "special"},
            {"name": "Midnight Dive", "power": 85, "category": "physical"},
            {
                "name": "Lakeglow",
                "power": 0,
                "category": "special",
                "effect": "heal",
                "amount": 40,
            },
        ],
    ),
]


AREAS = [
    {
        "id": "whispering-woods",
        "name": "Whispering Woods",
        "habitats": ["woodland", "garden"],
        "icon": "🌲",
        "background": "forest",
    },
    {
        "id": "mirror-marsh",
        "name": "Mirror Marsh",
        "habitats": ["wetland"],
        "icon": "🪷",
        "background": "wetland",
    },
    {
        "id": "sunset-cliffs",
        "name": "Sunset Cliffs",
        "habitats": ["cliff", "coast"],
        "icon": "⛰️",
        "background": "cliff",
    },
    {
        "id": "city-canopy",
        "name": "City Canopy",
        "habitats": ["urban"],
        "icon": "🏙️",
        "background": "urban",
    },
]


state: Dict[str, object] = {
    "time_index": 0,
    "area_weather": {},
    "team": [],
    "box": [],
    "dex": set(),
    "levels": {},
    "net_attempts": 0,
}

def roll_weather() -> Dict[str, str]:
    return {area["id"]: random.choice(WEATHER_TYPES) for area in AREAS}


def reset_state() -> None:
    state["time_index"] = 0
    state["area_weather"] = roll_weather()
    state["team"] = []
    state["box"] = []
    state["dex"] = set()
    state["levels"] = {}
    state["net_attempts"] = 0


reset_state()


def build_state_payload() -> Dict[str, object]:
    return {
        "time_slot": TIME_SLOTS[state["time_index"]],
        "areas": [
            {
                **area,
                "weather": state["area_weather"].get(area["id"], "Clear"),
            }
            for area in AREAS
        ],
    }


def bird_to_dict(bird: Bird) -> Dict[str, object]:
    return asdict(bird)


def eligible_birds(area_id: str) -> List[Bird]:
    area = next((area for area in AREAS if area["id"] == area_id), None)
    if not area:
        return []
    time_slot = TIME_SLOTS[state["time_index"]]
    weather = state["area_weather"].get(area_id, "Clear")
    birds = [
        bird
        for bird in BIRDS
        if time_slot in bird.active_times
        and weather in bird.weather
        and any(habitat in bird.habitats for habitat in area["habitats"])
    ]
    random.shuffle(birds)
    return birds[:5]


@app.get("/api/state")
def get_state():
    return jsonify(build_state_payload())


@app.post("/api/advance-time")
def advance_time():
    state["time_index"] = (state["time_index"] + 1) % len(TIME_SLOTS)
    state["area_weather"] = roll_weather()
    state["net_attempts"] = 0
    return jsonify(build_state_payload())


@app.post("/api/reset")
def reset():
    reset_state()
    return jsonify(build_state_payload())


@app.get("/api/birds")
def list_birds():
    return jsonify([bird_to_dict(bird) for bird in BIRDS])


@app.get("/api/player")
def player_state():
    return jsonify(
        {
            "team": state["team"],
            "box": state["box"],
            "dex": list(state["dex"]),
            "levels": state["levels"],
        }
    )


@app.get("/api/expedition")
def expedition():
    area_id = request.args.get("area")
    if not area_id:
        return jsonify({"error": "area is required"}), 400
    area = next((area for area in AREAS if area["id"] == area_id), None)
    if not area:
        return jsonify({"error": "area not found"}), 404
    birds = eligible_birds(area_id)
    return jsonify(
        {
            "area": area,
            "weather": state["area_weather"].get(area_id, "Clear"),
            "time_slot": TIME_SLOTS[state["time_index"]],
            "birds": [bird_to_dict(bird) for bird in birds],
        }
    )


@app.post("/api/capture")
def capture():
    payload = request.get_json(silent=True) or {}
    bird_id = payload.get("birdId")
    bird = next((bird for bird in BIRDS if bird.id == bird_id), None)
    if not bird:
        return jsonify({"error": "bird not found"}), 404
    state["net_attempts"] = int(state.get("net_attempts", 0)) + 1
    roll = random.randint(1, 100)
    success = roll <= bird.catch_rate
    if success:
        if bird_id not in state["dex"]:
            state["dex"].add(bird_id)
        state["levels"].setdefault(bird_id, 1)
        if len(state["team"]) < 3:
            state["team"].append(bird_id)
            location = "team"
        else:
            state["box"].append(bird_id)
            location = "box"
    else:
        location = "escaped"
    return jsonify(
        {
            "success": success,
            "location": location,
            "roll": roll,
            "net_attempts": state["net_attempts"],
        }
    )


@app.post("/api/release")
def release():
    payload = request.get_json(silent=True) or {}
    bird_id = payload.get("birdId")
    if not bird_id:
        return jsonify({"error": "birdId is required"}), 400
    if bird_id in state["box"]:
        state["box"].remove(bird_id)
    else:
        return jsonify({"error": "bird not in box"}), 404
    if bird_id not in state["team"] and bird_id not in state["box"]:
        state["levels"].pop(bird_id, None)
    return jsonify(
        {
            "team": state["team"],
            "box": state["box"],
            "dex": list(state["dex"]),
            "levels": state["levels"],
        }
    )


@app.post("/api/battle/start")
def battle_start():
    payload = request.get_json(silent=True) or {}
    player_bird_id = payload.get("birdId")
    player_bird = next((bird for bird in BIRDS if bird.id == player_bird_id), None)
    if not player_bird:
        return jsonify({"error": "player bird not found"}), 404
    if player_bird_id not in state["team"]:
        return jsonify({"error": "bird not in team"}), 400
    opponent = random.choice(BIRDS)
    return jsonify(
        {
            "player": bird_to_dict(player_bird),
            "opponent": bird_to_dict(opponent),
            "player_level": state["levels"].get(player_bird_id, 1),
        }
    )


@app.post("/api/level-up")
def level_up():
    payload = request.get_json(silent=True) or {}
    bird_id = payload.get("birdId")
    if not bird_id:
        return jsonify({"error": "birdId is required"}), 400
    current_level = state["levels"].get(bird_id, 1)
    state["levels"][bird_id] = current_level + 1
    return jsonify({"birdId": bird_id, "level": state["levels"][bird_id]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
