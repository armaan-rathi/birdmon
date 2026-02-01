# Birdmon

A prototype Flask + React webapp for a bird-watching adventure RPG. The current build focuses on the exploration loop: choose a habitat, see the weather, spot birds, and add them to your team.

## Tech Stack
- Flask API running on port **5001**
- React + Vite front-end

## Gameplay controls
- **Advance Time** rolls the next time slot and refreshes weather.
- **Reset Fieldwork** clears your team/box and returns to the initial time slot.

## Running locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open the app at `http://localhost:5173`.
