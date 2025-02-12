// helloapp/static/helloapp/main.ts

const retrieveButton = document.getElementById("retrieveButton") as HTMLButtonElement;
const entriesDisplay = document.getElementById("entriesDisplay") as HTMLUListElement;

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
