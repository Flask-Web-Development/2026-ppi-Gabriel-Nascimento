const button = document.getElementById("dropdown-button");
const menu = document.getElementById("dropdown-menu");

if (button && menu) {

    button.addEventListener("click", function (e) {
        e.stopPropagation();

        if (menu.style.display === "flex") {
            menu.style.display = "none";
        } else {
            menu.style.display = "flex";
        }
    });

    document.addEventListener("click", function () {
        menu.style.display = "none";
    });

}

setTimeout(() => {
    const flash = document.querySelector('.flash');

    if (flash) {
        flash.style.opacity = '0';

        setTimeout(() => {
            flash.remove();
        }, 300);
    }
}, 3000);