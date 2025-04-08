const { app, Menu, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const Database = require("better-sqlite3");

const db = new Database("data.sqlite");

db.exec(
  "CREATE TABLE IF NOT EXISTS gecmis (isim TEXT, tarih DATE, ucret INTEGER, islem TEXT)"
);

function createWindow() {
  const win = new BrowserWindow({
    width: 1024,
    height: 560,
    resizable: false,
    maximizable: true,
    minimizable: true,
    webPreferences: {
      devTools: true,
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  Menu.setApplicationMenu(null);
  app.commandLine.appendSwitch("disable-features", "OverlayScrollbar");
  win.loadFile("masaustuisyeri/index.html");
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  app.quit();
});


ipcMain.on("veri-gonder", (event, data) => {
  const stmt = db.prepare(
    "INSERT INTO gecmis (isim, tarih, ucret, islem) VALUES (?, ?, ?, ?)"
  );
  stmt.run(data.isim, data.tarih, data.ucret, data.islem);
  console.log("Veri kaydedildi:", data);
});


ipcMain.handle("veri-cek", () => {
  return db.prepare("SELECT * FROM gecmis").all();
});


require("electron-reload")(__dirname, {
  electron: path.join(__dirname, "node_modules", ".bin", "electron"),
});
