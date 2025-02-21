document.addEventListener('DOMContentLoaded', function () {
    var hamburgerToggle = document.getElementById('hamburgerToggle');
    if (hamburgerToggle) {
        hamburgerToggle.addEventListener('click', function () {
            document.body.classList.toggle('nav-open');
            console.log('nav-open toggled', document.body.classList);
        });
    }
});