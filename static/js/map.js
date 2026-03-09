let map;
let markers = [];
let routingControl = null;
let userLocation = null;
let userMarker = null;
let activeCard = null;
let activeCategory = "human";

var CHENNAI_DEFAULT = { lat: 13.0827, lng: 80.2707 };

function initMap() {
    map = L.map("map", {
        center: [CHENNAI_DEFAULT.lat, CHENNAI_DEFAULT.lng],
        zoom: 13,
        zoomControl: false
    });

    L.control.zoom({ position: "topright" }).addTo(map);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    userLocation = { lat: CHENNAI_DEFAULT.lat, lng: CHENNAI_DEFAULT.lng };

    geocodeLocationInput();
    bindSearchEvents();
    bindCategoryToggle();
    loadMedicineList();
}

function geocodeLocation(query) {
    return fetch("https://nominatim.openstreetmap.org/search?format=json&q=" + encodeURIComponent(query) + "&countrycodes=in&limit=1")
        .then(function (res) { return res.json(); })
        .then(function (data) {
            if (data.length > 0) {
                userLocation = {
                    lat: parseFloat(data[0].lat),
                    lng: parseFloat(data[0].lon)
                };
            } else {
                userLocation = { lat: CHENNAI_DEFAULT.lat, lng: CHENNAI_DEFAULT.lng };
            }
            placeUserMarker();
            return userLocation;
        })
        .catch(function () {
            userLocation = { lat: CHENNAI_DEFAULT.lat, lng: CHENNAI_DEFAULT.lng };
            placeUserMarker();
            return userLocation;
        });
}

function placeUserMarker() {
    if (userMarker) {
        map.removeLayer(userMarker);
    }

    var icon = L.divIcon({
        className: "user-location-marker",
        html: '<div class="user-marker-dot"><div class="user-marker-pulse"></div></div>',
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });

    userMarker = L.marker([userLocation.lat, userLocation.lng], { icon: icon, zIndexOffset: 1000 }).addTo(map);
    userMarker.bindPopup('<div class="info-window"><h3>📍 Your Location</h3></div>', {
        className: "leaflet-custom-popup",
        maxWidth: 200
    });
}

function geocodeLocationInput() {
    var input = document.getElementById("location-input");

    input.addEventListener("change", function () {
        var query = input.value.trim();
        if (!query) return;

        geocodeLocation(query).then(function (loc) {
            map.setView([loc.lat, loc.lng], 14);
        });
    });
}

function resolveUserLocation() {
    if (userLocation) return userLocation;
    userLocation = { lat: CHENNAI_DEFAULT.lat, lng: CHENNAI_DEFAULT.lng };
    return userLocation;
}

function bindSearchEvents() {
    var searchBtn = document.getElementById("search-btn");
    var medicineInput = document.getElementById("medicine-input");

    searchBtn.addEventListener("click", performSearch);
    medicineInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            performSearch();
        }
    });
}

function performSearch() {
    var query = document.getElementById("medicine-input").value.trim();
    if (!query) return;

    var locationQuery = document.getElementById("location-input").value.trim();

    var resultsSection = document.getElementById("results-section");
    var emptyState = document.getElementById("empty-state");
    var loadingState = document.getElementById("loading-state");

    emptyState.classList.add("hidden");
    resultsSection.classList.add("hidden");
    loadingState.classList.remove("hidden");
    document.getElementById("medicine-list-section").classList.add("hidden");

    clearMarkers();
    clearRoute();

    var locationPromise;
    if (locationQuery) {
        locationPromise = geocodeLocation(locationQuery).then(function (loc) {
            map.setView([loc.lat, loc.lng], 14);
            return loc;
        });
    } else {
        resolveUserLocation();
        locationPromise = Promise.resolve(userLocation);
    }

    locationPromise.then(function () {
        return fetch("/search?medicine=" + encodeURIComponent(query) + "&category=" + activeCategory);
    })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            loadingState.classList.add("hidden");

            if (data.source === "verified" && data.results.length > 0) {
                renderVerifiedResults(data.results);
            } else if (data.source === "fallback" || data.results.length === 0) {
                searchNearbyPharmacies();
            } else {
                emptyState.classList.remove("hidden");
            }
        })
        .catch(function () {
            loadingState.classList.add("hidden");
            emptyState.classList.remove("hidden");
        });
}

