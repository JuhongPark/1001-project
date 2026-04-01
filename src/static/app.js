/**
 * LightMap Boston - Frontend Map Application
 */

const BOSTON_CENTER = [-71.065, 42.355];
const TILES_DAY = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json";
const TILES_NIGHT = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json";

let map;
let currentMode = "day";
let shadowData = null;
let streetlightData = null;
let businessData = null;
let buildingData = null;
let sliderDebounceTimer = null;
let weatherTimer = null;
let canopyData = null;
let floodData = null;
let iceData = null;
let crimeNightData = null;

function D(msg) { fetch("/api/debug?msg=" + encodeURIComponent(msg)); }

// ── Initialization ──

async function init() {
    D("init: creating map");
    map = new maplibregl.Map({
        container: "map",
        style: TILES_DAY,
        center: BOSTON_CENTER,
        zoom: 15,
        attributionControl: true,
    });

    map.addControl(new maplibregl.NavigationControl(), "bottom-left");

    map.on("load", async () => {
        D("map.load fired");
        try {
            await loadStaticData();
            D("loadStaticData done");
            setupSlider();
            setupLayerToggles();
            setupClickInspect();
            setupCursorInteraction();
            D("calling updateFromSlider");
            await updateFromSlider();
            D("updateFromSlider done");
            showOnboarding();
            setupAboutPanel();
            startWeatherUpdates();
        } catch (err) {
            D("INIT ERROR: " + err.message);
            hideLoading();
        }
    });

    map.on("error", (e) => {
        D("MAP ERROR: " + (e.error ? e.error.message : "unknown"));
    });
}

// ── Onboarding ──

function showOnboarding() {
    if (sessionStorage.getItem("lightmap-onboarded")) return;
    const el = document.createElement("div");
    el.id = "onboarding";
    el.innerHTML = `
        <div class="onboarding-content">
            <b>LightMap Boston</b>
            <p class="tagline">Find shade by day. Find light by night.</p>
            <p>Drag the time slider to watch shadows move. At night, see which streets are well-lit.</p>
            <p>Click anywhere on the map for details.</p>
            <button id="onboarding-close">Got it</button>
        </div>
    `;
    document.body.appendChild(el);
    const escHandler = (e) => { if (e.key === "Escape") dismiss(); };
    const dismiss = () => {
        el.remove();
        sessionStorage.setItem("lightmap-onboarded", "1");
        document.removeEventListener("keydown", escHandler);
    };
    document.getElementById("onboarding-close").addEventListener("click", dismiss);
    document.addEventListener("keydown", escHandler);
}

// ── Helpers ──

function coordsToGeoJSON(coords) {
    return {
        type: "FeatureCollection",
        features: coords.map(function(c) {
            return {
                type: "Feature",
                geometry: { type: "Point", coordinates: c },
                properties: {},
            };
        }),
    };
}

// ── Data Loading ──

async function loadStaticData() {
    D("loadStaticData: start");
    showLoading("Loading map data...");
    try {
        const bldRes = await fetch("/api/buildings");
        if (!bldRes.ok) throw new Error("buildings HTTP " + bldRes.status);
        buildingData = await bldRes.json();
        D("loadStaticData: buildings loaded, " + buildingData.features.length);
    } catch (err) {
        D("loadStaticData ERROR: " + err.message);
        showError("Failed to load map data. Please refresh the page.");
    } finally {
        hideLoading();
    }
}

async function loadNightData() {
    if (streetlightData && businessData) return;
    D("loadNightData: start");
    showLoading("Loading night data...");
    try {
        const [slRes, bizRes] = await Promise.all([
            fetch("/api/streetlights"),
            fetch("/api/businesses"),
        ]);
        if (!slRes.ok || !bizRes.ok) throw new Error("night data HTTP error");
        const slRaw = await slRes.json();
        businessData = await bizRes.json();
        streetlightData = coordsToGeoJSON(slRaw.coords);
        D("loadNightData: done, sl=" + streetlightData.features.length + " biz=" + businessData.features.length);
    } catch (err) {
        D("loadNightData ERROR: " + err.message);
        showError("Failed to load night data. Please try again.");
    } finally {
        hideLoading();
    }
}

