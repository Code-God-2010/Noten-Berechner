document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('checkbox');
  
    checkbox.checked = localStorage.getItem('darkMode') === 'true';
    checkbox.addEventListener('change', function (event) {
        if (event.currentTarget.checked) {
          darkmode();
        } else {
          nodark();
        }
        localStorage.setItem('darkMode', event.currentTarget.checked);
    });
});

//initial loading of the page
if (localStorage.getItem('darkMode') === 'true') {
    darkmode();
} else {
    nodark();
}
//function for checkbox when checkbox is checked to switch to dark mode
function darkmode() {
  var r = document.querySelector(':root');
  r.style.setProperty('--background', '#312F2F');
  r.style.setProperty('--divColor', '#0E7C7B');
  r.style.setProperty('--linkHover', '#91818A');
  r.style.setProperty('--textColor', '#F1F0EA');
}

//function for checkbox when checkbox is not checked
function nodark() {
    var r = document.querySelector(':root');
    r.style.setProperty('--background', '#F1F1F2');
    r.style.setProperty('--divColor', '#A1D6E2');
    r.style.setProperty('--linkHover', '#1995AD');
    r.style.setProperty('--textColor', '#000000');
}