const { exec } = require("node:child_process");
const fs = require("node:fs");
const { join } = require("node:path");
const path = require("node:path");
const { session } = require("electron");
const { app, BrowserWindow, ipcMain, shell } = require("electron/main");

let loginwindow;

async function runscript(binpath, args, onsuccess, onerror) {
  exec(binpath + args, (error, stdout, stderr) => {
    if (error) {
      console.error("Error running script:", error.message);
      if (onerror)
        onerror(error, stderr);
      return;
    }

    console.warn(binpath + args);
    console.warn("Script output:", stdout);

    if (stdout.includes("success")) {
      console.warn("Script execution successful");
      if (onsuccess)
        onsuccess(stdout);
    } else {
      console.error("Unexpected script output");
      if (onerror)
        onerror(new Error("Unexpected script output"), stdout);
    }
  });
}

function createwindow() {
  const win = new BrowserWindow({
    width: 900,
    height: 800,
    webPreferences: {
      preload: join(__dirname, "preload.cjs"),
    },
    title: "Creamplayer",
    autoHideMenuBar: true,
  });

  if (require("node:process").env.NODE_ENV === "development") {
    win.loadURL("http://localhost:3000");
    win.maximize();
    win.webContents.openDevTools();
  } else {
    win.loadFile("./dist/index.html");
  }
}

function createloginwindow() {
  loginwindow = new BrowserWindow({
    width: 800,
    height: 600,
  });

  loginwindow.loadURL("https://music.163.com/login");

  loginwindow.on("closed", () => {
    loginwindow = null;
  });
}

ipcMain.handle("netease-login", async () => {
  if (loginwindow) {
    loginwindow.focus();
  } else {
    createloginwindow();
  }
});

ipcMain.handle("get-netease-login", async () => {
  try {
    const cookies = await loginwindow.webContents.session.cookies.get({
      url: "https://music.163.com",
    });
    const cookiestring = cookies
      .map(cookie => `${cookie.name}=${cookie.value}`)
      .join("; ");

    return cookiestring;
  } catch {
    return null;
  }
});

ipcMain.handle("close-netease-login", async () => {
  if (loginwindow) {
    loginwindow.close();
    loginwindow = null;
  }
});

ipcMain.handle("download", async (_, args) => {
  const binpath = join("./resources/musicdownloader.exe");

  return new Promise((resolve) => {
    runscript(
      binpath,
      args,
      (stdout) => {
        const match = stdout.match(/successfully:(.*)/);
        if (match && match[1]) {
          const result = match[1].trim();
          const decodedurl = decodeURIComponent(result);

          resolve(decodedurl);
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

ipcMain.handle("open", async (_, relativepath) => {
  const absolutepath = path.resolve(relativepath);
  if (fs.existsSync(absolutepath)) {
    shell.showItemInFolder(absolutepath);
  } else {
    console.error("Path does not exist:", absolutepath);
  }
});

app.whenReady().then(() => {
  createwindow();

  const defaultsession = session.defaultSession;
  defaultsession.webRequest.onBeforeSendHeaders((details, callback) => {
    const cookievalue = details.requestHeaders.flag;
    if (cookievalue) {
      delete details.requestHeaders.flag;
      details.requestHeaders.Cookie = cookievalue;
    }

    callback({ requestHeaders: details.requestHeaders });
  });

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createwindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (require("node:process").platform !== "darwin") {
    app.quit();
  }
});
