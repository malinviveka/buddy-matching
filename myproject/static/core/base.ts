document.addEventListener('DOMContentLoaded', () => {
    const hamburgerToggle = document.getElementById('hamburgerToggle');
    
    if (hamburgerToggle) {
      hamburgerToggle.addEventListener('click', () => {
        document.body.classList.toggle('nav-open');
        console.log('nav-open toggled', document.body.classList);
      });
    }
});