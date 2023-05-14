$(document).ready(function () {
    const alert = document.getElementById("alert-timer")
    if (!alert) return;
    const timer = alert.dataset.timer

    setTimeout(function () {
        setTimeout(function () {
            alert.style.transition = "all 2.5s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-50px)";

            setTimeout(function () {
                alert.remove();
            }, 2500);

        }, timer);

    }, 3000);
});


const items = document.querySelectorAll(".toggle_password");
items.forEach(item => {
        const passwordField = item.querySelector("input");
        const spanField = item.querySelector("span");
        spanField.addEventListener('click', () => {
        const show_eye_icon = item.querySelector(".fa-eye");
        const hide_eye_icon = item.querySelector(".fa-eye-slash");

        if (passwordField.type === "password") {
            passwordField.type = "text";
            show_eye_icon.classList.add("d-none");
            hide_eye_icon.classList.remove("d-none");
        } else {
            passwordField.type = "password";
            hide_eye_icon.classList.add("d-none");
            show_eye_icon.classList.remove("d-none");
        }
    });
});
