const { app, BrowserWindow, Menu } = require('electron');
const isDev = require('electron-is-dev');
const path = require('path');
const http = require('http');
const spawn = require('child_process').spawn;

let mainWindow;
let pythonProcess;

const BACKEND_PORT = 5000;

// Start Python backend
function startPythonBackend() {
  console.log('Starting Python backend...');

  if (isDev) {
    const backendDir = path.join(__dirname, '../backend');
    pythonProcess = spawn(path.join(backendDir, 'venv/Scripts/python.exe'), [
      '-m',
      'uvicorn',
      'app.main:app',
      '--host',
      '127.0.0.1',
      '--port',
      String(BACKEND_PORT),
      '--reload'
    ], {
      stdio: 'inherit',
      cwd: backendDir,
      env: {
        ...process.env,
        PYTHONPATH: backendDir,
      },
    });
  } else {
    // Packaged app: backend is a PyInstaller bundle under resources/backend
    const backendExe = path.join(process.resourcesPath, 'backend', 'finance-tracker-backend.exe');
    pythonProcess = spawn(backendExe, [], {
      stdio: 'ignore',
      cwd: path.dirname(backendExe),
      windowsHide: true,
      env: {
        ...process.env,
        API_PORT: String(BACKEND_PORT),
      },
    });
  }

  pythonProcess.on('error', (err) => {
    console.error('Failed to start Python backend:', err);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });

  return waitForBackend();
}

// Poll the health endpoint until the backend is accepting requests.
// The packaged backend can take several seconds to start (pandas/sklearn imports).
function waitForBackend(timeoutMs = 30000) {
  const deadline = Date.now() + timeoutMs;
  return new Promise((resolve, reject) => {
    const attempt = () => {
      const req = http.get(`http://127.0.0.1:${BACKEND_PORT}/health`, (res) => {
        res.resume();
        if (res.statusCode === 200) {
          resolve();
        } else {
          retry();
        }
      });
      req.setTimeout(1000, () => req.destroy(new Error('timeout')));
      req.on('error', retry);
    };
    const retry = () => {
      if (Date.now() > deadline) {
        reject(new Error(`Backend did not respond on port ${BACKEND_PORT} within ${timeoutMs}ms`));
        return;
      }
      setTimeout(attempt, 500);
    };
    attempt();
  });
}

// Create Electron window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  const startUrl = isDev
    ? 'http://localhost:5173'  // Vite dev server
    : `file://${path.join(__dirname, '../frontend/dist/index.html')}`;

  if (isDev) {
    mainWindow.webContents.session.clearCache();
  }

  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// App lifecycle
app.on('ready', async () => {
  try {
    await startPythonBackend();
    createWindow();
  } catch (err) {
    console.error('App startup failed:', err);
    app.quit();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (pythonProcess) {
    console.log('Terminating Python backend...');
    pythonProcess.kill('SIGTERM');
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// Menu
const template = [
  {
    label: 'File',
    submenu: [
      { role: 'quit' },
    ],
  },
  {
    label: 'View',
    submenu: [
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },
    ],
  },
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);
