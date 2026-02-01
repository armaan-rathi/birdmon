import { useEffect, useMemo, useState } from "react";

const backgroundThemes = {
  forest: "linear-gradient(180deg, #b6e3a1 0%, #6abf69 100%)",
  wetland: "linear-gradient(180deg, #b8e4f0 0%, #5aa6c2 100%)",
  cliff: "linear-gradient(180deg, #f6caa5 0%, #c7875b 100%)",
  urban: "linear-gradient(180deg, #d5d7e0 0%, #7f8799 100%)"
};

const birdIcons = {
  "northern-cardinal": "🐦",
  "great-blue-heron": "🪿",
  "peregrine-falcon": "🦅",
  "snowy-owl": "🦉",
  "american-crow": "🐦‍⬛",
  "ruby-throated-hummingbird": "🐤",
  "belted-kingfisher": "🐦",
  "scarlet-tanager": "🐦"
};

const weatherIcons = {
  Clear: "☀️",
  Overcast: "☁️",
  Rain: "🌧️",
  Windy: "🌬️",
  Fog: "🌫️"
};

const timeBadges = {
  Dawn: "🌅",
  Midday: "🌞",
  Dusk: "🌇",
  Night: "🌙"
};

function StatPill({ label, value }) {
  return (
    <span className="stat-pill">
      <strong>{label}:</strong> {value}
    </span>
  );
}

