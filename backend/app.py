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
}

def reset_state() -> None:
    state["time_index"] = 0
    state["area_weather"] = roll_weather()
    state["team"] = []
    state["box"] = []
    state["dex"] = set()


reset_state()


def roll_weather() -> Dict[str, str]:
    return {area["id"]: random.choice(WEATHER_TYPES) for area in AREAS}


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
    roll = random.randint(1, 100)
    success = roll <= bird.catch_rate
    if success:
        if bird_id not in state["dex"]:
            state["dex"].add(bird_id)
        if len(state["team"]) < 3:
            state["team"].append(bird_id)
            location = "team"
        else:
            state["box"].append(bird_id)
            location = "box"
    else:
        location = "escaped"
    return jsonify({"success": success, "location": location, "roll": roll})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
