let panorama;
let map;
let marker;
const latty = parseFloat(document.getElementById("333").textContent);
const longgy = parseFloat(document.getElementById("4444").textContent);
document.getElementById("333").remove();
document.getElementById("4444").remove();

function resetLocation() {
  panorama.setPosition({
    lat: latty,
    lng: longgy
  });
}

function initStreetView() {
  // Set the panorama options
  panorama = new google.maps.StreetViewPanorama(document.getElementById("pano"), {
    position: {
      lat: latty,
      lng: longgy
    },
    pov: {
      heading: 0,
      pitch: 0
    },
    fullscreenControl: false,
    disableDefaultUI: true,
    showRoadLabels: false,
  });
  // Set the map options
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: {
      lat: 39.728493,
      lng: -121.837479
    },
    disableDefaultUI: true,
    fullscreenControl: true,
    keyboardShortcuts: false,
  });
  // Disable double click zoom
  map.setOptions({
    disableDoubleClickZoom: true,
    clickableIcons: false,
    styles: [{
      featureType: 'transit',
      elementType: 'labels',
      stylers: [{
        visibility: 'off'
      }]
    }, ]
  });

  // Update the hidden form fields with the initial marker position
  updateFormFields(map.getCenter().lat(), map.getCenter().lng());
  // Update the marker position when the user double clicks on the map

  map.addListener("dblclick", (event) => {
    if (marker) {
      marker.setPosition(event.latLng);
    } else {
      marker = new google.maps.Marker({
        position: event.latLng,
        map: map,
        draggable: false,
      });
    }
    const submitButton = document.getElementById("submitButton")
    submitButton.disabled = false;
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    updateFormFields(lat, lng);
  });
}
const updateFormFields = (lat, lng) => {
  const guessLatField = document.getElementById("id_guessLat");
  const guessLngField = document.getElementById("id_guessLng");
  guessLatField.value = lat;
  guessLngField.value = lng;
}
const mappy = document.getElementById("mapWrapper")
const actualMap = document.getElementById("map")
const submitBtn = document.getElementById("submitButton")
if (window.innerWidth > 750 && window.innerHeight > 600) {
  mappy.addEventListener('mouseover', () => {
    actualMap.style.height = '400px';
    actualMap.style.width = '550px';
  });
  mappy.addEventListener('mouseleave', () => {
    actualMap.style.height = '250px';
    actualMap.style.width = '250px';
  });
} else {
  mappy.addEventListener("touchstart", () => {
    document.getElementById("mapWrapper").style.opacity = "1";
  })
  mappy.addEventListener("touchend", () => {
    document.getElementById("mapWrapper").style.opacity = "0.55";
  });
}

const timerElement = document.getElementById("time");
// Retrieve the current round number
const currentRound = parseFloat(document.getElementById("5555").textContent);
document.getElementById("5555").remove();
let storedRound = localStorage.getItem("round");
let totalTime;
// Check if the stored round matches the current round
if (storedRound && parseInt(storedRound) === currentRound) {
  // Use stored time if rounds match
  totalTime = parseInt(localStorage.getItem("time")) || 60;
} else {
  // Reset time to 60 seconds if rounds do not match
  totalTime = 60;
}
const countdown = setInterval(() => {
  let minutes = Math.floor(totalTime / 60);
  let seconds = totalTime % 60;
  minutes = minutes < 10 ? '0' + minutes : minutes;
  seconds = seconds < 10 ? '0' + seconds : seconds;
  timerElement.textContent = minutes + ":" + seconds;
  // Store the current round and time in localStorage
  localStorage.setItem("time", totalTime);
  localStorage.setItem("round", currentRound);
  if (totalTime <= 0) {
    clearInterval(countdown);
    if(parseFloat(document.getElementById("id_guessLat").value) != 39.728493 && parseFloat(document.getElementById("id_guessLng").value) != -121.837479) {
      document.getElementById("id_guessLat").value = -1;
      document.getElementById("id_guessLng").value = -1;
    }
    document.getElementById("submitButton").disabled = false;
    document.getElementById("submitButton").click();
  }
  totalTime--;
}, 1000);

// Make the initStreetView function global
window.initStreetView = initStreetView;