async function loadShadows(timeStr) {
    D("loadShadows: " + timeStr);
    const res = await fetch("/api/shadows?time=" + encodeURIComponent(timeStr));
    if (!res.ok) throw new Error("shadows HTTP " + res.status);
    shadowData = await res.json();
    D("loadShadows: done, " + shadowData.features.length + " features");
    return shadowData;
}

// ── Map Layers ──

function addDayLayers() {
    D("addDayLayers: start");
    try {
        if (!map.getSource("shadows")) {
            map.addSource("shadows", {
                type: "geojson",
                data: shadowData || { type: "FeatureCollection", features: [] },
            });
            map.addLayer({
                id: "shadows-fill",
                type: "fill",
                source: "shadows",
                paint: { "fill-color": "#334155", "fill-opacity": 0.35 },
            });
        } else {
            map.getSource("shadows").setData(
                shadowData || { type: "FeatureCollection", features: [] }
            );
        }

        if (!map.getSource("buildings") && buildingData) {
            map.addSource("buildings", {
                type: "geojson",
                data: buildingData,
            });
            map.addLayer({
                id: "buildings-fill",
                type: "fill",
                source: "buildings",
                paint: { "fill-color": "#94a3b8", "fill-opacity": 0.7 },
            });
            map.addLayer({
                id: "buildings-outline",
                type: "line",
                source: "buildings",
                paint: { "line-color": "#475569", "line-width": 0.8 },
            });
        }
        D("addDayLayers: done");
    } catch (err) {
        D("addDayLayers ERROR: " + err.message);
    }
}

function addNightLayers() {
    D("addNightLayers: start");
    try {
        if (!map.getSource("streetlights")) {
            map.addSource("streetlights", {
                type: "geojson",
                data: streetlightData || { type: "FeatureCollection", features: [] },
            });
            map.addLayer({
                id: "streetlights-heat",
                type: "heatmap",
                source: "streetlights",
                paint: {
                    "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 10, 4, 14, 12, 18, 24],
                    "heatmap-opacity": 0.7,
                    "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 10, 0.5, 14, 1, 18, 2],
                    "heatmap-color": [
                        "interpolate", ["linear"], ["heatmap-density"],
                        0, "rgba(0,0,0,0)", 0.2, "#1e3a5f", 0.4, "#2563eb",
                        0.6, "#60a5fa", 0.8, "#fbbf24", 1.0, "#ffffff",
                    ],
                },
            });
        }

        if (!map.getSource("businesses")) {
            map.addSource("businesses", {
                type: "geojson",
                data: businessData || { type: "FeatureCollection", features: [] },
            });
            map.addLayer({
                id: "businesses-circle",
                type: "circle",
                source: "businesses",
                paint: {
                    "circle-radius": ["interpolate", ["linear"], ["zoom"], 10, 2, 15, 4, 18, 7],
                    "circle-color": "#f97316",
                    "circle-opacity": 0.8,
                    "circle-stroke-width": 0.5,
                    "circle-stroke-color": "#ffffff",
                },
            });
        }
        D("addNightLayers: done");
    } catch (err) {
        D("addNightLayers ERROR: " + err.message);
    }
}

function setLayerVisibility(layerId, visible) {
    if (map.getLayer(layerId)) {
        map.setLayoutProperty(layerId, "visibility", visible ? "visible" : "none");
    }
}

// ── Mode Switching ──

