function switchDisplay(el) {
    el.innerHTML = el.innerHTML == "Dark Mode" ? "Light Mode" : "Dark Mode";
    s = document.getElementById("stylesheet");
    if (s.getAttribute("class") == "page") {
        s.href = s.href.includes("fiddletools.css") ? "../fiddletools_dark.css" : "../fiddletools.css";
    } else {
        s.href = s.href.includes("fiddletools.css") ? "fiddletools_dark.css" : "fiddletools.css";
    }
    
}