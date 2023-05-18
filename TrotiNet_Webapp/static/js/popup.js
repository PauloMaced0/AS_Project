function toggle(id) {
    // Toggle the visibility of the element with the given id
    var element = document.getElementById(id);
    if (element.style.display === "none") {
        element.style.display = "block";
    }
    else {
        element.style.display = "none";
    }
}