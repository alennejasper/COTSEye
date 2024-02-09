self.addEventListener("install", event => {
    console.log("The service worker or cache for COTSEye has been installed.");
});

self.addEventListener("activate", event => {
    console.log("The service worker or cache for COTSEye has been activated.");
});

self.addEventListener("fetch", event => {
    console.log("The service worker or cache for COTSEye has fetched an object.", event);
});