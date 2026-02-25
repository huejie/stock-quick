# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Stock-Quick (智投助手) is a personal stock tracking mini-program that supports both A-shares and HK stocks. It provides quick access to market hotspots and watchlist management.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                Frontend (uni-app)                    │
│              Vue 3 + TypeScript + Pinia              │
│      Supports: H5 / WeChat Mini-Program              │
├─────────────────────────────────────────────────────┤
│                Backend (FastAPI)                     │
│          Python + akshare + yfinance                 │
├─────────────────────────────────────────────────────┤
│              Data Sources (Free)                     │
│     akshare (A-shares) / yfinance (HK stocks)        │
└─────────────────────────────────────────────────────┘
```

### Directory Structure

- `backend/` - FastAPI backend service
  - `app/api/` - API route handlers
  - `app/core/` - Configuration (settings from `.env`)
  - `app/models/` - Data models
  - `app/schemas/` - Pydantic request/response schemas
  - `app/services/` - Business logic (currently uses in-memory storage for MVP)
- `frontend/` - uni-app frontend
  - `src/api/` - HTTP request utilities
  - `src/pages/` - Page components (watchlist, market)
  - `src/store/` - Pinia state management
  - `src/types/` - TypeScript type definitions

## Development Commands

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server (port 8000)
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API documentation available at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run H5 development server (port 7777)
npm run dev:h5

# Run WeChat mini-program development
npm run dev:mp-weixin

# Build for H5
npm run build:h5

# Build for WeChat mini-program
npm run build:mp-weixin
```

### Testing

```bash
# Backend tests (when available)
cd backend
pytest

# With coverage
pytest --cov=app
```

## Key APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/watchlist` | GET | Get user's watchlist |
| `/api/watchlist` | POST | Add stock to watchlist |
| `/api/watchlist` | DELETE | Remove stock from watchlist |
| `/api/watchlist/search` | GET | Search stocks by keyword |
| `/health` | GET | Health check |

## Configuration

### Backend Environment Variables

Create `backend/.env` based on `backend/.env.example`:
- `ENV` - Environment (development/production)
- `DEBUG` - Enable debug mode
- `MONGODB_URL` - MongoDB connection (for future persistence)
- `REDIS_URL` - Redis connection (for future caching)

### Frontend API Base URL

Configure in `frontend/src/api/request.ts`:
- H5: Uses proxy via vite.config.ts
- WeChat Mini-Program: Direct backend URL

## Notes

- **MVP Storage**: Watchlist currently uses in-memory storage. Data is lost on server restart.
- **Stock Data Caching**: A-share and HK stock data is cached for 1 hour to reduce API calls to akshare.
- **Fallback Data**: If akshare fails, the service falls back to a hardcoded list of popular stocks.
- **Color Convention**: Red for gains, green for losses (A-share convention).
