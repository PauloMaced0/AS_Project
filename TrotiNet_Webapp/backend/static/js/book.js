var scooterIcon = L.icon({
  iconUrl: "./static/img/interfaceImage/scooter.png",
  iconSize: [30, 30],
});

var userIcon = L.icon({
  iconUrl: "./static/img/interfaceImage/user.png",
  iconSize: [35, 35],
});

function resizeMarkers() {
  var zoomLevel = map.getZoom();

  var newSize;

  if (zoomLevel >= 18) {
    newSize = [25, 25];
  } else if (zoomLevel >= 15 && zoomLevel <= 17) {
    newSize = [30, 30];
  } else {
    newSize = [35, 35];
  }

  // Update the icon size for each marker
  markers.forEach(function (marker) {
    marker.setIcon(L.icon({
      iconUrl: './static/img/interfaceImage/scooter.png',
      iconSize: newSize,
    }));
  });
}

var markers = [];

const user_location = { "lat": 40.633202419864595, "long": -8.65943696039659 }
var map = L.map('map_book').setView([user_location.lat - 0.00080, user_location.long], 17);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

L.marker([user_location.lat, user_location.long], { icon: userIcon }).addTo(map);

function displayDataOnMap(data) {
  data.record.scooter_location.forEach(function (scooter) {
    var lat = scooter.lat;
    var long = scooter.long;
    var batt = scooter.batt;
    let battery_state;

    if (batt >= 60 && batt <= 100) {
      battery_state = '<i class="bi bi-battery-full" style="font-size: 20px; color:green;"></i>'
    } else if (batt >= 21 && batt <= 59) {
      battery_state = '<i class="bi bi-battery-half" style="font-size: 20px; color:orange;"></i>'
    } else if (batt >= 0 && batt <= 20) {
      battery_state = '<i class="bi bi-battery" style="font-size: 20px; color:red;"></i>'
    }

    var marker = L.marker([lat, long], { icon: scooterIcon }).addTo(map);
    marker
      .bindPopup('<div class="d-flex align-items-center"> Battery:&nbsp <strong>' + batt + '%</strong>&nbsp' + battery_state + '</div>')
      .on('click', function () {
        console.log(batt);
      });
    markers.push(marker);
  });
}
map.on('zoomend', resizeMarkers);

$.getJSON("https://api.jsonbin.io/v3/b/646f7a938e4aa6225ea401ee", function (data) {
  displayDataOnMap(data);
});

function setDateInput() {
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  let month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
  let day = currentDate.getDate().toString().padStart(2, '0');

  const formattedDate = `${year}-${month}-${day}`;
  document.getElementById("dateInput").value = formattedDate;
}

setDateInput();

$(".leaflet-control-attribution").remove();

$(".leaflet-control-zoom").remove();