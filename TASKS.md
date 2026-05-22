# VS Code Launch Tasks & Debug Configuration

This project includes comprehensive VS Code tasks for development, testing, building, and debugging.

## Quick Start

### Option 1: Run Full Development Environment (Recommended)
```
Press: Ctrl + Shift + B  (default build task)
```
This starts both backend and frontend concurrently.

### Option 2: Run Tasks Individually

**Open Task Menu**: `Ctrl + Shift + P` → Search for "Tasks: Run Task"

---

## Available Tasks

### 🚀 Launch Tasks

#### **Full Dev: Backend + Frontend (Concurrent)** ⭐ DEFAULT
- **What**: Starts Uvicorn backend + Vite frontend together
- **Command**: `npm run dev` (from root)
- **Ports**: Backend on 5000, Frontend on 5173
- **Use when**: Starting fresh development session
- **Keyboard**: `Ctrl + Shift + B`

#### **Backend: Start FastAPI**
- **What**: Starts Python FastAPI server only
- **Command**: `python -m uvicorn app.main:app --host 127.0.0.1 --port 5000`
- **Port**: http://127.0.0.1:5000
- **API Docs**: http://127.0.0.1:5000/docs
- **Use when**: Testing API independently or debugging backend

#### **Frontend: Start Dev Server**
- **What**: Starts Vite dev server only
- **Command**: `npm run dev` (from frontend folder)
- **Port**: http://localhost:5173
- **Use when**: Testing frontend independently or debugging UI

#### **Electron: Launch App**
- **What**: Launches the Electron desktop app
- **Dependencies**: Requires frontend dev server running first
- **Use when**: Testing full desktop application

---

### 🔗 Utilities

#### **API: Open Swagger Docs**
- **What**: Opens Swagger API documentation in browser
- **URL**: http://127.0.0.1:5000/docs
- **Requires**: Backend running
- **Interactive**: Allows testing all API endpoints directly

#### **Frontend: Open Dev Server**
- **What**: Opens Vite dev server in browser
- **URL**: http://localhost:5173
- **Requires**: Frontend running

#### **MongoDB: Check Connection**
- **What**: Verifies MongoDB connection
- **Command**: Tests connection to localhost:27017

---

### 📦 Build Tasks

#### **Build: Frontend (Production)**
- **What**: Builds optimized frontend for production
- **Output**: `frontend/dist/`
- **Command**: `npm run build`
- **Use when**: Preparing for release/deployment

#### **Build: Electron Executable**
- **What**: Packages Electron app as .exe for Windows
- **Output**: `dist/Finance Tracker.exe`
- **Command**: `npm run build:electron`
- **Requirements**: Frontend must be built first
- **Use when**: Creating Windows installer

---

### 📥 Installation Tasks

#### **Backend: Install Dependencies**
- **What**: Installs Python packages from requirements.txt
- **Command**: `pip install -r requirements.txt`
- **Use when**: Adding new Python dependencies or fresh setup

#### **Frontend: Install Dependencies**
- **What**: Installs npm packages from package.json
- **Command**: `npm install`
- **Use when**: Adding new npm packages or fresh setup

---

### 🧪 Testing & Quality

#### **Linter: Check Python (Backend)**
- **What**: Runs pylint on backend code
- **Command**: `pylint app/`
- **Checks**: Code style, unused imports, potential errors

---

## Debug Configurations (F5 or Debug Panel)

### Available Configurations

1. **Backend: Python FastAPI** 🐍
   - Debug FastAPI application
   - Supports breakpoints
   - Auto-reload on file changes
   - Console output in integrated terminal

2. **Frontend: React Dev Server** 🌐
   - Debug React code in browser
   - Chrome DevTools integration
   - Source maps for TypeScript

3. **Electron: Main Process** ⚛️
   - Debug Electron main process
   - Node debugger
   - Breakpoints in IPC code

4. **Full Stack (Debug)** 🔗
   - Compound configuration
   - Starts both Backend and Frontend debuggers
   - Recommended for integrated debugging

5. **Backend: Python Tests** 🧪
   - Run pytest test suite
   - Verbose output
   - Breakpoints in tests