function renderVerifiedResults(results) {
    var resultsSection = document.getElementById("results-section");
    var resultsList = document.getElementById("results-list");
    var resultsTitle = document.getElementById("results-title");
    var resultsBadge = document.getElementById("results-badge");

    if (userLocation) {
        results.forEach(function (item) {
            item._dist = haversineJs(userLocation.lat, userLocation.lng, item.lat, item.lng);
        });
        results.sort(function (a, b) { return a._dist - b._dist; });
    }

    resultsTitle.textContent = results.length + " Verified " + (results.length === 1 ? "Pharmacy" : "Pharmacies");
    resultsBadge.className = "badge verified";
    resultsBadge.textContent = "✓ Verified Stock";

    resultsList.innerHTML = "";

    var bounds = L.latLngBounds();

    results.forEach(function (item, index) {
        var pos = [item.lat, item.lng];
        bounds.extend(pos);

        var marker = createMarker(pos, item.pharmacy, "verified");
        markers.push(marker);

        marker.on("click", function () {
            showPopup(marker, item);
        });

        var distText = (item._dist !== undefined) ? item._dist + " km" : "";

        var li = document.createElement("li");
        li.className = "result-card";
        li.style.animationDelay = (index * 0.06) + "s";
        li.innerHTML =
            '<div class="card-top">' +
            '<span class="pharmacy-name">' + escapeHtml(item.pharmacy) + '</span>' +
            '<span class="stock-badge verified">Verified</span>' +
            '</div>' +
            '<div class="card-address">' + escapeHtml(item.address) + '</div>' +
            '<div class="card-meta">' +
            '<span class="card-phone">📞 ' + escapeHtml(item.phone || "N/A") + '</span>' +
            (distText ? '<span class="card-distance">📍 ' + distText + '</span>' : '<span class="card-timestamp">Updated: ' + formatTimestamp(item.last_updated) + '</span>') +
            '</div>' +
            '<button class="directions-btn" data-lat="' + item.lat + '" data-lng="' + item.lng + '">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 22l10-6 10 6L12 2z"/></svg>' +
            'Get Directions' +
            '</button>';

        li.addEventListener("click", function () {
            map.setView(pos, 16);
            showPopup(marker, item);
            setActiveCard(li);
        });

        li.querySelector(".directions-btn").addEventListener("click", function (e) {
            e.stopPropagation();
            getDirections({ lat: parseFloat(this.dataset.lat), lng: parseFloat(this.dataset.lng) });
        });

        resultsList.appendChild(li);
    });

    map.fitBounds(bounds, { padding: [60, 60] });
    resultsSection.classList.remove("hidden");
}

function searchNearbyPharmacies() {
    resolveUserLocation();

    var amenity = (activeCategory === "pet") ? "veterinary" : "pharmacy";
    var overpassQuery = '[out:json][timeout:10];node["amenity"="' + amenity + '"](around:5000,' + userLocation.lat + ',' + userLocation.lng + ');out body 5;';

    fetch("https://overpass-api.de/api/interpreter?data=" + encodeURIComponent(overpassQuery))
        .then(function (res) { return res.json(); })
        .then(function (data) {
            if (data.elements && data.elements.length > 0) {
                renderFallbackResults(data.elements.slice(0, 5));
            } else {
                document.getElementById("empty-state").classList.remove("hidden");
            }
        })
        .catch(function () {
            document.getElementById("empty-state").classList.remove("hidden");
        });
}

