'use strict'

// map
const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const apiUrl = 'http://127.0.0.1:3000/';
const startLocation = 'EFHK';
const airportMarkers = L.featureGroup().addTo(map);

// icons kartan kohdissa
const blueIcon = L.divIcon({ className: 'blue-icon' });
const greenIcon = L.divIcon({ className: 'green-icon '});

// from for player name
document.querySelector('player-name').addEventListener('submit', function(event){
  event.preventDefault();
  const playerName = document.querySelector('player-name').value;
});

/*
async function getData(url) {
  const response = await
}

 */


//////// game status update (mitä edes tarvitaan budjetin lisäksi?)
function updateStatus(status) {
  document.querySelector('budget').innerHTML = status.co2.budget;
}




/* check if game is over
function checkGameStatus(budget) {
  if budget
}

 */



