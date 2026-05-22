# Finance Tracker - Desktop App

A lightweight desktop finance tracker built with Electron + React + Python/FastAPI, connected to MongoDB.

## Overview

- **Desktop App**: Electron (Windows)
- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: Python FastAPI + Uvicorn
- **Database**: MongoDB (local instance)
- **Features**: Transactions list/table, pay period filtering, category breakdown, spending trends, recurring detection

## Project Structure

```
finance-tracker/
├── frontend/              # React + TypeScript UI
│   ├── src/
│   │   ├── api/          # API clients & endpoints
│   │   ├── components/   # Reusable React components
│   │   ├── pages/        # Page-level components
│   │   ├── types/        # TypeScript types
│   │   ├── hooks/        # Custom React hooks
│   │   └── App.tsx       # Main app component
│   ├── index.html
│   └── vite.config.ts
├── backend/              # Python FastAPI server
│   ├── app/
│   │   ├── main.py       # FastAPI entry point
│   │   ├── models/       # Pydantic models
│   │   ├── services/     # Business logic
│   │   ├── repository/   # MongoDB access layer
│   │   ├── util/         # Pay period detection, utilities
│   │   └── ml/           # ML features (future)
│   ├── venv/             # Python virtual environment
│   ├── .env              # Configuration (localhost MongoDB)
│   └── requirements.txt
├── electron/             # Electron main process
│   ├── main.js           # App entry, subprocess management
│   └── preload.js        # IPC bridge
└── package.json          # Root npm scripts

```

## Prerequisites

- **Node.js** 16+ (for frontend & Electron)
- **Python** 3.10+ (for backend)
- **MongoDB** 4.4+ (local instance at `mongodb://localhost:27017`)

## Quick Start

### 1. Verify MongoDB is Running

```bash
# Check if MongoDB is running on localhost:27017
# You should have MongoDB installed locally
```

### 2. Install Backend Dependencies

```bash
cd backend
.\venv\Scripts\Activate.ps1  # On Windows
# or: source venv/bin/activate  # On Mac/Linux

# Dependencies should already be installed, but to reinstall:
# pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install  # Should already be done
```

### 4. Run Development Mode

From the root directory:

```bash
# Option A: Run everything together (frontend + Electron)
npm run dev

# Option B: Run individually
# Terminal 1: Start backend
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 5000

# Terminal 2: Start frontend dev server
cd frontend
npm run dev

# Terminal 3: Start Electron
npm run dev:electron
```

## API Documentation

Once the backend is running, visit: **http://127.0.0.1:5000/docs**

This shows the interactive Swagger documentation for all endpoints.

## Key Endpoints

### Transactions
- `GET /api/transactions` - Get all transactions
- `GET /api/transactions/{id}` - Get by ID
- `GET /api/transactions/search?query=...` - Search
- `GET /api/transactions/by-date?start=...&end=...` - Date range
- `GET /api/transactions/by-pay-period?month=...` - Pay period (e.g., "September2024")
- `POST /api/transactions` - Create
- `PUT /api/transactions/{id}` - Update
- `DELETE /api/transactions/{id}` - Delete
- `GET /api/pay-periods?months=12` - List available months
- `GET /api/recurring` - Get recurring transactions
- `GET /api/categories` - List categories

### Statistics
- `GET /api/stats/summary?start=...&end=...` - Summary (total, net, avg)
- `GET /api/stats/category-breakdown?start=...&end=...` - Spending by category
- `GET /api/stats/spending-trend?start=...&end=...&granularity=daily` - Trends

### Health
- `GET /health` - Basic health check
- `GET /api/health` - API + MongoDB check

## Development Notes

### Pay Period Detection

The system detects pay periods by looking for a marker transaction description:
- **Marker**: `"TIMECLOCK PLUS L DES:"`
- This identifies paycheck deposits and sets period boundaries
- Ported from your existing .NET implementation

### MongoDB Configuration

The backend connects to:
- **URI**: `mongodb://localhost:27017` (from `.env`)
- **Database**: `financial_data`
- **Collection**: `transactions`

If MongoDB is not running, the API will start but database operations will fail gracefully.

### Frontend State Management

- **React Hooks** for state
- **Context API** for global state (if needed)
- **Axios** for API calls
- **Recharts** for visualization

### Electron Integration

The Electron main process (`electron/main.js`):
1. Spawns the Python backend as a subprocess
2. Waits for the server to start (~2 seconds)
3. Opens the React dev server (or built app)
4. Manages window lifecycle

## Next Steps

### Phase 5: ML Features
- [ ] Transaction categorization (scikit-learn)
- [ ] Recurring transaction detection
- [ ] CSV import with auto-categorization

### Phase 6: Polish & Packaging
- [ ] Error handling improvements
- [ ] Database indexing
- [ ] Unit & integration tests
- [ ] Windows `.exe` installer (electron-builder)

## Troubleshooting

**Backend won't connect to MongoDB**
- Ensure MongoDB is running: `mongod` or check your MongoDB installation
- Verify connection string in `backend/.env`

**Frontend can't reach backend**
- Ensure backend is running on `http://127.0.0.1:5000`
- Check CORS is enabled (it is, for all origins)
- Look at browser console for fetch errors

**Electron window is blank**
- Check that frontend dev server is running on `http://localhost:5173`
- Look at Electron dev tools (`Ctrl+Shift+I`)

**Port 5000 already in use**
- Change `API_PORT` in `backend/.env` and update frontend `api/client.ts`
- Or kill the existing process: `lsof -i :5000` (Mac/Linux) or `netstat -ano | findstr :5000` (Windows)

## File Changes Summary

### Created Files
- `frontend/src/`: All React components, hooks, types, API clients
- `backend/app/`: All Python services, repositories, models, utilities
- `electron/main.js`, `preload.js`: Electron entry points
- `package.json`: Updated with Electron & scripts
- `.env`: Configuration files
- `README.md`: This file

### Key Logic Ported from .NET App
- **PayPeriodCalculator.cs** → `backend/app/util/pay_period.py`
  - Marker-based pay period detection
  - 3-month search window optimization
  - Available pay periods listing
- **Transaction.cs** → `backend/app/models/transaction.py`
- **TransactionsViewModel.cs** → React hooks + TransactionsPage.tsx
- **Repository pattern** → `TransactionRepository` with MongoDB adapter

## Database Schema (MongoDB)

### Transaction Document
```json
{
  "_id": ObjectId("..."),
  "amount": -50.25,
  "balance": 1234.56,
  "category": "Groceries",
  "date": ISODate("2024-09-15"),
  "description": "WALMART #123",
  "is_deposit": false,
  "is_recurring": false,
  "transaction_id": "TXN_12345",
  "type": "Debit"
}
```

Indices to create (for performance):
```javascript
db.transactions.createIndex({ "date": -1 })
db.transactions.createIndex({ "category": 1 })
db.transactions.createIndex({ "description": "text" })
```

## License

ISC

---

**Status**: Phases 1-4 complete. Backend running & verified. Frontend components built. Ready for Phase 5 (ML features) and Phase 6 (packaging).