export default function App() {
  const [state, setState] = useState(null);
  const [birds, setBirds] = useState([]);
  const [player, setPlayer] = useState({ team: [], box: [], dex: [] });
  const [selectedArea, setSelectedArea] = useState(null);
  const [expedition, setExpedition] = useState(null);
  const [message, setMessage] = useState("");
  const [showDex, setShowDex] = useState(false);

  const teamBirds = useMemo(
    () => player.team.map((id) => birds.find((bird) => bird.id === id)),
    [player.team, birds]
  );

  const boxBirds = useMemo(
    () => player.box.map((id) => birds.find((bird) => bird.id === id)),
    [player.box, birds]
  );

  useEffect(() => {
    Promise.all([fetch("/api/state"), fetch("/api/birds"), fetch("/api/player")])
      .then(async ([stateRes, birdsRes, playerRes]) => {
        const [stateData, birdData, playerData] = await Promise.all([
          stateRes.json(),
          birdsRes.json(),
          playerRes.json()
        ]);
        setState(stateData);
        setBirds(birdData);
        setPlayer(playerData);
      })
      .catch(() => {
        setMessage("Unable to reach the Aviary server.");
      });
  }, []);

  const handleAdvanceTime = async () => {
    const response = await fetch("/api/advance-time", { method: "POST" });
    const data = await response.json();
    setState(data);
    setSelectedArea(null);
    setExpedition(null);
    setMessage("New time slot rolled with fresh weather patterns.");
  };

  const handleReset = async () => {
    const response = await fetch("/api/reset", { method: "POST" });
    const data = await response.json();
    setState(data);
    setSelectedArea(null);
    setExpedition(null);
    setPlayer({ team: [], box: [], dex: [] });
    setMessage("Fieldwork reset. Your team is back at HQ.");
  };

  const handleSelectArea = async (area) => {
    setSelectedArea(area);
    const response = await fetch(`/api/expedition?area=${area.id}`);
    const data = await response.json();
    setExpedition(data);
    setMessage("Prepare the net! Birds are circling the habitat.");
  };

  const handleCapture = async (bird) => {
    const response = await fetch("/api/capture", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ birdId: bird.id })
    });
    const result = await response.json();
    if (result.success) {
      const playerRes = await fetch("/api/player");
      const playerData = await playerRes.json();
      setPlayer(playerData);
      setMessage(
        `${bird.name} was caught and sent to your ${result.location}!`
      );
    } else {
      setMessage(`${bird.name} dodged the net and flew away.`);
    }
  };

  const caughtLookup = new Set(player.dex);

  return (
    <div className="app">
      <header className="top-bar">
        <div>
          <h1>Birdmon Expedition Deck</h1>
          <p className="subtitle">
            Track habitats, set your time slot, and net your new companions.
          </p>
        </div>
        <div className="time-pill">
          <span>{timeBadges[state?.time_slot] ?? "⏳"}</span>
          <div>
            <div className="time-label">Current Time</div>
            <div className="time-slot">{state?.time_slot ?? "Loading"}</div>
          </div>
        </div>
        <div className="top-actions">
          <button className="primary" onClick={() => setShowDex(true)}>
            Open Bird-Dex
          </button>
          <button className="secondary" onClick={handleAdvanceTime}>
            Advance Time
          </button>
          <button className="tertiary" onClick={handleReset}>
            Reset Fieldwork
          </button>
        </div>
      </header>

      {message && <div className="message">{message}</div>}

      <main className="main-grid">
        <section className="panel">
          <h2>Map Overview</h2>
          <div className="map-grid">
            {state?.areas?.map((area) => (
              <button
                key={area.id}
                className={`area-card ${
                  selectedArea?.id === area.id ? "active" : ""
                }`}
                onClick={() => handleSelectArea(area)}
              >
                <div className="area-icon">{area.icon}</div>
                <div>
                  <div className="area-name">{area.name}</div>
                  <div className="area-weather">
                    {weatherIcons[area.weather] ?? "❔"} {area.weather}
                  </div>
                </div>
                <div className="area-hover">
                  <strong>Habitats</strong>
                  <div>{area.habitats.join(", ")}</div>
                  <strong>Weather</strong>
                  <div>{area.weather}</div>
                </div>
              </button>
            ))}
          </div>
        </section>

        <section className="panel">
          <h2>Team & Storage</h2>
          <div className="team-grid">
            {teamBirds.length === 0 && (
              <p className="muted">No birds in your team yet.</p>
            )}
            {teamBirds.map((bird) => (
              <div key={bird.id} className="bird-card">
                <div className="bird-icon">{birdIcons[bird.id]}</div>
                <div>
                  <div className="bird-name">{bird.name}</div>
                  <StatPill label="Type" value={bird.category} />
                </div>
              </div>
            ))}
          </div>
          <div className="box-panel">
            <h3>Storage Box</h3>
            {boxBirds.length === 0 && (
              <p className="muted">No extras stored yet.</p>
            )}
            <div className="box-grid">
              {boxBirds.map((bird) => (
                <span key={bird.id} className="box-item">
                  {birdIcons[bird.id]} {bird.name}
                </span>
              ))}
            </div>
          </div>
        </section>
      </main>

      <section className="expedition">
        <div className="expedition-header">
          <h2>
            {expedition?.area?.name ?? "Choose a habitat for expedition"}
          </h2>
          <span className="expedition-meta">
            {expedition
              ? `${expedition.time_slot} · ${expedition.weather}`
              : "Awaiting selection"}
          </span>
        </div>
        <div
          className="expedition-scene"
          style={{
            background:
              backgroundThemes[expedition?.area?.background] ||
              "linear-gradient(180deg, #d6e7ff 0%, #9cb1d9 100%)"
          }}
        >
          {expedition?.birds?.length ? (
            <div className="bird-swarm">
              {expedition.birds.map((bird, index) => (
                <div
                  key={bird.id}
                  className="bird-sprite"
                  style={{
                    top: `${15 + index * 10}%`,
                    left: `${10 + (index * 18) % 70}%`
                  }}
                >
                  <div className="bird-sprite-icon">{birdIcons[bird.id]}</div>
                  <div className="bird-sprite-name">{bird.name}</div>
                  <button
                    className="net-button"
                    onClick={() => handleCapture(bird)}
                  >
                    Throw Net
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-expedition">
              Select an area to see birds appear here.
            </div>
          )}
        </div>
      </section>

      {showDex && (
        <div className="modal">
          <div className="modal-card">
            <div className="modal-header">
              <h2>Bird-Dex</h2>
              <button onClick={() => setShowDex(false)}>Close</button>
            </div>
            <div className="dex-grid">
              {birds.map((bird) => (
                <div
                  key={bird.id}
                  className={`dex-card ${
                    caughtLookup.has(bird.id) ? "caught" : ""
                  }`}
                >
                  <div className="dex-top">
                    <span className="dex-icon">{birdIcons[bird.id]}</span>
                    <div>
                      <div className="bird-name">{bird.name}</div>
                      <div className="bird-category">{bird.category}</div>
                    </div>
                  </div>
                  <div className="dex-meta">
                    <StatPill label="Size" value={bird.size} />
                    <StatPill label="Rarity" value={bird.rarity} />
                    <StatPill label="Temper" value={bird.temperament} />
                  </div>
                  <div className="dex-description">{bird.description}</div>
                  <div className="dex-tags">
                    <StatPill label="Habitats" value={bird.habitats.join(", ")} />
                    <StatPill
                      label="Active"
                      value={bird.active_times.join(", ")}
                    />
                    <StatPill label="Weather" value={bird.weather.join(", ")} />
                    <StatPill label="Traits" value={bird.traits.join(", ")} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
