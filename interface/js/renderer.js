document.getElementById('DownloadFileButton').addEventListener('click', () => {
  window.electronAPI.downloadURL("http://localhost:8000/download");
});