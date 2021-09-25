document.addEventListener("DOMContentLoaded", siteNav);

function siteNav() {

  // Select the menu icon
  const menuIcon = document.querySelector(".js-navBtn");
  const menu = document.querySelector(".js-navMenu");

  menuIcon.classList.remove('is-hidden');
  menu.classList.remove('is-open');

  // For each element, add a listener for the "click" event.
  menuIcon.addEventListener("click", toggleMenu);

  function toggleMenu(e) {
    menu.classList.toggle('is-open');
  };

}
