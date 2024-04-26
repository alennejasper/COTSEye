self.addEventListener("install", event => {
    console.log("The service worker or cache for COTSEye has been installed.");

    event.waitUntil(
        caches.open("service/index").then(cache => {
            cache.addAll([                    
                "public/service/fallback/",

                "contributor/service/fallback/",


                "/statics/templates/public/service/index/index.html",

                "/statics/templates/contributor/service/index/index.html",

                "/statics/templates/public/service/fallback/fallback.html",

                "/statics/templates/contributor/service/fallback/fallback.html",

                
                "/statics/css/public/service/index/index.css",

                "/statics/css/contributor/service/index/index.css",

                "/statics/css/public/service/fallback/fallback.css",

                "/statics/css/contributor/service/fallback/fallback.css",


                "/statics/templates/webwares/application.js",
                                
                
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

                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2",

                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.ttf",
                
                "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
                
                "https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js",
                
                "https://cdn.jsdelivr.net/npm/sweetalert2@11",
            ]);
        })
    );
});


self.addEventListener("activate", event => {
    console.log("The service worker or cache for COTSEye has been activated.");

    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.filter( key => key !== "service/index" && key !== "service/whole").map(key => caches.delete(key))
            )
        })
    );    
});

  
self.addEventListener("fetch", event => {
    console.log("The service worker or cache for COTSEye has fetched an object.", event);

    const limit = (name, size) => {
        caches.open(name).then(cache => {
            cache.keys().then(keys => {
                if(keys.length > size){
                    cache.delete(keys[0]).then(() => limit(name, size));
                };
            });
        })
    };

    event.respondWith(
        caches.match(event.request).then(response => {
            if(response){
                const expiration = 1 * 60 * 1000;

                const today = new Date().getTime();
                
                const age = new Date(response.headers.get("date")).getTime();

                if(today - age > expiration){
                    return fetch(event.request).then(fetch => {
                        const clone = fetch.clone();

                        caches.open("service/whole").then(cache => {
                            cache.put(event.request, clone);

                            limit("service/whole", 50);
                        });

                        return fetch;
                    });

                } else{
                    return response;
                };
                
            } else{
                return fetch(event.request).then(response => {
                    const clone = response.clone();

                    caches.open("service/whole").then(cache => {
                        cache.put(event.request, clone);

                        limit("service/whole", 50);
                    });

                    return response;

                }).catch(() => {
                    if (event.request.url.includes("contributor/")) {
                        return caches.match("contributor/service/fallback/");

                    } else {
                        return caches.match("public/service/fallback/");
                    };
                });
            };
        })
    );
});