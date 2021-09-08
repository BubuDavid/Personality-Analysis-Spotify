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
