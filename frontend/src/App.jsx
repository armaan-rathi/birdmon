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
  "scarlet-tanager": "🐦",
  osprey: "🦅",
  "sandhill-crane": "🪿",
  "bald-eagle": "🦅",
  "pileated-woodpecker": "🪵",
  "barn-swallow": "🐦",
  "red-tailed-hawk": "🦅",
  "atlantic-puffin": "🪿",
  "black-capped-chickadee": "🐦",
  "prairie-falcon": "🦅",
  "common-loon": "🦢"
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

function getBirdIcon(birdId) {
  return birdIcons[birdId] ?? "🐦";
}

export default function App() {
  const [state, setState] = useState(null);
  const [birds, setBirds] = useState([]);
  const [player, setPlayer] = useState({
    team: [],
    box: [],
    dex: [],
    levels: {}
  });
  const [selectedArea, setSelectedArea] = useState(null);
  const [expedition, setExpedition] = useState(null);
  const [message, setMessage] = useState("");
  const [showDex, setShowDex] = useState(false);
  const [captureFeedback, setCaptureFeedback] = useState(null);
  const [captureModal, setCaptureModal] = useState(null);
  const [timeAdvanceNotice, setTimeAdvanceNotice] = useState(false);
  const [battle, setBattle] = useState(null);
  const [battleLog, setBattleLog] = useState([]);
  const [battleStatus, setBattleStatus] = useState("idle");
  const [battleHighlight, setBattleHighlight] = useState(null);
  const [selectedBattleBird, setSelectedBattleBird] = useState("");
  const [battleTurn, setBattleTurn] = useState("player");

  const teamBirds = useMemo(
    () =>
      player.team
        .map((id) => birds.find((bird) => bird.id === id))
        .filter(Boolean),
    [player.team, birds]
  );

  const boxBirds = useMemo(
    () =>
      player.box
        .map((id) => birds.find((bird) => bird.id === id))
        .filter(Boolean),
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
    setCaptureFeedback(null);
    setCaptureModal(null);
    setMessage("New time slot rolled with fresh weather patterns.");
  };

  const handleReset = async () => {
    const response = await fetch("/api/reset", { method: "POST" });
    const data = await response.json();
    setState(data);
    setSelectedArea(null);
    setExpedition(null);
    setPlayer({ team: [], box: [], dex: [], levels: {} });
    setCaptureFeedback(null);
    setCaptureModal(null);
    setMessage("Fieldwork reset. Your team is back at HQ.");
  };

  const handleSelectArea = async (area) => {
    setSelectedArea(area);
    const response = await fetch(`/api/expedition?area=${area.id}`);
    const data = await response.json();
    setExpedition(data);
    setCaptureFeedback(null);
    setCaptureModal(null);
    setMessage("Prepare the net! Birds are circling the habitat.");
  };

  const autoAdvanceTime = async () => {
    setTimeAdvanceNotice(true);
    const response = await fetch("/api/advance-time", { method: "POST" });
    const data = await response.json();
    setTimeout(() => {
      setTimeAdvanceNotice(false);
    }, 1200);
    setState(data);
    setSelectedArea(null);
    setExpedition(null);
    setCaptureFeedback(null);
    setCaptureModal(null);
    setMessage("Time advanced after repeated net throws.");
  };

  const handleCapture = async (bird) => {
    const response = await fetch("/api/capture", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ birdId: bird.id })
    });
    const result = await response.json();
    setCaptureFeedback({ id: bird.id, success: result.success });
    setCaptureModal({
      name: bird.name,
      success: result.success,
      location: result.location
    });
    if (result.success) {
      const playerRes = await fetch("/api/player");
      const playerData = await playerRes.json();
      setPlayer(playerData);
    } else {
      setMessage("");
    }
    if (result.net_attempts && result.net_attempts % 3 === 0) {
      await autoAdvanceTime();
    }
  };

  const handleRelease = async (birdId) => {
    const response = await fetch("/api/release", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ birdId })
    });
    const data = await response.json();
    setPlayer(data);
    setMessage("Bird released back into the wild.");
  };

  const calculateDamage = (move, attacker, defender) => {
    const attackStat =
      move.category === "special"
        ? attacker.stats["Special Attack"]
        : attacker.stats["Attack"];
    const defenseStat =
      move.category === "special"
        ? defender.stats["Special Defense"]
        : defender.stats["Defense"];
    const base = move.power + attackStat * 0.6 - defenseStat * 0.35;
    const variance = 0.85 + Math.random() * 0.3;
    return Math.max(8, Math.floor(base * variance));
  };

  const handleCpuMove = (currentBattle, updatedOpponentHp) => {
    if (!currentBattle) {
      return;
    }
    const opponentMove =
      currentBattle.opponent.moves[
        Math.floor(Math.random() * currentBattle.opponent.moves.length)
      ];
    const damageToPlayer = calculateDamage(
      opponentMove,
      currentBattle.opponent,
      currentBattle.player
    );
    const playerHp = Math.max(0, currentBattle.playerHp - damageToPlayer);
    setBattleHighlight("opponent");
    setBattleLog((logs) => [
      `${currentBattle.opponent.name} used ${opponentMove.name} (${damageToPlayer})!`,
      ...logs
    ]);
    const nextBattle = {
      ...currentBattle,
      opponentHp: updatedOpponentHp,
      playerHp
    };
    setBattle(nextBattle);
    if (playerHp === 0) {
      setBattleStatus("lost");
      setBattleHighlight("player");
      return;
    }
    setBattleTurn("player");
  };

  const handlePlayerMove = (move) => {
    if (!battle || battleStatus !== "in-progress" || battleTurn !== "player") {
      return;
    }
    const damageToOpponent = calculateDamage(
      move,
      battle.player,
      battle.opponent
    );
    const opponentHp = Math.max(0, battle.opponentHp - damageToOpponent);
    setBattleHighlight("player");
    setBattleLog((logs) => [
      `${battle.player.name} used ${move.name} (${damageToOpponent})!`,
      ...logs
    ]);
    const nextBattle = {
      ...battle,
      opponentHp
    };
    setBattle(nextBattle);
    if (opponentHp === 0) {
      setBattleStatus("won");
      setBattleHighlight("opponent");
      fetch("/api/level-up", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ birdId: battle.player.id })
      })
        .then((res) => res.json())
        .then((data) => {
          setPlayer((prev) => ({
            ...prev,
            levels: { ...prev.levels, [data.birdId]: data.level }
          }));
        });
      return;
    }
    setBattleTurn("cpu");
    setTimeout(() => handleCpuMove(nextBattle, opponentHp), 900);
  };

  const handleStartBattle = async () => {
    if (!selectedBattleBird) {
      setMessage("Choose a bird from your team to start a battle.");
      return;
    }
    setCaptureFeedback(null);
    const response = await fetch("/api/battle/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ birdId: selectedBattleBird })
    });
    const data = await response.json();
    if (data.error) {
      setMessage(data.error);
      return;
    }
    const nextBattle = {
      player: data.player,
      opponent: data.opponent,
      playerHp: data.player.stats.HP,
      opponentHp: data.opponent.stats.HP
    };
    setBattle(nextBattle);
    setBattleStatus("in-progress");
    setBattleHighlight(null);
    setBattleTurn("player");
    setBattleLog([
      `${data.opponent.name} challenged you from the wilds!`,
      "Choose a move to begin."
    ]);
  };

  const caughtLookup = new Set(player.dex);
  const messageClass = captureFeedback
    ? `message ${captureFeedback.success ? "success" : "failure"}`
    : "message";

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

      {message && <div className={messageClass}>{message}</div>}
      {timeAdvanceNotice && (
        <div className="modal time-shift">
          <div className="modal-card">
            <h2>Time Advances</h2>
            <p>Three net throws passed. The habitat shifts with time.</p>
          </div>
        </div>
      )}
      {captureModal && (
        <div className="modal capture-result">
          <div className="modal-card">
            <h2>{captureModal.success ? "Capture Success!" : "Capture Missed"}</h2>
            <p>
              {captureModal.success
                ? `${captureModal.name} was secured and sent to your ${captureModal.location}.`
                : `${captureModal.name} dodged the net and slipped away.`}
            </p>
            <button className="primary" onClick={() => setCaptureModal(null)}>
              Continue
            </button>
          </div>
        </div>
      )}

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
                <div className="bird-icon">{getBirdIcon(bird.id)}</div>
                <div>
                  <div className="bird-name">{bird.name}</div>
                  <StatPill label="Type" value={bird.category} />
                  <StatPill
                    label="Level"
                    value={player.levels?.[bird.id] ?? 1}
                  />
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
                <div key={bird.id} className="box-item">
                  <span>
                    {getBirdIcon(bird.id)} {bird.name}
                  </span>
                  <button
                    className="release-button"
                    onClick={() => handleRelease(bird.id)}
                  >
                    Release
                  </button>
                </div>
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
                  className={`bird-sprite ${
                    captureFeedback?.id === bird.id
                      ? captureFeedback.success
                        ? "captured"
                        : "escaped"
                      : ""
                  }`}
                  style={{
                    top: `${15 + index * 10}%`,
                    left: `${10 + (index * 18) % 70}%`
                  }}
                >
                  <div className="bird-sprite-icon">
                    {getBirdIcon(bird.id)}
                  </div>
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

      <section className="battle">
        <div className="battle-header">
          <div>
            <h2>Battle Arena</h2>
            <p className="muted">
              Send out a team bird to spar against a wild challenger.
            </p>
          </div>
          <div className="battle-controls">
            <select
              value={selectedBattleBird}
              onChange={(event) => setSelectedBattleBird(event.target.value)}
            >
              <option value="">Select team bird</option>
              {teamBirds.map((bird) => (
                <option key={bird.id} value={bird.id}>
                  {bird.name}
                </option>
              ))}
            </select>
            <button className="primary" onClick={handleStartBattle}>
              Start Battle
            </button>
          </div>
        </div>
        <div className="battle-stage">
          {battle ? (
            <div className="battle-board">
              <div
                className={`battle-card ${
                  battleHighlight === "player" ? "active" : ""
                } ${battle.playerHp === 0 ? "defeated" : ""}`}
              >
                <div className="battle-icon">
                  {getBirdIcon(battle.player.id)}
                </div>
                <div>
                  <div className="battle-name">{battle.player.name}</div>
                  <div className="battle-meta">
                    Level {player.levels?.[battle.player.id] ?? 1}
                  </div>
                </div>
                <div className="hp-bar">
                  <span
                    style={{
                      width: `${(battle.playerHp / battle.player.stats.HP) * 100}%`
                    }}
                  />
                </div>
                <div className="hp-text">
                  {battle.playerHp} / {battle.player.stats.HP}
                </div>
                <div className="battle-moves">
                  {battle.player.moves.map((move) => (
                    <button
                      key={move.name}
                      className="move-chip"
                      disabled={battleTurn !== "player" || battleStatus !== "in-progress"}
                      onClick={() => handlePlayerMove(move)}
                    >
                      {move.name}
                    </button>
                  ))}
                </div>
              </div>
              <div
                className={`battle-card ${
                  battleHighlight === "opponent" ? "active" : ""
                } ${battle.opponentHp === 0 ? "defeated" : ""}`}
              >
                <div className="battle-icon">
                  {getBirdIcon(battle.opponent.id)}
                </div>
                <div>
                  <div className="battle-name">{battle.opponent.name}</div>
                  <div className="battle-meta">CPU Challenger</div>
                </div>
                <div className="hp-bar">
                  <span
                    style={{
                      width: `${
                        (battle.opponentHp / battle.opponent.stats.HP) * 100
                      }%`
                    }}
                  />
                </div>
                <div className="hp-text">
                  {battle.opponentHp} / {battle.opponent.stats.HP}
                </div>
                <div className="battle-moves">
                  {battle.opponent.moves.map((move) => (
                    <span key={move.name} className="move-chip muted">
                      {move.name}
                    </span>
                  ))}
                </div>
              </div>
              <div className={`battle-result ${battleStatus}`}>
                {battleStatus === "won" && "Victory! Your bird leveled up."}
                {battleStatus === "lost" && "Defeat... Heal up and try again."}
                {battleStatus === "in-progress" &&
                  (battleTurn === "player"
                    ? "Your turn! Choose a move."
                    : "CPU is choosing a response...")}
              </div>
              <div className="battle-log">
                {battleLog.slice(0, 5).map((entry, index) => (
                  <div key={`${entry}-${index}`} className="log-entry">
                    {entry}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="empty-expedition">
              Select a team bird and start a battle to begin.
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
                    <span className="dex-icon">{getBirdIcon(bird.id)}</span>
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
                  <div className="dex-stats">
                    {Object.entries(bird.stats).map(([key, value]) => (
                      <StatPill key={key} label={key} value={value} />
                    ))}
                  </div>
                  <div className="dex-moves">
                    {bird.moves.map((move) => (
                      <div key={move.name} className="move-pill">
                        <div className="move-name">{move.name}</div>
                        <div className="move-meta">
                          <span className="move-type">{move.category}</span>
                          <span className="move-power">Power {move.power}</span>
                        </div>
                      </div>
                    ))}
                  </div>
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
