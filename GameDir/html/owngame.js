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
const startingMarker = [60.3172, 24.9633];
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
  document.querySelector('#ohjeet').classList.add('hide');
  document.querySelector('#kysymysbox').classList.remove('hide');
  //document.querySelector('#player-model').classList.add('hide'); // ei toimi for now
  //mainGame(`${playerName}&loc=${startLocation}`);
  mainGame(startingMarker, startLocation);

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

// nyt toimi ((((:
function helsinkiVantaa(){
  map.flyTo(startingMarker, 8);
  const mark = L.marker(startingMarker)
      .addTo(map)
      .bindPopup(`Starting point`)
      .openPopup()
      .setIcon(greenIcon);
  airportMarkers.addLayer(mark);
  console.log('im here');
  document.querySelector('#kysymysbox').classList.add('hide');

}
helsinkiVantaa();
uppdateStatus();

async function mainGame(location, name) {
    try {
        const gameData = await getData('http://127.0.0.1:3000/airports/');
        console.log(gameData);
        console.log(location);
        airportMarkers.clearLayers();

        // lisää tämänhetkien lokaatio
         const marker = L.marker(location).addTo(map);
            airportMarkers.addLayer(marker);
                 marker.setIcon(greenIcon);
                map.flyTo(location, 8);
                marker.bindPopup(`You are here: <b>${name}</b>`);
                marker.openPopup();
                document.querySelector('#country').innerHTML = `Kysymys at ${name}`;

        for (const airport of gameData) {
            // lisätään muut kolme
            const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
            airportMarkers.addLayer(marker);
            marker.setIcon(blueIcon);
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            h4.innerHTML = airport.airportName;
            popupContent.append(h4);
            // button
            const goButton = document.createElement('button');
            goButton.classList.add('button');
            goButton.innerHTML = 'Go here';

            console.log(goButton);

            popupContent.appendChild(goButton);
            marker.bindPopup(popupContent);

            goButton.addEventListener('click', () => {
                map.flyTo([airport.latitude_deg, airport.longitude_deg], 8);
                marker.bindPopup(`You are here: <b>${airport.countryName} , ${airport.airportName}</b>`)
                    .openPopup();
                document.querySelector('#country').innerHTML = `Kysymys at ${airport.countryName}`;
                mainGame([airport.latitude_deg, airport.longitude_deg], airport.airportName);
                });
            }
        } catch (error) {
        console.log(error);
    }
    gameQuestion();
    // kysymysboksi näkyviin
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

        uppdateStatus()
      } else {
        alert('Väärin, mene seruaavaan maahan ja vastaa kysymykseen!')
        document.querySelector('#kysymysbox').classList.add('hide');
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

gameQuestion();
correct_check();