async function switchMode(info) {
    const newMode = info.is_day ? "day" : "night";
    const modeChanged = newMode !== currentMode;
    D("switchMode: newMode=" + newMode + " currentMode=" + currentMode + " changed=" + modeChanged);

    if (modeChanged) {
        const newStyle = info.is_day ? TILES_DAY : TILES_NIGHT;
        const center = map.getCenter();
        const zoom = map.getZoom();
        const bearing = map.getBearing();
        const pitch = map.getPitch();

        D("switchMode: calling setStyle");
        map.setStyle(newStyle);

        // Wait for style.load with timeout
        await new Promise((resolve) => {
            const timeout = setTimeout(() => {
                D("switchMode: style.load TIMEOUT after 10s");
                resolve();
            }, 10000);
            map.once("style.load", () => {
                clearTimeout(timeout);
                D("switchMode: style.load fired");
                resolve();
            });
        });

        map.setCenter(center);
        map.setZoom(zoom);
        map.setBearing(bearing);
        map.setPitch(pitch);
        currentMode = newMode;
    }

    if (info.is_day) {
        addDayLayers();
        setLayerVisibility("shadows-fill", document.getElementById("toggle-shadows").checked);
        setLayerVisibility("buildings-fill", document.getElementById("toggle-buildings").checked);
        setLayerVisibility("buildings-outline", document.getElementById("toggle-buildings").checked);
    } else {
        addNightLayers();
        setLayerVisibility("streetlights-heat", document.getElementById("toggle-streetlights").checked);
        setLayerVisibility("businesses-circle", document.getElementById("toggle-businesses").checked);
    }

    updateUI(info);
    D("switchMode: done");
}

// ── UI Updates ──

function describeSun(altitude) {
    if (altitude <= 0) return "Nighttime";
    if (altitude < 10) return "Sunrise/sunset \u2014 very long shadows";
    if (altitude < 25) return "Low sun \u2014 long shadows";
    if (altitude < 45) return "Moderate sun \u2014 medium shadows";
    if (altitude < 65) return "High sun \u2014 short shadows";
    return "Overhead \u2014 minimal shadows";
}

function updateUI(info) {
    const isNight = !info.is_day;
    const modeIcon = info.is_day ? "\u2600\uFE0F" : "\uD83C\uDF19";
    const modeText = info.is_day ? "Shadow Map" : "Brightness Map";

    const modeEl = document.getElementById("info-mode");
    modeEl.textContent = modeIcon + " " + modeText;
    if (modeEl.dataset.lastMode && modeEl.dataset.lastMode !== modeText) {
        modeEl.classList.add("mode-flash");
        setTimeout(() => modeEl.classList.remove("mode-flash"), 1200);
    }
    modeEl.dataset.lastMode = modeText;
    document.getElementById("info-time").textContent = formatTime(info.time);
    document.getElementById("info-sun").textContent = describeSun(info.sun_altitude);

    const statsEl = document.getElementById("info-stats");
    if (info.is_day && shadowData && shadowData.metadata) {
        statsEl.textContent = shadowData.metadata.building_count.toLocaleString() + " buildings analyzed";
        statsEl.style.display = "block";
    } else if (!info.is_day && streetlightData) {
        statsEl.textContent = streetlightData.features.length.toLocaleString() + " streetlights mapped";
        statsEl.style.display = "block";
    } else {
        statsEl.style.display = "none";
    }

    ["info-panel", "time-control", "layer-control", "legend", "weather-panel"].forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.classList.toggle("night", isNight);
    });

    document.getElementById("legend-day").style.display = info.is_day ? "block" : "none";
    document.getElementById("legend-night").style.display = info.is_day ? "none" : "block";

    document.getElementById("toggle-shadows").closest("label").style.display = info.is_day ? "block" : "none";
    document.getElementById("toggle-buildings").closest("label").style.display = info.is_day ? "block" : "none";
    document.getElementById("toggle-trees").closest("label").style.display = info.is_day ? "block" : "none";
    document.getElementById("toggle-streetlights").closest("label").style.display = info.is_day ? "none" : "block";
    document.getElementById("toggle-businesses").closest("label").style.display = info.is_day ? "none" : "block";
    document.getElementById("toggle-crime").closest("label").style.display = info.is_day ? "none" : "block";
}

function formatTime(isoStr) {
    const d = new Date(isoStr);
    return d.toLocaleString("en-US", {
        month: "short", day: "numeric", year: "numeric",
        hour: "numeric", minute: "2-digit", hour12: true,
    });
}

// ── Time Slider ──

function setupSlider() {
    const slider = document.getElementById("time-slider");
    slider.addEventListener("input", () => {
        updateSliderLabel(slider.value);
        clearTimeout(sliderDebounceTimer);
        sliderDebounceTimer = setTimeout(() => updateFromSlider(), 300);
    });
    const now = new Date();
    const currentMinutes = now.getHours() * 60 + Math.floor(now.getMinutes() / 30) * 30;
    slider.value = currentMinutes;
    updateSliderLabel(currentMinutes);
}

