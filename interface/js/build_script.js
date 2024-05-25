const packager = require('electron-packager');
const options = {
    dir: ".",
    out: "dist",
    platform: "win32"
};

packager(options)
    .then(appPaths => {
        console.log("Electron app has been packaged at", appPaths);
    })
    .catch(error => {
        console.error("Error packaging Electron app:", error);
    });
