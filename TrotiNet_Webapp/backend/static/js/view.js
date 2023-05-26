// Create a Leaflet map objectd

const scooter = {"lat":40.6384849216439 ,"long": -8.651193883281309 };
var map = L.map('map_trip').setView([scooter.lat, scooter.long], 18);

// Add a tile layer from OpenStreetMap
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(map);

L.marker([scooter.lat, scooter.long]).addTo(map)

$(".leaflet-control-attribution").remove();

$(".leaflet-control-zoom").remove();