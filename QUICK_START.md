# Quick Reference - Launch Commands

## Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Shift + B` | **Start Full Dev** (Backend + Frontend) |
| `Ctrl + Shift + P` | Open Command Palette (search tasks) |
| `F5` | Start Debugging |
| `Ctrl + `` | Toggle Integrated Terminal |
| `Ctrl + Shift + U` | Toggle Output Panel |
| `Ctrl + Shift + D` | Open Debug Panel |

---

## Instant Launch

### 🚀 Full Development (Recommended)
```
Ctrl + Shift + B
```
- Starts FastAPI backend (port 5000)
- Starts Vite frontend (port 5173)
- Both run concurrently
- Wait ~5 seconds for both to be ready

### 🐍 Backend Only
```
Ctrl + Shift + P → Tasks: Run Task → "Backend: Start FastAPI"
```
- FastAPI on http://127.0.0.1:5000
- API Docs at http://127.0.0.1:5000/docs

### 🌐 Frontend Only
```
Ctrl + Shift + P → Tasks: Run Task → "Frontend: Start Dev Server"
```
- Vite on http://localhost:5173

### 🔍 View API Docs (Interactive)
```
Ctrl + Shift + P → Tasks: Run Task → "API: Open Swagger Docs"
```
- Opens Swagger UI
- Test all endpoints directly

---

## Development Workflow

### Session 1: Quick Testing
```
1. Ctrl + Shift + B                    (start dev environment)
2. Wait 5 seconds for both to start
3. Browser opens frontend at localhost:5173
4. Open http://127.0.0.1:5000/docs in another tab to test API
5. Edit files → Hot reload happens automatically
6. Done!
```

### Session 2: Debug Backend
```
1. Ctrl + Shift + B                    (start dev environment in one terminal)
2. Open another terminal: Ctrl + Shift + `` 
3. F5 → Select "Backend: Python FastAPI"
4. Set breakpoints by clicking left margin
5. Trigger breakpoint by using frontend or API docs
6. Debug in VS Code!
```

### Session 3: Debug Frontend
```
1. Ctrl + Shift + B                    (start dev environment)
2. F12                                 (open browser DevTools)
3. Edit code, hot reload happens
4. Use Chrome DevTools to inspect React components
5. Done!
```

---

## URLs (Bookmarks These!)

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:5000/docs | API Swagger Docs (test endpoints) |
| http://127.0.0.1:5000/api/health | API Health Check |
| http://localhost:5173 | Frontend Dev Server |
| http://localhost:5173/__vite_ping | Vite Check |

---

## Terminal Commands (Direct Execution)

### Manual Backend Start
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 5000
```

### Manual Frontend Start
```powershell
cd frontend
npm run dev
```

### Manual Full Dev Start
```powershell
npm run dev
```

### Build for Production
```powershell
npm run build
npm run build:electron
```

---

## Environment Check

### Is Backend Running?
```
curl http://127.0.0.1:5000/health
```
Should return: `{"status":"ok"}`

### Is MongoDB Connected?
```
curl http://127.0.0.1:5000/api/health
```
Should return: `{"mongodb":"ok","api":"ok"}`

### Is Frontend Running?
```
curl http://localhost:5173
```
Should return HTML page

---

## Common Tasks via Command Palette

```
Ctrl + Shift + P, then type:

Tasks: Run Task
  → Full Dev: Backend + Frontend (Concurrent)
  → Backend: Start FastAPI
  → Frontend: Start Dev Server
  → Backend: Install Dependencies
  → API: Open Swagger Docs

Debug: Start Debugging
  → Backend: Python FastAPI
  → Full Stack (Debug)

Debug: Terminate Task
  → (stops running tasks)

Developer: Reload Window
  → (refresh VS Code if things break)
```

---

## Stop Everything

```
Ctrl + Shift + P → Tasks: Terminate Task → Select task
```
Or close the terminal tabs.

---

## File Locations

| File | Purpose |
|------|---------|
| `.vscode/tasks.json` | Task definitions |
| `.vscode/launch.json` | Debug configurations |
| `.vscode/settings.json` | Workspace settings |
| `backend/.env` | Backend configuration |
| `frontend/vite.config.ts` | Frontend build config |
| `electron/main.js` | Electron entry point |

---

## Extensions to Install

```
Ctrl + Shift + X → Click "Install" on Recommended tab
```

Recommended:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Prettier (esbenp.prettier-vscode)
- ESLint (dbaeumer.vscode-eslint)
- MongoDB (mongodb.mongodb-vscode)
- GitLens (eamodio.gitlens)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Tasks not showing | `Ctrl+Shift+P` → "Developer: Reload Window" |
| Port 5000 in use | `netstat -ano \| findstr :5000` → `taskkill /PID <PID>` |
| Port 5173 in use | `netstat -ano \| findstr :5173` → `taskkill /PID <PID>` |
| Backend won't connect | Check MongoDB running: `mongod` |
| Frontend blank page | Check browser console (F12) for errors |
| Debugger not working | Restart VS Code, ensure extensions installed |

---

**For detailed information, see [TASKS.md](TASKS.md)**
