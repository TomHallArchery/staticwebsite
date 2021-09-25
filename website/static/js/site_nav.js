document.addEventListener("DOMContentLoaded", siteNav);

function siteNav() {

  // Select the menu icon
  const menuIcon = document.querySelector(".site_nav--btn");
  const menu = document.querySelector(".site_nav--menu");

  menuIcon.classList.remove('hidden');
  menu.classList.remove('open');

  // For each element, add a listener for the "click" event.
  menuIcon.addEventListener("click", toggleMenu);

  function toggleMenu(e) {
    menu.classList.toggle('open');
  };

}
