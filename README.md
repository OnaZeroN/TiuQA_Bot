# Tiu QA Bot
[![Author](https://img.shields.io/badge/Author-@OnaZeroN-blue)](https://github.com/OnaZeroN)

## ⚙️ System dependencies
- Python 3.13+
- Docker
- docker-compose
- make
- uv

## 🐳 Quick Start with Docker compose
- Rename `.env.dist` to `.env` and configure it
- Rename `docker-compose.example.yml` to `docker-compose.yml`
- Run `make app-build` command then `make app-run` to start the bot

Use `make` to see all available commands

## 🔧 Development

### Setup environment
```bash
uv sync
```
