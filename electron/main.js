const { app, BrowserWindow, Menu } = require('electron');
const isDev = require('electron-is-dev');
const path = require('path');
const spawn = require('child_process').spawn;

let mainWindow;
let pythonProcess;

// Python backend configuration
const PYTHON_EXECUTABLE = isDev 
  ? path.join(__dirname, '../backend/venv/Scripts/python.exe')
  : path.join(process.resourcesPath, 'backend/venv/Scripts/python.exe');

const PYTHON_MAIN = isDev
  ? path.join(__dirname, '../backend/app/main.py')
  : path.join(process.resourcesPath, 'backend/app/main.py');

// Start Python backend
function startPythonBackend() {
  console.log('Starting Python backend...');
  console.log('Python:', PYTHON_EXECUTABLE);
  console.log('Main:', PYTHON_MAIN);

  const backendDir = path.join(__dirname, '../backend');
  
  pythonProcess = spawn(PYTHON_EXECUTABLE, [
    '-m',
    'uvicorn',
    'app.main:app',
    '--host',
    '127.0.0.1',
    '--port',
    '5000',
    '--reload'
  ], {
    stdio: 'inherit',
    cwd: backendDir,
    env: {
      ...process.env,
      PYTHONPATH: backendDir,
    },
  });

  pythonProcess.on('error', (err) => {
    console.error('Failed to start Python backend:', err);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });

  // Give backend time to start
  return new Promise((resolve) => {
    setTimeout(() => resolve(), 2000);
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
