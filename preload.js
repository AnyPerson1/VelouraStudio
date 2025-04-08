const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  veriEkle: (data) => ipcRenderer.send("veri-gonder", data),
  veriCek: () => ipcRenderer.invoke("veri-cek"),
});
