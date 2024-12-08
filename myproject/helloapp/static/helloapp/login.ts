document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const firstNameInput = document.querySelector<HTMLInputElement>('#id_first_name');
    const surnameInput = document.querySelector<HTMLInputElement>('#id_surname');

    form?.addEventListener('submit', (event) => {
        if (!firstNameInput?.value || !surnameInput?.value) {
            alert('Please fill in both fields.');
            event.preventDefault();
        }
    });
});