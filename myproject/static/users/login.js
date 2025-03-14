document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const emailInput = document.querySelector("#id_email");
  const passwordInput = document.querySelector("#id_password");
  form === null || form === void 0
    ? void 0
    : form.addEventListener("submit", (event) => {
        if (
          !(emailInput === null || emailInput === void 0
            ? void 0
            : emailInput.value) ||
          !(passwordInput === null || passwordInput === void 0
            ? void 0
            : passwordInput.value)
        ) {
          alert("Please fill in both fields.");
          event.preventDefault();
        }
      });
});