function renderFallbackResults(places) {
    var resultsSection = document.getElementById("results-section");
    var resultsList = document.getElementById("results-list");
    var resultsTitle = document.getElementById("results-title");
    var resultsBadge = document.getElementById("results-badge");

    if (userLocation) {
        places.forEach(function (place) {
            place._dist = haversineJs(userLocation.lat, userLocation.lng, place.lat, place.lon);
        });
        places.sort(function (a, b) { return a._dist - b._dist; });
    }

    resultsTitle.textContent = places.length + " Unverified Nearby " + (places.length === 1 ? "Pharmacy" : "Pharmacies");
    resultsBadge.className = "badge fallback";
    resultsBadge.textContent = "Unverified Nearby";

    resultsList.innerHTML = "";

    var bounds = L.latLngBounds();
    if (userLocation) bounds.extend([userLocation.lat, userLocation.lng]);

    places.forEach(function (place, index) {
        var pos = [place.lat, place.lon];
        var name = (place.tags && place.tags.name) ? place.tags.name : "Pharmacy";
        var address = (place.tags && place.tags["addr:full"]) ? place.tags["addr:full"] : ((place.tags && place.tags["addr:street"]) ? place.tags["addr:street"] : "Address unavailable");
        bounds.extend(pos);

        var distText = (place._dist !== undefined) ? place._dist + " km" : "";

        var marker = createMarker(pos, name, "fallback");
        markers.push(marker);

        marker.on("click", function () {
            showPopup(marker, {
                pharmacy: name,
                address: address,
                phone: (place.tags && place.tags.phone) ? place.tags.phone : null,
                last_updated: null,
                _dist: place._dist
            });
        });

        var li = document.createElement("li");
        li.className = "result-card";
        li.style.animationDelay = (index * 0.06) + "s";
        li.innerHTML =
            '<div class="card-top">' +
            '<span class="pharmacy-name">' + escapeHtml(name) + '</span>' +
            '<span class="stock-badge fallback">Unverified</span>' +
            '</div>' +
            '<div class="card-address">' + escapeHtml(address) + '</div>' +
            '<div class="card-meta">' +
            '<span class="card-phone">📍 Nearby pharmacy</span>' +
            (distText ? '<span class="card-distance">' + distText + '</span>' : '') +
            '</div>' +
            '<button class="directions-btn" data-lat="' + place.lat + '" data-lng="' + place.lon + '">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 22l10-6 10 6L12 2z"/></svg>' +
            'Get Directions' +
            '</button>';

        li.addEventListener("click", function () {
            map.setView(pos, 16);
            setActiveCard(li);
        });

        li.querySelector(".directions-btn").addEventListener("click", function (e) {
            e.stopPropagation();
            getDirections({ lat: parseFloat(this.dataset.lat), lng: parseFloat(this.dataset.lng) });
        });

        resultsList.appendChild(li);
    });

    map.fitBounds(bounds, { padding: [60, 60] });
    resultsSection.classList.remove("hidden");
}

function createMarker(position, title, type) {
    var colors = {
        verified: "#22c55e",
        fallback: "#fbbf24"
    };

    var color = colors[type] || "#6366f1";

    var icon = L.divIcon({
        className: "custom-marker",
        html: '<div style="' +
            "width:20px;height:20px;border-radius:50%;background:" + color + ";" +
            "border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.4);" +
            '"></div>',
        iconSize: [20, 20],
        iconAnchor: [10, 10],
        popupAnchor: [0, -12]
    });

    return L.marker(position, { icon: icon, title: title }).addTo(map);
}

