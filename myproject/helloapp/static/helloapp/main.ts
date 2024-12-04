// helloapp/static/helloapp/main.ts

const accountCreationForm = document.getElementById("accountCreationForm") as HTMLFormElement;
const submitAccountButton = document.getElementById("submitAccountButton") as HTMLButtonElement;
const retrieveButton = document.getElementById("retrieveButton") as HTMLButtonElement;
const entriesDisplay = document.getElementById("entriesDisplay") as HTMLUListElement;
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

retrieveButton.addEventListener("click", async (event) => {
    event.preventDefault();
    try {
        const response = await fetch("/api/get_entries/");
        if (response.ok) {
            const data = await response.json();
            entriesDisplay.innerHTML = "";  // Clear existing entries
            data.entries.forEach((entry: { firstname: string, surname: string }) => {
                const listItem = document.createElement("li");
                listItem.textContent = entry.surname;
                entriesDisplay.appendChild(listItem);
            });
        } else {
            console.error("Error retrieving entries");
        }
    } catch (error) {
        console.error("Network error:", error);
    }
});