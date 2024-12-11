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
const startLocation = 'Helsinki-Vantaa';
const startingMarker = [60.3172, 24.9633];
const airportMarkers = L.featureGroup().addTo(map);
let leimat = 0;
let co2_budget = 3500;
let coranswer;


// icons kartan kohdissa
const blueIcon = L.divIcon({ className: 'blue-icon' });
const greenIcon = L.divIcon({ className: 'green-icon '});

//const nimi = document.querySelector('#player-form');
//console.log(nimi);

// from for player name
document.querySelector('#player-form').addEventListener('submit', function (event){
  event.preventDefault();
  const playerName = document.querySelector('#player-input').value;
  document.querySelector('#player-modal').classList.add('hide');
  console.log(playerName);
  document.querySelector('#ohjeet').classList.add('hide');
  document.querySelector('#kysymysbox').classList.remove('hide');
  //document.querySelector('#player-model').classList.add('hide'); // if peli dont generate maat open this and take the one above away, but it should work
    // toisaalta nyt oihjeet ei näy hyvin ja peli alkaa heti kysymyksistä
  mainGame(startingMarker, startLocation);

});

// game status update
function updateStatus() {
  document.querySelector('#co2_budget').innerHTML = co2_budget;
  document.querySelector('#leimat').innerHTML = leimat;
}

// function to fetch data from API
async function getData(url) {
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

/* function checkLeimat(leimat){
  if (leimat === 5) {
    alert('olet kerännyt 5 leimaa')
    console.log(leimat + 'fuck')
  }
} */

function checkLeimat() {
  if (leimat === 5) {
    // SweetAlert 2 for game over
    Swal.fire({
      icon: 'success',
      title: 'Victory!',
      text: 'Olet kerännyt 5 leimaa!',
      showCancelButton: true,
      confirmButtonText: 'Restart',
      cancelButtonText: 'Close',
      allowOutsideClick: false
    }).then((result) => {
      if (result.isConfirmed) {
        // Restart the game
        location.reload(); // Restarts the game by reloading the page
      } else {
        console.log('Victory, but the player chose not to restart.');
      }
    });
  }
}

function checkBudget(co2_budget) {
  if (co2_budget <= 0) {
    // SweetAlert 2 for game over
    Swal.fire({
      icon: 'error',
      title: 'Game Over!',
      text: 'Budjettisis on loppu, hävisit pelin!',
      showCancelButton: true,
      confirmButtonText: 'Restart',
      cancelButtonText: 'Close',
      allowOutsideClick: false
    }).then((result) => {
      if (result.isConfirmed) {
        // Restart the game
        location.reload(); // Restarts the game by reloading the page
      } else {
        console.log('Game over, but the player chose not to restart.');
      }
    });
  }
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
                // budget update
                co2_budget -= 500;
                updateStatus(co2_budget);
                // check if there is no
                checkBudget(co2_budget);
                map.flyTo([airport.latitude_deg, airport.longitude_deg], 8);

                marker.bindPopup(`You are here: <b>${airport.countryName}, ${airport.airportName}</b>`)
                    .openPopup();
                document.querySelector('#country').innerHTML = `Kysymys at ${airport.countryName}`;
                mainGame([airport.latitude_deg, airport.longitude_deg], airport.airportName);

                });
            }
        } catch (error) {
        console.log(error);
    }
    gameQuestion();
    document.querySelector('#kysymysbox').classList.remove('hide');
}

async function gameQuestion() {
    const questionData = await getData('http://127.0.0.1:3000/questions/');
    document.getElementById('question'). innerHTML = questionData.question;
    coranswer = questionData.correct_answer;
}

function correct_check(correct_answer) {
  for (let x of document.getElementsByName('options')) {
    if (x.checked) {
      if (x.value === correct_answer) {
        // SweetAlert 2 for correct answer
        Swal.fire({
          icon: 'success',
          title: 'Oikein!',
          text: 'Saat leiman.',
          confirmButtonText: 'OK'
        }).then(() => {
          document.querySelector('#kysymysbox').classList.add('hide');
          leimat++;
          updateStatus();
          checkLeimat();
        });
      } else {
        // SweetAlert 2 for incorrect answer
        Swal.fire({
          icon: 'error',
          title: 'Väärin!',
          text: 'Mene seuraavaan maahan ja vastaa uuteen kysymykseen.',
          confirmButtonText: 'OK'
        }).then(() => {
          document.querySelector('#kysymysbox').classList.add('hide');
        });
      }
    }
  }
}


/*
function correct_check(correct_answer) {
  for (let x of document.getElementsByName('options')) {
    if (x.checked) {
      if (x.value === correct_answer) {
        alert('Oikein! Saat leiman.');
        document.querySelector('#kysymysbox').classList.add('hide');
        leimat++
        updateStatus();
      } else {
        alert('Väärin! Mene seuraavaan maahan ja vastaa uuteen kysymykseen.')
        document.querySelector('#kysymysbox').classList.add('hide');
      }
    }
  }
}

 */

document.getElementById('submit').addEventListener('click', async function (event) {
  event.preventDefault()
  correct_check(coranswer);
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

helsinkiVantaa();
updateStatus();
gameQuestion();
correct_check();