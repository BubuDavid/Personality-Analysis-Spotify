// This function checks the status of the songs.json
// Returns the json content on string format
// And on the callback function below, you code what you want
// to do with that.
function readTextFile(file, callback) {
  let rawFile = new XMLHttpRequest();
  rawFile.overrideMimeType("application/json");
  rawFile.open("GET", file, true);
  rawFile.onreadystatechange = function () {
    if (rawFile.readyState === 4 && rawFile.status == "200") {
      callback(rawFile.responseText);
    }
  };
  rawFile.send(null);
}

//  This function creates card components from a random song list
// and returns a list of that songs into a string.
function createComponents(nSongs, randomSongs) {
  let tweet_songs = "";
  const songsContainer = document.querySelector(".random-songs__container");
  for (song of randomSongs) {
    songsContainer.innerHTML += `<div class='random-song__item'>
        <button class='btn btn--red btn--small'><i class="btn-shuffle fas fa-random"></i></button>
          <img src='${song[0]["image"]}' alt='Album image' />
          <h1>${song[0]["name"]}</h1>
          <p>|${song[0]["artists"].join(" | ")}|</p>
        </div>`;
    // Save songs name
    tweet_songs += `* ${song[0]["name"]}\n`;
  }
  return tweet_songs;
}
// Returns a list of randomly chosen songs
function chooseRandomSongs(nSongs, songs) {
  let randomSongs = [];
  for (let i = 0; i < nSongs; i++) {
    randomSongs.push(songs.splice((Math.random() * songs.length) | 0, 1));
  }
  return randomSongs;
}

function checkAndUpdateCounter(tweet) {
  const tweetContainer = document.querySelector(".tweet__container");
  const letterCounter = document.querySelector("#tweet__word-counter");

  letterCounter.innerHTML = `${tweet.length}/280`;
  if (tweet.length > 280) {
    tweetContainer.classList.add("forbidden");
  } else {
    tweetContainer.classList.remove("forbidden");
  }
}

// Define songs list
let songsData;

// The json read, treatment and display
if (pageUrl.includes("/tweet-view")) {
  readTextFile("./static/scripts/songs.json", function (text) {
    songsData = JSON.parse(text);
    // Define all the variables and const to be defined
    let nSongs = 5;
    const tweetArea = document.querySelector("#tweet-review");
    // Create a smaller list with random songs
    let randomSongs = chooseRandomSongs(nSongs, songsData);
    // Create components with this random songs
    let tweet_songs = createComponents(nSongs, randomSongs);
    // Creates the tweets body
    let startOfTweet =
      "Soy un BubuBot hecho con #Python 🐍 y #SpotifyAPI 🎶. Algunas recomendaciones:\n";
    let endOfTweet =
      "Primera persona en decir todos los artistas bien, Bubu le da un beso/sticker 🤓.";
    // Display the tweet in the textarea
    tweetArea.value = startOfTweet + tweet_songs + endOfTweet;
    // Count the words inside the textarea
    checkAndUpdateCounter(tweetArea.value);
    // Update the counter with an event listener over the textarea
    tweetArea.addEventListener("input", () => {
      // Update the word count variable
      startOfTweet = tweetArea.value;
      checkAndUpdateCounter(startOfTweet);
    });
  });
}

// Switch songs method
const closeBtn = document
  .querySelectorAll(".btn-shuffle")
  .forEach((shuffleBtn) => {
    shuffleBtn.addEventListener("click", () => {});
  });
