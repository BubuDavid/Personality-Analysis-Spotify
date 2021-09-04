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
