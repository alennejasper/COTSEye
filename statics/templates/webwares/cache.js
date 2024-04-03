self.addEventListener("install", event => {
    console.log("The service worker or cache for COTSEye has been installed.");

    event.waitUntil(
        Promise.all([
            caches.open("public/service/index").then(cache => {
                cache.addAll([
                    "/statics/templates/public/service/index/index.html",
                    
                    "/statics/css/public/service/index/index.css",


                    "/statics/templates/webwares/application.js",
                    
                    "/statics/templates/webwares/manifest.json",
                    

                    "/statics/assets/icons/logo.png",
                    
                    "/statics/assets/icons/logo (72 x 72).png",
                    
                    "/statics/assets/icons/logo (96 x 96).png",
                    
                    "/statics/assets/icons/logo (120 x 120).png",
                    
                    "/statics/assets/icons/logo (128 x 128).png",
                    
                    "/statics/assets/icons/logo (144 x 144).png",
                    
                    "/statics/assets/icons/logo (152 x 152).png",
                    
                    "/statics/assets/icons/logo (180 x 180).png",
                    
                    "/statics/assets/icons/logo (192 x 192).png",
                    
                    "/statics/assets/icons/logo (384 x 384).png",
                    
                    "/statics/assets/icons/logo (512 x 512).png",

                    "https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&display=swap",
                    
                    "https://fonts.googleapis.com/css2?family=Overlock:wght@400;700;900&display=swap",
                    
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
                    
                    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
                    
                    "https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js",
                    
                    "https://cdn.jsdelivr.net/npm/sweetalert2@11"
                ]);
            }),

            caches.open("public/service/home").then(cache => {
                cache.addAll([
                    "/statics/templates/public/service/home/home.html",
                    
                    "/statics/css/public/service/home/home.css",
                    

                    "https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&display=swap",
                    
                    "https://fonts.googleapis.com/css2?family=Overlock:wght@400;700;900&display=swap",
                ]);
            })
        ])
    );
});



self.addEventListener("activate", event => {
    console.log("The service worker or cache for COTSEye has been activated.");
});


self.addEventListener("fetch", event => {
    console.log("The service worker or cache for COTSEye has fetched an object.", event);
});