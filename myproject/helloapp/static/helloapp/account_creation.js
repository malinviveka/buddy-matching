var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const accountCreationForm = document.getElementById("accountCreationForm");
const submitAccountButton = document.getElementById("submitAccountButton");
const messageDiv = document.getElementById("message");
submitAccountButton.addEventListener("click", (event) => __awaiter(this, void 0, void 0, function* () {
    event.preventDefault(); //prevents re-loading page to trigger submission
    const formData = new FormData(accountCreationForm); //index.html <form id="accountCreationForm" ...>
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    try {
        const response = yield fetch(accountCreationForm.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
            },
            body: formData,
        });
        if (response.ok) {
            const result = yield response.json();
            messageDiv.innerText = result.message;
            messageDiv.style.color = "green";
            accountCreationForm.reset();
            // todo: redirect to home page (see views.py todo)
        }
        else {
            const errors = yield response.json();
            messageDiv.innerText = `Errors: ${JSON.stringify(errors.errors)}`;
            messageDiv.style.color = "red";
        }
    }
    catch (error) {
        messageDiv.innerText = "An error occurred while creating the account: " + error;
        messageDiv.style.color = "red";
    }
}));
document.addEventListener("DOMContentLoaded", () => {
    const roleSelect = document.querySelector("#id_role");
    const specialFields = document.querySelectorAll("[data-role-field]");
    if (!roleSelect) {
        console.error("Dropdown mit ID 'id_role' nicht gefunden.");
        return;
    }
    const updateSpecialFields = () => {
        var _a;
        const selectedRole = roleSelect.value;
        specialFields.forEach(field => {
            const roleField = field.getAttribute("data-role-field");
            const parent = field.parentElement;
            if (roleField === selectedRole) {
                parent.style.display = "block";
                console.log(`Showing field for role: ${roleField}`); // Debugging
            }
            else {
                parent.style.display = "none";
                console.log(`Hiding field for role: ${roleField}`); // Debugging
            }
        });
        const countryField = document.getElementById("id_country");
        const countryLabel = (_a = countryField === null || countryField === void 0 ? void 0 : countryField.parentElement) === null || _a === void 0 ? void 0 : _a.querySelector("label");
        if (selectedRole === "Buddy") {
            countryLabel.innerText = "Preferred Country";
            countryField.placeholder = "Enter preferred country";
        }
        else if (selectedRole === "International Student") {
            countryLabel.innerText = "Country of Sending University";
            countryField.placeholder = "Enter country of sending university";
        }
    };
    roleSelect.addEventListener("change", updateSpecialFields);
    updateSpecialFields(); // Initial visibility setup
});
