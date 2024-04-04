self.addEventListener("install", event => {
    console.log("The service worker or cache for COTSEye has been installed.");

    event.waitUntil(
        Promise.all([
            caches.open("public/service/index").then(cache => {
                cache.addAll([
                    "/statics/templates/public/service/index/index.html",

                    
                    "{% static 'css/public/service/index/index.css' %}",


                    "{% static 'templates/webwares/application.js' %}",
                    
                    "{% static 'templates/webwares/manifest.json' %}",
                    
                    
                    "{% static 'assets/icons/logo.png' %}",

                    "{% static 'assets/icons/logo (180 x 180).png' %}",

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
                    "{% url 'Public Service Home' %}",
                    
                    "/statics/templates/public/service/home/home.html",
                    
                    
                    "{% static 'css/public/service/home/home.css' %}",


                    "{% static 'assets/maps/google' %}/11/1731/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1731/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1731/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1731/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1731/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1731/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1731/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1732/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1732/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1732/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1732/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1732/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1732/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1732/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1733/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1733/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1733/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1733/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1733/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1733/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1733/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1734/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1734/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1734/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1734/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1734/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1734/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1734/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1735/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1735/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1735/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1735/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1735/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1735/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1735/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1736/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1736/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1736/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1736/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1736/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1736/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1736/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1737/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1737/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1737/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1737/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1737/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1737/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1737/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1738/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1738/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1738/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1738/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1738/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1738/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1738/993.jpg",
                    
                    "{% static 'assets/maps/google' %}/11/1739/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1739/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1739/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1739/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1739/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1739/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1739/993.jpg",

                    "{% static 'assets/maps/google' %}/11/1740/987.jpg",

                    "{% static 'assets/maps/google' %}/11/1740/988.jpg",

                    "{% static 'assets/maps/google' %}/11/1740/989.jpg",

                    "{% static 'assets/maps/google' %}/11/1740/990.jpg",

                    "{% static 'assets/maps/google' %}/11/1740/991.jpg",

                    "{% static 'assets/maps/google' %}/11/1740/992.jpg",

                    "{% static 'assets/maps/google' %}/11/1740/993.jpg",


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