function updateSliderLabel(minutes) {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    const ampm = h >= 12 ? "PM" : "AM";
    const h12 = h === 0 ? 12 : h > 12 ? h - 12 : h;
    document.getElementById("slider-label").textContent =
        h12 + ":" + String(m).padStart(2, "0") + " " + ampm;
}

async function updateFromSlider() {
    const minutes = parseInt(document.getElementById("time-slider").value);
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    const today = new Date();
    const timeStr = today.getFullYear() + "-" +
        String(today.getMonth() + 1).padStart(2, "0") + "-" +
        String(today.getDate()).padStart(2, "0") + "T" +
        String(h).padStart(2, "0") + ":" + String(m).padStart(2, "0");

    D("updateFromSlider: " + timeStr);
    showLoading("Updating...");

    try {
        D("updateFromSlider: fetching info");
        const infoRes = await fetch("/api/info?time=" + encodeURIComponent(timeStr));
        if (!infoRes.ok) throw new Error("info HTTP " + infoRes.status);
        const info = await infoRes.json();
        D("updateFromSlider: info mode=" + info.mode);

        if (info.is_day) {
            await loadShadows(timeStr);
        } else {
            await loadNightData();
        }

        D("updateFromSlider: calling switchMode");
        await switchMode(info);
        D("updateFromSlider: complete");
    } catch (err) {
        D("updateFromSlider ERROR: " + err.message);
        showError("Connection lost. Please try again.");
    } finally {
        hideLoading();
    }
}

// ── Layer Toggles ──

function setupLayerToggles() {
    document.getElementById("toggle-shadows").addEventListener("change", (e) => {
        setLayerVisibility("shadows-fill", e.target.checked);
    });
    document.getElementById("toggle-buildings").addEventListener("change", (e) => {
        setLayerVisibility("buildings-fill", e.target.checked);
        setLayerVisibility("buildings-outline", e.target.checked);
    });
    document.getElementById("toggle-trees").addEventListener("change", (e) => {
        toggleTreeCanopy(e.target.checked);
    });
    document.getElementById("toggle-streetlights").addEventListener("change", (e) => {
        setLayerVisibility("streetlights-heat", e.target.checked);
    });
    document.getElementById("toggle-businesses").addEventListener("change", (e) => {
        setLayerVisibility("businesses-circle", e.target.checked);
    });
    document.getElementById("toggle-flood").addEventListener("change", (e) => {
        toggleHazardLayer("flood", e.target.checked);
    });
    document.getElementById("toggle-ice").addEventListener("change", (e) => {
        toggleHazardLayer("ice", e.target.checked);
    });
    document.getElementById("toggle-crime").addEventListener("change", (e) => {
        toggleHazardLayer("crime", e.target.checked);
    });
}

// ── Hazard / Safety Layers ──

async function toggleHazardLayer(type, show) {
    if (!show) {
        setLayerVisibility(type + "-heat", false);
        var legendHazard = document.getElementById("legend-hazard");
        var anyActive = document.getElementById("toggle-flood").checked ||
                        document.getElementById("toggle-ice").checked;
        legendHazard.style.display = anyActive ? "block" : "none";
        return;
    }

    var data = null;
    if (type === "flood") {
        if (!floodData) {
            D("loading flood data");
            var res = await fetch("/api/hazards/flood");
            var raw = await res.json();
            floodData = coordsToGeoJSON(raw.coords);
        }
        data = floodData;
    } else if (type === "ice") {
        if (!iceData) {
            D("loading ice data");
            var res = await fetch("/api/hazards/ice");
            var raw = await res.json();
            iceData = coordsToGeoJSON(raw.coords);
        }
        data = iceData;
    } else if (type === "crime") {
        if (!crimeNightData) {
            D("loading crime night data");
            var res = await fetch("/api/safety/nighttime");
            var raw = await res.json();
            crimeNightData = coordsToGeoJSON(raw.coords);
        }
        data = crimeNightData;
    }

    if (!data) return;

    var layerId = type + "-heat";
    var sourceId = type + "-source";

    if (!map.getSource(sourceId)) {
        map.addSource(sourceId, { type: "geojson", data: data });
        var color = type === "flood" ? "#2563eb" : type === "ice" ? "#9333ea" : "#ef4444";
        map.addLayer({
            id: layerId,
            type: "heatmap",
            source: sourceId,
            paint: {
                "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 10, 6, 14, 15, 18, 25],
                "heatmap-opacity": 0.5,
                "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 10, 0.3, 14, 0.8, 18, 1.5],
                "heatmap-color": [
                    "interpolate", ["linear"], ["heatmap-density"],
                    0, "rgba(0,0,0,0)", 0.3, color + "33", 0.6, color + "88", 1.0, color,
                ],
            },
        });
    }
    setLayerVisibility(layerId, true);

    var legendHazard = document.getElementById("legend-hazard");
    legendHazard.style.display = "block";
}

