
window.onload = function() {
  // Global root styles
  let styles = getComputedStyle(document.documentElement);

  // saturation input change
  const greysat = document.getElementById('greysat-inp');
  greysat.addEventListener("input", function(event) {
      document.documentElement.style.setProperty('--greysat', event.target.value + '%');
    }
  )

  // invert colors on click to input
  document.querySelector('#invert-btn').addEventListener('click', function(event) {
    let invert = styles.getPropertyValue('--invert');
    document.documentElement.style.setProperty('--invert', 1-invert);
  })

  // tint input change
  const strongtint = document.getElementById('strongtint-inp');
  strongtint.addEventListener("input", function(event) {
      document.documentElement.style.setProperty('--strongtint', event.target.value + '%');
  })

  const weaktint = document.getElementById('weaktint-inp');
  weaktint.addEventListener("input", function(event) {
      document.documentElement.style.setProperty('--weaktint', event.target.value + '%');
  })
}
