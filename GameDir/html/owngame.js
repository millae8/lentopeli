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
const leimat = 0;
const co2_budget = 9000;


// icons kartan kohdissa
const blueIcon = L.divIcon({ className: 'blue-icon' });
const greenIcon = L.divIcon({ className: 'green-icon '});

//const nimi = document.querySelector('#player-form');
//console.log(nimi);

// from for player name
document.querySelector('#player-form').addEventListener('submit', function (event){
  event.preventDefault();
  const playerName = document.querySelector('#player-input').value;
  console.log(playerName);
  //document.querySelector('#player-model').classList.add('hide'); // ei toimi for now
  //mainGame(`${playerName}&loc=${startLocation}`);
  mainGame(playerName);

});


// game status update
function uppdateStatus() {
  document.querySelector('#co2_budget').innerHTML = co2_budget;
  document.querySelector('#leimat').innerHTML = leimat;
}



/* check if game is over
function checkGameStatus(budget) {
  if budget
}
*/

// function to fetch data from API
async function getData(url) {
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

// tää function ei toimi :((((
function helsinkiVantaa(){
  const startingMarker = [60.3172, 24.9633];
  map.flyTo(startingMarker, 8);
  const mark = L.marker(startingMarker)
      .addTo(map)
      .bindPopup(`Starting point`)
      .setIcon(greenIcon);
  airportMarkers.addLayer(mark);
  console.log('im here');

}
helsinkiVantaa();
uppdateStatus();

async function mainGame() {
    try {
        const gameData = await getData('http://127.0.0.1:3000/airports/');
        console.log(gameData);

        for (const airport of gameData) {
            const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map); // untill tänne it works
            ////////// tästä eteenpäin toimi
            if (airport) {
                marker.bindPopup(`You are here: ${airport.countryName} , ${airport.airportName}`);
                marker.openPopup();
               // marker.setIcon(blueIcon); tää ei toimiiiiiiiii
            } else {
                marker.setIcon(blueIcon);
                const popupContent = document.createElement('div');
                const box = document.createElement('box');
                box.innerHTML = airport.airportName;
                popupContent.append(box);
                const goButton = document.createElement('button');
                goButton.classList('button');
                goButton.innerHTML = 'Go here';
                popupContent.append(goButton);
                const p = document.createElement('p');
                p.innerHTML = `Distance x km`;
                popupContent.append(p);
                marker.bindPopup(popupContent);
            }
        }

    } catch (error) {
        console.log(error);
    }
}

/*
async function mainGame(){
    const gameData = await getData('http://127.0.0.1:3000/airports/');
    console.log(gameData);
    for (const airport of gameData) {
        const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map); // untill tänne it works
        marker.bindPopup(`You are here: ${airport.airportName}`);
        console.log(airport.airportName);
        marker.openPopup();
        // tässä supposed to be when you choose an airport to go to
       // marker.setIcon(blueIcon);
  }
}

 */


async function gameQuestion() {
    const questionData = await getData('http://127.0.0.1:3000/questions/');
        document.getElementById('question'). innerHTML = questionData.question;
        document.getElementById('correct_answer').innerHTML = questionData.correct_answer;
}


function correct_check(correct_answer) {
  for (let x of document.getElementsByName('options')) {
    if (x.checked) {
      if (x.value === correct_answer) {
        alert('Oikein!');
        // status.leimat += 1 ?
      } else {
        alert('Väärin :(')
      }
    }
  }
}

document.getElementById('submit').addEventListener('click', async function (event) {
  event.preventDefault()
  const questionData = await getData('http://127.0.0.1:3000/questions/');
  correct_check(questionData.correct_answer);
});

// turkki
async function getTurkki(){
    try {
        const turkkiData = await getData('http://127.0.0.1:3000/turkki/');
        console.log(turkkiData);
    } catch (error) {
        console.log(error);
    }

}
/// until here works
        /*
        const {latitude_deg, longitude_deg} = turkkiData
        const countryMarker = L.marker([latitude_deg, longitude_deg]).addTo(map);
        countryMarker.bindPopup(`you are here ${countryName}`).openPopup();
        map.setView([latitude_deg, longitude_deg], 6);
    } catch (error) {
        console.log(error)
    }
}

getTurkki();

*/

//helsinkiVantaa();
//gameQuestion();