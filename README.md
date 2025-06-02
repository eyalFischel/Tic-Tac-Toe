# 🕹️ Real-Time Multiplayer Tic-Tac-Toe Game

This project is a real-time multiplayer **Tic-Tac-Toe (X and O)** game that allows two players to compete from separate browsers. When one player makes a move, it is instantly reflected on the other player's interface.

---

## ✨ Features

- 🔁 Real-time multiplayer gameplay
- 🎮 Classic 3x3 Tic-Tac-Toe logic
- 🐍 Backend: FastAPI (Python) with WebSocket support
- 🌐 Cross-browser play — no login required

---

## 🧱 Tech Stack

### Backend
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- Python 3.8+

---

## 🚀 Getting Started

### 🔧 Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

### 🐳 Run with Docker Compose

```bash
docker-compose up
```

### NOTES
If I had more time, I would have:
* Added the UI
* Written automated tests
* Looked for additional bugs and potential issues
* Analyzed potential time and memory complexity problems
* Would have added users stats APIs

#### Feel free to play with it locally (port 8000) or use the API from (private server, proxmox vm) https://www.tictractoe.com/help , You can also use : https://www.tictractoe.com/docs for more information.