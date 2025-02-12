document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const emailInput = document.querySelector<HTMLInputElement>('#id_email');
    const passwordInput = document.querySelector<HTMLInputElement>('#id_password');

    form?.addEventListener('submit', (event) => {
        if (!emailInput?.value || !passwordInput?.value) {
            alert('Please fill in both fields.');
            event.preventDefault();
        }
    });
});