if ("serviceWorker" in navigator){
    navigator.serviceWorker.register("/cache.js", {scope: "/contributor"})
        .then((register) => console.log("The service worker or cache for COTSEye is now registered.", register))

        .catch((error) => console.log("The service worker or cache for COTSEye cannot be registered.", error));
    
    navigator.serviceWorker.register("/cache.js", {scope: "/public"})
        .then((register) => console.log("The service worker or cache for COTSEye is now registered.", register))

        .catch((error) => console.log("The service worker or cache for COTSEye cannot be registered.", error));
};