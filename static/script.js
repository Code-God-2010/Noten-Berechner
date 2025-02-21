function darkMode(){
    var r = document.querySelector(':root');
    r.style.setProperty('--background', '#240750');
    r.style.setProperty('--divColor', '#344c64');
    r.style.setProperty('--linkHover', '#57a6a1');
    r.style.setProperty('--textColor', '#FFFFFF');
}

function lightMode(){
    var r = document.querySelector(':root');
    r.style.setProperty('--background', '#F1F1F2');
    r.style.setProperty('--divColor', '#A1D6E2');
    r.style.setProperty('--linkHover', '#1995AD');
    r.style.setProperty('--textColor', '#000000');
}