// ── Cursor Interaction ──

function setupCursorInteraction() {
    const interactiveLayers = ["shadows-fill", "buildings-fill", "businesses-circle"];
    map.on("mousemove", (e) => {
        const layers = interactiveLayers.filter((id) => map.getLayer(id));
        if (layers.length === 0) return;
        const features = map.queryRenderedFeatures(e.point, { layers });
        map.getCanvas().style.cursor = features.length > 0 ? "pointer" : "";
    });
}

// ── Click to Inspect ──

let mapPopup = null;

function setupClickInspect() {
    mapPopup = new maplibregl.Popup({ closeButton: false, maxWidth: "220px" });

    map.on("click", (e) => {
        const layers = ["shadows-fill", "buildings-fill", "businesses-circle"].filter(
            (id) => map.getLayer(id)
        );
        const features = map.queryRenderedFeatures(e.point, { layers });
        let html = "";

        if (features.length > 0) {
            const f = features[0];
            if (f.layer.id === "shadows-fill") {
                const height = Math.round(f.properties.height_ft);
                const shadowLen = Math.round(f.properties.shadow_len_m);
                html = "<b>Shaded area</b><br>" + height + " ft building<br>Shadow extends ~" + shadowLen + " m";
            } else if (f.layer.id === "buildings-fill") {
                const height = f.properties.BLDG_HGT_2010;
                if (height) {
                    const heightM = Math.round(height * 0.3048);
                    const stories = Math.round(height / 12);
                    html = "<b>Building</b><br>" + Math.round(height) + " ft (" + heightM + " m)<br>~" + stories + " stories";
                } else {
                    html = "<b>Building</b><br>Height data unavailable";
                }
            } else if (f.layer.id === "businesses-circle") {
                html = "<b>" + (f.properties.name || "Unknown") + "</b>";
            }
        } else if (currentMode === "night" && streetlightData) {
            const clickLng = e.lngLat.lng;
            const clickLat = e.lngLat.lat;
            if (clickLat < 42.22 || clickLat > 42.41 || clickLng < -71.20 || clickLng > -70.92) {
                mapPopup.remove();
                return;
            }
            let nearbyCount = 0;
            const radius = 0.002;
            for (const f of streetlightData.features) {
                const [lng, lat] = f.geometry.coordinates;
                const dx = lng - clickLng;
                const dy = lat - clickLat;
                if (dx * dx + dy * dy < radius * radius) nearbyCount++;
            }
            let level, desc;
            if (nearbyCount >= 15) { level = "Well-lit area"; desc = "Good visibility at night"; }
            else if (nearbyCount >= 8) { level = "Moderately lit"; desc = "Some visibility"; }
            else if (nearbyCount >= 3) { level = "Dimly lit"; desc = "Limited visibility"; }
            else { level = "Dark area"; desc = "Very low visibility"; }
            html = "<b>" + level + "</b><br>" + desc + "<br><span style='opacity:0.7'>" + nearbyCount + " streetlights nearby</span>";
        }

        if (!html) { mapPopup.remove(); return; }

        mapPopup.remove();
        mapPopup.setLngLat(e.lngLat).setHTML(html);
        if (currentMode === "night") {
            mapPopup.addClassName("night-popup");
        } else {
            mapPopup.removeClassName("night-popup");
        }
        mapPopup.addTo(map);
    });
}

