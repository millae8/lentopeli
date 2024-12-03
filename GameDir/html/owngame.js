'use strict'

// map
const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const startLocation = 'EFHK';
const airportMarkers = L.featureGroup().addTo(map);

// icons kartan kohdissa
const blueIcon = L.divIcon({ className: 'blue-icon' });
const greenIcon = L.divIcon({ className: 'green-icon '});

// from for player player name
document.querySelector('player-form').addEventListener('submit', function (event){
    event.preventDefault();
    const playerName = document.querySelector('player-name').value;

})


searchForm.addEventListener('click', async function(event){
    event.preventDefault();
    const response = await fetch('http://127.0.0.1:3000/airport/');
    const airport = await response.json();
    console.log(airport);
    // remove possible other markers
    airportMarkers.clearLayers();

})

async function getData(url) {
    const response = await fetch(url);
    if (response.ok) throw new Error('invalid server input :(');
    const data = await response.json();
    console.log(data);
    return data;
}