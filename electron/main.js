const { app, BrowserWindow, ipcMain, shell } = require("electron/main");
const { exec } = require("child_process");
const { join } = require("path");
const path = require("path");
const fs = require("fs");

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

// Create the main Electron window
function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: join(__dirname, "preload.js"),
    },
    autoHideMenuBar: true,
  });

  if (process.env.NODE_ENV === "development") {
    win.loadURL("http://localhost:3000");
    win.maximize();
    win.webContents.openDevTools();
  } else {
    win.loadFile(path.join(__dirname, "dist/index.html"));
  }
}

ipcMain.handle("download", async (event, args) => {
  const binPath = join(__dirname, "musicdownloader.py");

  return new Promise((resolve) => {
    runScript(
      `python "${binPath}"`,
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