function showPopup(marker, item) {
    var content =
        '<div class="info-window">' +
        '<h3>' + escapeHtml(item.pharmacy) + '</h3>' +
        '<p>' + escapeHtml(item.address) + '</p>';

    if (item.phone) {
        content += '<p>📞 ' + escapeHtml(item.phone) + '</p>';
    }
    if (item._dist !== undefined) {
        content += '<p>📍 ' + item._dist + ' km away</p>';
    }
    if (item.last_updated) {
        content += '<p>Updated: ' + formatTimestamp(item.last_updated) + '</p>';
    }
    content += '</div>';

    marker.bindPopup(content, {
        className: "leaflet-custom-popup",
        maxWidth: 280,
        minWidth: 200
    }).openPopup();
}

function getDirections(destination) {
    clearRoute();

    var origin = L.latLng(userLocation.lat, userLocation.lng);

    routingControl = L.Routing.control({
        waypoints: [
            origin,
            L.latLng(destination.lat, destination.lng)
        ],
        router: L.Routing.osrmv1({
            serviceUrl: "https://router.project-osrm.org/route/v1"
        }),
        lineOptions: {
            styles: [
                { color: "#6366f1", weight: 6, opacity: 0.85 }
            ],
            addWaypoints: false
        },
        createMarker: function () { return null; },
        addWaypoints: false,
        draggableWaypoints: false,
        fitSelectedRoutes: true,
        show: true,
        collapsible: true,
        showAlternatives: false
    }).addTo(map);
}

function clearRoute() {
    if (routingControl) {
        map.removeControl(routingControl);
        routingControl = null;
    }
}

function clearMarkers() {
    markers.forEach(function (m) { map.removeLayer(m); });
    markers = [];
    activeCard = null;
}

function setActiveCard(card) {
    if (activeCard) activeCard.classList.remove("active");
    card.classList.add("active");
    activeCard = card;
    card.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function formatTimestamp(ts) {
    if (!ts) return "N/A";
    var date = new Date(ts);
    var now = new Date();
    var diffMs = now - date;
    var diffHrs = Math.floor(diffMs / 3600000);

    if (diffHrs < 1) return "Just now";
    if (diffHrs < 24) return diffHrs + "h ago";
    var diffDays = Math.floor(diffHrs / 24);
    if (diffDays === 1) return "1 day ago";
    if (diffDays < 7) return diffDays + " days ago";
    return date.toLocaleDateString("en-IN", { day: "numeric", month: "short" });
}

function escapeHtml(str) {
    if (!str) return "";
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

function haversineJs(lat1, lng1, lat2, lng2) {
    var R = 6371.0;
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLng = (lng2 - lng1) * Math.PI / 180;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLng / 2) * Math.sin(dLng / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * c * 100) / 100;
}

function loadMedicineList() {
    fetch("/medicines?category=" + activeCategory)
        .then(function (res) { return res.json(); })
        .then(function (data) {
            var container = document.getElementById("medicine-tags");
            var countBadge = document.getElementById("medicine-count-badge");

            countBadge.textContent = data.length + " available";
            container.innerHTML = "";

            data.forEach(function (med) {
                var tag = document.createElement("button");
                tag.className = "medicine-tag";
                tag.innerHTML = '<span class="tag-name">' + escapeHtml(med.name) + '</span><span class="tag-count">' + med.shops + ' shops</span>';
                tag.addEventListener("click", function () {
                    document.getElementById("medicine-input").value = med.name;
                    performSearch();
                });
                container.appendChild(tag);
            });
        });
}

function bindCategoryToggle() {
    var buttons = document.querySelectorAll(".category-btn");
    buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            if (btn.dataset.category === activeCategory) return;

            buttons.forEach(function (b) { b.classList.remove("active"); });
            btn.classList.add("active");
            activeCategory = btn.dataset.category;

            document.getElementById("medicine-input").value = "";
            document.getElementById("results-section").classList.add("hidden");
            document.getElementById("empty-state").classList.add("hidden");
            document.getElementById("medicine-list-section").classList.remove("hidden");
            clearMarkers();
            clearRoute();
            loadMedicineList();
        });
    });
}

document.addEventListener("DOMContentLoaded", initMap);
