# Django Leaderboard API

## Overview
The **Django Leaderboard API** is a RESTful service that allows users to manage games, contestants, scores, leaderboards, and game popularity metrics. The system enables tracking of games and contestants while providing real-time leaderboards and a game popularity score.

## Live API URL
**Base URL:** [https://django-leaderboard.onrender.com/api/](https://django-leaderboard.onrender.com/api/)

## Features
- Create, update, and delete games
- Create, update, and delete contestants
- Start and end games with contestants joining and exiting
- Assign scores to contestants in active games
- Retrieve global and game-specific leaderboards
- Compute and display game popularity score (refreshes every 5 minutes)

## Assumptions
- Each game and contestant has a unique identifier.
- Scores are assigned only when a contestant is inside an active game.
- Leaderboard and popularity scores are recalculated periodically.
- Scores reset every day (no carry-forward mechanism).
- Games must be explicitly started before contestants can join.
- A background task updates game popularity scores every 5 minutes.

---

## Setup Guide
### Running Locally
1. **Clone the repository:**
   ```sh
   git clone https://github.com/RohanGeorge23/Django-Leaderboard.git
   cd Django-Leaderboard
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Run the server:**
   ```sh
   python manage.py runserver
   ```

### Environment Variables
Create a `.env` file and set the following:
```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # Or PostgreSQL if using a production database
ALLOWED_HOSTS=localhost,127.0.0.1,django-leaderboard.onrender.com
```

---

## API Endpoints
### **Games API**
#### **1. Create a Game**
`POST /games/`
```json
{
  "name": "Chess",
  "description": "A strategy board game",
  "max_players": 2
}
```

#### **2. Retrieve All Games**
`GET /games/`

#### **3. Retrieve a Specific Game**
`GET /games/{game_id}/`

#### **4. Update a Game**
`PUT /games/{game_id}/`
```json
{
  "name": "Updated Chess",
  "max_players": 4
}
```

#### **5. Delete a Game**
`DELETE /games/{game_id}/`

---

### **Contestants API**
#### **1. Create a Contestant**
`POST /contestants/`
```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

#### **2. Retrieve All Contestants**
`GET /contestants/`

#### **3. Retrieve a Specific Contestant**
`GET /contestants/{contestant_id}/`

#### **4. Update a Contestant**
`PUT /contestants/{contestant_id}/`
```json
{
  "name": "Alice Johnson"
}
```

#### **5. Delete a Contestant**
`DELETE /contestants/{contestant_id}/`

---

### **Game Management API**
#### **1. Start a Game**
`POST /games/{game_id}/start/`

#### **2. End a Game**
`POST /games/{game_id}/end/`

#### **3. Add a Contestant to a Game**
`POST /games/{game_id}/join/`
```json
{
  "contestant_id": 1
}
```

#### **4. Remove a Contestant from a Game**
`POST /games/{game_id}/exit/`
```json
{
  "contestant_id": 1
}
```

---

### **Scoring API**
#### **1. Assign Score to a Contestant**
`POST /games/{game_id}/score/`
```json
{
  "contestant_id": 1,
  "score": 100
}
```

---

### **Leaderboard API**
#### **1. Retrieve Global Leaderboard**
`GET /leaderboard/global/`

#### **2. Retrieve Game-specific Leaderboard**
`GET /leaderboard/game/{game_id}/`

#### **3. Retrieve Daily Leaderboard**
`GET /leaderboard/daily/`

---

### **Game Popularity API**
#### **1. Retrieve Game Popularity Score**
`GET /games/popularity/`

**Formula:**
```python
Score = (0.3 * (w1/max_daily_players) +
         0.2 * (w2/max_concurrent_players) +
         0.25 * (w3/max_upvotes) +
         0.15 * (w4/max_session_length) +
         0.1 * (w5/max_daily_sessions))
```

- **w1:** Players who played the game yesterday
- **w2:** Players currently in the game
- **w3:** Total upvotes
- **w4:** Maximum session length yesterday
- **w5:** Total sessions yesterday
- **Refreshes every 5 minutes**

---

## Test Scenario
1. **Create 5+ games** using `POST /games/`
2. **Add multiple contestants** using `POST /contestants/`
3. **Join contestants to different games** at various timestamps (`POST /games/{game_id}/join/`)
4. **Assign scores to contestants** (`POST /games/{game_id}/score/`)
5. **Get leaderboards** at game and global levels (`GET /leaderboard/global/`)
6. **Check popularity score** (`GET /games/popularity/`)
7. **Wait 6 minutes and check again** to confirm the score changes

---

## Deployment on Render
1. **Push your code to GitHub**
2. **Link the repository to Render**
3. **Set the build command:** `pip install -r requirements.txt`
4. **Set the start command:** `gunicorn leaderboard.wsgi`
5. **Set environment variables** (like `ALLOWED_HOSTS`)
6. **Deploy and verify API using Postman or curl**

---

## Contact
For any questions or issues, contact [Rohan George](https://github.com/RohanGeorge23).

