const { contextBridge } = require('electron');

// Expose safe IPC methods to renderer process
contextBridge.exposeInMainWorld('electron', {
  // Placeholder for future IPC methods if needed
  apiVersion: '1.0.0',
});