---

## How to Use Tasks

### Method 1: Keyboard Shortcut
```
Ctrl + Shift + P                    → Open Command Palette
Type: "Tasks: Run Task"             → See available tasks
Select desired task                 → Press Enter
```

### Method 2: Keyboard Shortcut (Default)
```
Ctrl + Shift + B    →   Runs default task (Full Dev)
```

### Method 3: Terminal Integration
```
View → Terminal                     → Open integrated terminal
Ctrl + `                            → Toggle terminal
```

### Method 4: VS Code UI
```
Terminal → Run Task                 → Click desired task
```

---

## Typical Development Workflow

### 1. Start Development Session
```
Press: Ctrl + Shift + B
```
✓ Backend starts on port 5000
✓ Frontend starts on port 5173

### 2. View API Documentation
```
Tasks → Run Task → "API: Open Swagger Docs"
```
✓ Swagger UI opens in browser
✓ Test endpoints interactively

### 3. Start Debugging
```
Press: F5 or View → Run and Debug
Select: "Backend: Python FastAPI" or "Frontend: React Dev Server"
```
✓ Debugger attaches
✓ Breakpoints enabled

### 4. Build for Production
```
Tasks → Run Task → "Build: Frontend (Production)"
Tasks → Run Task → "Build: Electron Executable"
```
✓ Creates dist/ folder with production build
✓ Creates .exe installer

---

## Common Issues & Solutions

### Backend won't start
```
✓ Check MongoDB running: mongod --dbpath <path>
✓ Check port 5000 not in use: netstat -ano | findstr :5000
✓ Run: "Backend: Install Dependencies" task
```

### Frontend won't start
```
✓ Check port 5173 not in use
✓ Run: "Frontend: Install Dependencies" task
✓ Delete frontend/node_modules and run npm install
```

### Tasks not showing up
```
✓ Reload VS Code: Ctrl + Shift + P → "Developer: Reload Window"
✓ Check .vscode/tasks.json syntax
✓ Verify all file paths are correct
```

### Debugging not working
```
✓ Ensure correct debugger installed (Python, Chrome)
✓ Check breakpoint is on valid line
✓ Check process is actually running
✓ View Debug Console for errors
```

---

## Environment Variables

Backend uses `.env` file at `backend/.env`:
```
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=financial_data
COLLECTION_NAME=transactions
API_HOST=127.0.0.1
API_PORT=5000
LAZY_CONNECT=true
```

To change ports or database, edit this file and restart tasks.

---

## Recommended VS Code Extensions

Install these for better development experience:

- **Python** (ms-python.python) - Python support, debugging
- **Pylance** (ms-python.vscode-pylance) - Python type checking
- **Prettier** (esbenp.prettier-vscode) - Code formatting
- **ESLint** (dbaeumer.vscode-eslint) - JavaScript/TypeScript linting
- **MongoDB** (mongodb.mongodb-vscode) - MongoDB connection explorer
- **GitLens** (eamodio.gitlens) - Git integration

Auto-install by clicking "Install" in Extensions → Recommended

---

## Tips & Tricks

1. **Split Terminal for Multiple Tasks**
   - Start one task, then `Ctrl + Shift + P` → "Terminal: Create New Terminal"
   - Run another task in the new terminal

2. **Stop Running Tasks**
   - `Ctrl + Shift + P` → "Tasks: Terminate Task"
   - Or close the terminal

3. **View Task Output**
   - Output panel appears automatically when task runs
   - `Ctrl + Shift + U` to toggle Output panel

4. **Rerun Last Task**
   - `Ctrl + Shift + P` → "Tasks: Rerun Last Task"

5. **Debug with Print Statements**
   - Backend: Add `print()` statements, output in integrated terminal
   - Frontend: Use `console.log()`, view in browser DevTools (F12)

---

## Performance Tips

- Keep backend running in one terminal for development
- Frontend dev server has hot module reloading (HMR) - very fast
- Use Chrome DevTools (F12) for frontend debugging
- Python debugger (F5) for backend breakpoints

---

**For more details**, see [README.md](../README.md) and [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md)
