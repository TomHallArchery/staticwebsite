document.addEventListener("DOMContentLoaded", handler);

function handler() {
  console.log('Page loaded, site_nav priming')

  // Select the menu icon
  const menuIcon = document.querySelector("nav .hamburger");
  const menu = document.querySelector(".site_nav ul");

  menuIcon.classList.remove('hidden');
  menu.classList.remove('open');

  // For each element, add a listener for the "click" event.
  menuIcon.addEventListener("click", function(e) {
    menu.classList.toggle('open');
  });

  console.log('site_nav ready')

}
