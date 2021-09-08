const menu = document.querySelector(".menu");
const menuImg = document.querySelector("#menu__image");
const menuItems = document.querySelectorAll(".menu__icons--item");
const menuUserName = document.querySelector(".menu_username");

menuImg.addEventListener("click", () => {
  for (let i = 1; i < menuItems.length; i++) {
    setTimeout(() => {
      menuItems[i].classList.toggle("deactivate");
    }, i * 50);
  }
  menuUserName.classList.toggle("deactivate");
  menu.classList.toggle("deactivate");
  menuImg.classList.toggle("deactivate");
});

for (let i = 1; i < menuItems.length; i++) {
  menuItems[i].classList.toggle("deactivate");
}
menuUserName.classList.toggle("deactivate");
menu.classList.toggle("deactivate");
menuImg.classList.toggle("deactivate");
