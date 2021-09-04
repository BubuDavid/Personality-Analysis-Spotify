const header = document.querySelector(".header");
const profile_img = document.getElementById("profile_image");
const page_url = window.location.href;

// Redirect
header.addEventListener("click", () => {
  window.location.replace("/");
});
// Make the profile image to go away
if (page_url.includes("songs-page")) {
  setInterval(() => {
    profile_img.classList.add("hidden");
  }, 500);
}

// Activate or deactivate the btns
if (page_url.includes("songs-page/top")) {
  checkifScrolling();
  if (page_url.includes("short_term")) {
    const activateBtn = document.getElementById("short_term");
    activateBtn.classList.add("active");
  }
  if (page_url.includes("medium_term")) {
    const activateBtn = document.getElementById("medium_term");
    activateBtn.classList.add("active");
  }
  if (page_url.includes("long_term")) {
    const activateBtn = document.getElementById("long_term");
    activateBtn.classList.add("active");
  }
}
// Disapear btns when you are on recent music
if (page_url.includes("songs-page/recent/")) {
  checkifScrolling();
  const categories = document.querySelector(".categories");
  categories.style.opacity = "0";
  categories.style.pointerEvents = "none";
}

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
