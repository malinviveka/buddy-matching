// helloapp/static/helloapp/main.ts

document.addEventListener("DOMContentLoaded", () => {
    const entryInput = document.getElementById("entryInput") as HTMLInputElement;
    const saveButton = document.getElementById("saveButton") as HTMLButtonElement;
    const retrieveButton = document.getElementById("retrieveButton") as HTMLButtonElement;
    const entriesDisplay = document.getElementById("entriesDisplay") as HTMLUListElement;

    // Save entry to the database
    saveButton.addEventListener("click", async () => {
        const text = entryInput.value;
        if (text) {
            try {
                const response = await fetch("/api/save_entry/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ text: text }),
                });
                const data = await response.json();
                alert(data.message);  // Display confirmation message
                entryInput.value = "";  // Clear the input field
            } catch (error) {
                console.error("Error saving entry:", error);
            }
        }
    });

    // Retrieve all entries from the database
    retrieveButton.addEventListener("click", async () => {
        try {
            const response = await fetch("/api/get_entries/");
            if (response.ok) {
                const data = await response.json();
                entriesDisplay.innerHTML = "";  // Clear existing entries
                data.entries.forEach((entry: { id: number, text: string }) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = entry.text;
                    entriesDisplay.appendChild(listItem);
                });
            } else {
                console.error("Error retrieving entries");
            }
        } catch (error) {
            console.error("Network error:", error);
        }
    });
});

