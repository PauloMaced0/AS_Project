// Create a Leaflet map object
var map = L.map('map_book').setView([41.14278390310927, -8.612213735423238], 17);

// Add a tile layer from OpenStreetMap
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(map);

$.getJSON("https://api.jsonbin.io/v3/b/64442b4b8e4aa6225e8ec932", function (data) {
  var restaurants = L.geoJSON(data.record.features, {
    pointToLayer: function (feature, latlng) {
      return L.marker(latlng)
    },
  }).addTo(map);
});

$(".leaflet-control-attribution").remove();

$(".leaflet-control-zoom").remove();