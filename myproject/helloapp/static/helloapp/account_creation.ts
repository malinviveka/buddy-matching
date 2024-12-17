const accountCreationForm = document.getElementById("accountCreationForm") as HTMLFormElement;
const submitAccountButton = document.getElementById("submitAccountButton") as HTMLButtonElement;
const messageDiv = document.getElementById("message") as HTMLDivElement;


submitAccountButton.addEventListener("click", async (event) => {
    event.preventDefault(); //prevents re-loading page to trigger submission

    const formData = new FormData(accountCreationForm); //index.html <form id="accountCreationForm" ...>

    const csrfToken = (document.querySelector("[name=csrfmiddlewaretoken]") as HTMLInputElement).value;

    try {
        const response = await fetch(accountCreationForm.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
            },
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            messageDiv.innerText = result.message;
            messageDiv.style.color = "green";
            accountCreationForm.reset();
        } else {
            const errors = await response.json();
            messageDiv.innerText = `Errors: ${JSON.stringify(errors.errors)}`;
            messageDiv.style.color = "red";
        }
    } catch (error) {
        messageDiv.innerText = "An error occurred while creating the account.";
        messageDiv.style.color = "red";
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const roleSelect = document.querySelector("#id_role") as HTMLSelectElement;
    const specialFields = document.querySelectorAll("[data-role-field]");

    if (!roleSelect) {
        console.error("Dropdown mit ID 'id_role' nicht gefunden.");
        return;
    }

    const updateSpecialFields = () => {
        const selectedRole = roleSelect.value;
        
        specialFields.forEach(field => {
            const roleField = field.getAttribute("data-role-field");
            if (roleField === selectedRole) {
                (field as HTMLElement).style.display = "block";
                console.log(`Showing field for role: ${roleField}`); // Debugging
            } else {
                (field as HTMLElement).style.display = "none";
                console.log(`Hiding field for role: ${roleField}`); // Debugging
            }
        });

    }; 
    

    roleSelect.addEventListener("change", updateSpecialFields);
    updateSpecialFields(); // Initial visibility setup
    
});