'use strict'

// map
/* 1. show map using Leaflet library. (L comes from the Leaflet library) */

const map = L.map('map', { tap: false });
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);

/*
const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

 */

const apiUrl = 'http://127.0.0.1:3000/';
const startLocation = 'EFHK';
const airportMarkers = L.featureGroup().addTo(map);

// icons kartan kohdissa
const blueIcon = L.divIcon({ className: 'blue-icon' });
const greenIcon = L.divIcon({ className: 'green-icon '});

const nimi = document.querySelector('#player-form');
console.log(nimi);

// from for player name
document.querySelector('#player-form').addEventListener('submit', function (event){
  event.preventDefault();
  const playerName = document.querySelector('#player-input').value;
  console.log(playerName);
  mainGame(nimi);
});

/*
async function getData(url) {
  const response = await fetch(url);
  if ( !response.ok) {
  throw new Error('Invalid server input');
  const data = await response.json();
  return data;
}
 */

// game status update, (mitä tänne tarvitaan vielä?)
function uppdateStatus(status) {
  document.querySelector('#buget').innerHTML = status.co2.budget;

}

// function to show kysymykset?
function getQuestions(airport) {
  document.querySelector('#question').innerHTML = '' ;

}






/* check if game is over
function checkGameStatus(budget) {
  if budget
}


// function to fetch data from API
async function getData(url) {
  const response = await fetch(url);
  const data = response.json();
  console.log(data)

 */


async function mainGame(nimi) {
  const response = await fetch('http://127.0.0.1:3000/airports/');
  const gamedata = await response.json();
  console.log(gamedata);
  airportMarkers.clearLayers();
  // add marker
  for (const location of gamedata) {
    console.log(location.latitude_deg);
    console.log(location.longitude_deg);
    const marker = L.marker([location.latitude_deg, location.longitude_deg]).
      addTo(map).
      bindPopup('moimoimoi').
        setIcon(blueIcon).
      openPopup();
    airportMarkers.addLayer(marker);
  }

  // pan map to selected airport
  map.flyTo([airport.latitude_deg, airport.longitude_deg]);
}