// ── Loading / Error ──

function showLoading(text) {
    let el = document.querySelector(".loading-indicator");
    if (!el) {
        el = document.createElement("div");
        el.className = "loading-indicator";
        el.innerHTML = '<div class="spinner"></div><span></span>';
        document.body.appendChild(el);
    }
    el.querySelector("span").textContent = text;
    el.style.display = "flex";
}

function hideLoading() {
    const el = document.querySelector(".loading-indicator");
    if (el) el.style.display = "none";
}

function showError(text) {
    let el = document.querySelector(".error-toast");
    if (!el) {
        el = document.createElement("div");
        el.className = "error-toast";
        document.body.appendChild(el);
    }
    el.textContent = text;
    el.style.display = "block";
    setTimeout(() => { el.style.display = "none"; }, 5000);
}

// ── Tree Canopy ──

async function toggleTreeCanopy(show) {
    if (!show) {
        setLayerVisibility("canopy-heat", false);
        return;
    }
    if (!canopyData) {
        D("loading canopy density");
        showLoading("Loading tree data...");
        try {
            var res = await fetch("/api/canopy/density");
            var raw = await res.json();
            canopyData = coordsToGeoJSON(raw.coords);
            D("canopy loaded: " + canopyData.features.length);
        } catch (err) {
            D("canopy ERROR: " + err.message);
            hideLoading();
            return;
        }
        hideLoading();
    }
    if (!map.getSource("canopy-source")) {
        map.addSource("canopy-source", { type: "geojson", data: canopyData });
        map.addLayer({
            id: "canopy-heat",
            type: "heatmap",
            source: "canopy-source",
            paint: {
                "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 10, 4, 14, 10, 18, 20],
                "heatmap-opacity": 0.4,
                "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 10, 0.3, 14, 0.6, 18, 1],
                "heatmap-color": [
                    "interpolate", ["linear"], ["heatmap-density"],
                    0, "rgba(0,0,0,0)", 0.3, "#bbf7d0", 0.6, "#4ade80", 1.0, "#16a34a",
                ],
            },
        });
    }
    setLayerVisibility("canopy-heat", true);
}

// ── About Panel ──

function setupAboutPanel() {
    document.getElementById("about-toggle").addEventListener("click", function() {
        var panel = document.getElementById("about-panel");
        panel.style.display = panel.style.display === "none" ? "block" : "none";
        if (currentMode === "night") panel.classList.add("night");
        else panel.classList.remove("night");
    });
    document.getElementById("about-close").addEventListener("click", function() {
        document.getElementById("about-panel").style.display = "none";
    });
}

// ── Weather Panel ──

async function fetchWeather() {
    try {
        const res = await fetch("/api/weather");
        if (!res.ok) return;
        const w = await res.json();
        updateWeatherPanel(w);
    } catch (err) {
        D("fetchWeather ERROR: " + err.message);
    }
}

function updateWeatherPanel(w) {
    document.getElementById("weather-temp").textContent = w.temperature_f + "\u00B0F";
    document.getElementById("weather-condition").textContent = w.weather_description;

    var uvEl = document.getElementById("weather-uv");
    if (currentMode === "day") {
        uvEl.textContent = "UV " + w.uv_index;
        uvEl.style.display = "block";
    } else {
        uvEl.style.display = "none";
    }

    var aqiText = "AQI " + w.aqi;
    if (w.aqi > 100) {
        aqiText += " (Unhealthy)";
    } else if (w.aqi > 50) {
        aqiText += " (Moderate)";
    }
    document.getElementById("weather-aqi").textContent = aqiText;

    var alertEl = document.getElementById("weather-alert");
    alertEl.className = "";
    alertEl.textContent = "";
    var snowCodes = [71, 73, 75];
    if (snowCodes.indexOf(w.weather_code) !== -1) {
        alertEl.textContent = "Snow";
        alertEl.className = "snow";
    } else if (w.is_raining) {
        alertEl.textContent = "Rain";
        alertEl.className = "rain";
    }
}

function startWeatherUpdates() {
    fetchWeather();
    weatherTimer = setInterval(fetchWeather, 300000);
}

// ── Start ──

init();
