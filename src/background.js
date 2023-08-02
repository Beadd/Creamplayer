'use strict'
import path from 'path'

import { exec } from 'child_process';
import { app, protocol, BrowserWindow, screen, ipcMain, session } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

let win
let childWin;
let downloadCount = 0;
let errorWins = [];
function createChildWindow() {
  const htmlText = `
    <html>
      <head>
        <style>
          html {
            background-color: lightgreen;
            user-select: none;
          }
          h1 {
            font-size: 22vw;
            font-family: 'SuperBlack', Arial, sans-serif;
            text-align: center;
            position: relative;
            top: 50%;
            transform: translateY(-50%);    
          }
        </style>
      </head>
      <body>
        <h1>load</h1>
      </body>
    </html>`
  childWin = new BrowserWindow({ 
    width: 333,
    height: 222,
    autoHideMenuBar: true,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: true,
    }
  })
  const htmlDataUri = 'data:text/html,' + encodeURIComponent(htmlText);
  childWin.loadURL(htmlDataUri)
  childWin.on('closed', () => {
    childWin = undefined;
    errorWins.forEach(win => win.close());
    errorWins = [];
    downloadCount = 0;
  });
}

function createErrorWindow(message) {
  const errorHtmlText = `
    <html>
      <head>
        <style>
          html {
            background-color: red;
          }
          h1 {
            font-size: 12vw;
            font-family: 'SuperBlack', Arial, sans-serif;
            text-align: center;
            position: relative;
            top: 50%;
            transform: translateY(-50%);    
          }
        </style>
      </head>
      <body>
        <h1>` + String(message) + `</h1>
      </body>
    </html>`
  const errorWin = new BrowserWindow({ 
    width: 333,
    height: 222,
    autoHideMenuBar: true,
    parent: win,
    webPreferences: {
      nodeIntegration: true,
    }
  })
  const errorHtmlDataUri = 'data:text/html,' + encodeURIComponent(errorHtmlText);
  errorWin.loadURL(errorHtmlDataUri)
  errorWins.push(errorWin);
}

ipcMain.on('download', (event, args) => {
  if (!childWin) {
    createChildWindow()
  }
  downloadCount++;
  childWin.webContents.executeJavaScript(`
    document.querySelector('h1').innerText = '${downloadCount}';
  `);
  const binPath = path.join(__dirname, '../');
  console.log(args);
  exec(path.join(binPath) + args, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error running example.exe: ${error.message}`);
      childWin.webContents.executeJavaScript(`
        document.querySelector('h1').style.color = 'red';      
      `);
      const songid = args.match(/-i "(\d+)"/)[1];
      createErrorWindow(songid)
      return;
    }
    console.log('example.exe output:', stdout);
    if (stdout.includes('success')) {
      console.log('download completed successfully')
      downloadCount--;
    } else if (stdout.includes('vip')) {
      console.log('download is VIP')
      childWin.webContents.executeJavaScript(`
        document.querySelector('h1').style.color = 'red';      
      `);
    }
    if (downloadCount === 0) {
      // All downloads completed
      childWin.webContents.executeJavaScript(`
        document.querySelector('h1').innerText = 'success';  
      `);
    } else {
      // Update counter
      childWin.webContents.executeJavaScript(`
        document.querySelector('h1').innerText = '${downloadCount}';
      `);
    }
  });
})
ipcMain.on('set-cookie', (event, cookies) => {
  if (cookies) {
    const appSession = session.defaultSession;
    const cookiesObj = cookies.split(';').map(cookie => {
      const [name, value] = cookie.trim().split('=');
      return { name, value }; 
    });
    cookiesObj.forEach(cookie => {
      const encodedValue = encodeURIComponent(cookie.value);
      appSession.cookies.set({
        url: 'http://music.163.com/api/song/enhance/player',
        name: cookie.name, 
        value: encodedValue
      })
    });
    console.log('successfully set cookie')
  }
})

async function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize

  // Create the browser window.
  win = new BrowserWindow({
    width: width / 2,
    height: height,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
    }
  })
  win.maximize()
  
  const currentTime = new Date();
  const currentHour = currentTime.getHours();
  let greeting = '';

  if (currentHour >= 0 && currentHour < 12) {
    greeting = 'CreamPlayer - Good Morning';
  } else if (currentHour >= 12 && currentHour < 19) {
    greeting = 'CreamPlayer - Good Afternoon';
  } else {
    greeting = 'CreamPlayer - Good Evening';
  }

  win.webContents.on('did-finish-load', () => {
    win.webContents.executeJavaScript(`document.title = "${greeting}"`)
  })

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  app.commandLine.appendSwitch('disable-web-security')
  app.commandLine.appendSwitch('ignore-certificate-errors')

  createWindow()
})
// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
