
const { app, BrowserWindow, dialog, ipcMain} = require('electron');
const path = require('node:path');
//! const { spawn } = require('child_process');
//! const { execFile } = require('child_process');
const axios = require('axios');
const fs = require('fs');
const http = require('http');
const electronDl = require('electron-dl');
const {download} = require('electron-dl');

let isQuitting = false;
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'js/preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  mainWindow.loadFile('html/index.html');
}

// async function startFastApiService() {
//   //! Build path
//   const executablePath = path.join(__dirname, '..','dist','main','main.exe');

//   //! Dev path
//   // const executablePath = path.join(__dirname,'..','logic', 'dist' ,'main.exe');

//   console.log(executablePath)
//   execFile(executablePath, (error, stdout, stderr) => {
//     if (error) {
//       throw error;
//     }
//   });
// }

async function stopFastApiService() {
  try {
    const clearResponse = await axios.post(`http://${process.env.HOST}/clear`);
    if (clearResponse.status === 200) {
      console.log('Storage cleared');
    }
  } catch (error) {
    console.error(error);
  }
} 

app.whenReady().then(() => {

  // ******
  process.env['HOST'] = 'localhost:8000';
  electronDl();
  // ******

  //! startFastApiService();
  createWindow();
  //!console.log(process.env.HOST)

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('before-quit', async (event) => {
  if (!isQuitting) { 
    event.preventDefault();
    isQuitting = true; 
    await stopFastApiService();
    console.log('FastAPI service stopped and cleaned');

    app.quit(); 
  }
});
ipcMain.on('download-url', async (event, url) => {
  const win = BrowserWindow.getFocusedWindow();
    try {
        console.log(await download(win, url));
    } catch (error) {
        if (error instanceof electronDl.CancelError) {
          console.info('item.cancel() was called');
    } else {
      console.error(error);
    }
  }
});