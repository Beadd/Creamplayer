const { app, BrowserWindow, ipcMain, shell } = require("electron/main");
const { exec } = require("child_process");
const { join } = require("path");
const path = require("path");
const fs = require("fs");
const { session } = require("electron");

let loginWindow;

// Function to execute Python scripts
async function runScript(binPath, args, onSuccess, onError) {
  exec(binPath + args, (error, stdout, stderr) => {
    if (error) {
      console.error("Error running script:", error.message);
      if (onError) onError(error, stderr);
      return;
    }

    console.log(binPath + args);
    console.log("Script output:", stdout);

    if (stdout.includes("success")) {
      console.log("Script execution successful");
      if (onSuccess) onSuccess(stdout);
    } else {
      console.error("Unexpected script output");
      if (onError) onError(new Error("Unexpected script output"), stdout);
    }
  });
}

function setTitle(win) {
  const currentTime = new Date();
  const currentHour = currentTime.getHours();
  let greeting = "";

  if (currentHour >= 0 && currentHour < 12) {
    greeting = "Creamplayer - Good Morning";
  } else if (currentHour >= 12 && currentHour < 19) {
    greeting = "Creamplayer - Good Afternoon";
  } else {
    greeting = "Creamplayer - Good Evening";
  }

  win.webContents.on("did-finish-load", () => {
    win.webContents.executeJavaScript(`document.title = "${greeting}"`);
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 700,
    webPreferences: {
      preload: join(__dirname, "preload.cjs"),
    },
    title: "Creamplayer",
    autoHideMenuBar: true,
  });
  setTitle(win);

  if (process.env.NODE_ENV === "development") {
    win.loadURL("http://localhost:5173");
    win.maximize();
    win.webContents.openDevTools();
  } else {
    win.loadFile("./dist/index.html");
  }
}

function createLoginWindow() {
  loginWindow = new BrowserWindow({
    width: 800,
    height: 600,
  });

  loginWindow.loadURL("https://music.163.com/login");

  loginWindow.on("closed", () => {
    loginWindow = null;
  });
}

ipcMain.handle("netease-login", async () => {
  if (loginWindow) {
    loginWindow.focus();
  } else {
    createLoginWindow();
  }
});

ipcMain.handle("get-netease-login", async () => {
  try {
    const cookies = await loginWindow.webContents.session.cookies.get({
      url: "https://music.163.com",
    });
    const cookieString = cookies
      .map((cookie) => `${cookie.name}=${cookie.value}`)
      .join("; ");

    return cookieString;
  } catch (error) {
    return null;
  }
});

ipcMain.handle("download", async (event, args) => {
  const binPath = join("./resources/musicdownloader.exe");

  return new Promise((resolve) => {
    runScript(
      binPath,
      args,
      (stdout) => {
        const match = stdout.match(/successfully:(.*)/);
        if (match && match[1]) {
          const result = match[1].trim();
          const decodedUrl = decodeURIComponent(result);

          resolve(decodedUrl);
        } else {
          resolve(null);
        }
      },
      (error) => {
        console.error("Download failed", error);
        resolve(false);
      },
    );
  });
});

ipcMain.handle("open", async (event, relativePath) => {
  const absolutePath = path.resolve(relativePath);
  if (fs.existsSync(absolutePath)) {
    shell.showItemInFolder(absolutePath);
  } else {
    console.error("Path does not exist:", absolutePath);
  }
});

// Electron app lifecycle
app.whenReady().then(() => {
  createWindow();

  // Allow to set cookie
  const defaultSession = session.defaultSession;
  defaultSession.webRequest.onBeforeSendHeaders((details, callback) => {
    const cookieValue = details.requestHeaders["flag"];
    if (cookieValue) {
      delete details.requestHeaders["flag"];
      details.requestHeaders.Cookie = cookieValue;
    }

    callback({ requestHeaders: details.requestHeaders });
  });

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
