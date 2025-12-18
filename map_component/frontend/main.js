const { Streamlit } = window;

const map = L.map("map").setView([35, 135], 5);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap",
}).addTo(map);

let marker = null;

map.on("click", (e) => {
  const lat = e.latlng.lat;
  const lng = e.latlng.lng;

  if (marker) {
    map.removeLayer(marker);
  }
  marker = L.marker([lat, lng]).addTo(map);

  // Python に値を返す
  Streamlit.setComponentValue({
    lat: lat,
    lng: lng,
  });
});

// Streamlit に高さを通知（超重要）
Streamlit.setFrameHeight();
