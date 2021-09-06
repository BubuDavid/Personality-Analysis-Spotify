const header = document.querySelector(".header");
const pageUrl = window.location.href;

// Redirect
header.addEventListener("click", () => {
  window.location.replace("/");
});
// Check on scrolling
function checkifScrolling() {
  window.onscroll = () => {
    let distanceScrolled = document.documentElement.scrollTop;
    if (distanceScrolled >= 50) {
      header.classList.add("scrolling");
    } else {
      header.classList.remove("scrolling");
    }
  };
}
checkifScrolling();

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

// The json read and treatment.
if (pageUrl.includes("/test")) {
  readTextFile("./static/scripts/songs.json", function (text) {
    let songs = JSON.parse(text);
    console.log(songs);

    const songsContainer = document.querySelector(".random-songs__container");
  });
} else {
  console.log("hola");
}
