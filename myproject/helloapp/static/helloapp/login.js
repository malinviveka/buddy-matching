document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const firstNameInput = document.querySelector('#id_first_name');
    const surnameInput = document.querySelector('#id_surname');
    form === null || form === void 0 ? void 0 : form.addEventListener('submit', (event) => {
        if (!(firstNameInput === null || firstNameInput === void 0 ? void 0 : firstNameInput.value) || !(surnameInput === null || surnameInput === void 0 ? void 0 : surnameInput.value)) {
            alert('Please fill in both fields.');
            event.preventDefault();
        }
    });
});
