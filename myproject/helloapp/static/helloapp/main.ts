// helloapp/static/helloapp/main.ts

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