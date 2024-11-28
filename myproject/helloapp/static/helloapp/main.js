// helloapp/static/helloapp/main.ts
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
document.addEventListener("DOMContentLoaded", () => {
    const entryInput = document.getElementById("entryInput");
    const saveButton = document.getElementById("saveButton");
    const retrieveButton = document.getElementById("retrieveButton");
    const entriesDisplay = document.getElementById("entriesDisplay");
    // Save entry to the database
    saveButton.addEventListener("click", () => __awaiter(this, void 0, void 0, function* () {
        const text = entryInput.value;
        if (text) {
            try {
                const response = yield fetch("/api/save_entry/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ text: text }),
                });
                const data = yield response.json();
                alert(data.message); // Display confirmation message
                entryInput.value = ""; // Clear the input field
            }
            catch (error) {
                console.error("Error saving entry:", error);
            }
        }
    }));
    // Retrieve all entries from the database
    retrieveButton.addEventListener("click", () => __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch("/api/get_entries/");
            if (response.ok) {
                const data = yield response.json();
                entriesDisplay.innerHTML = ""; // Clear existing entries
                data.entries.forEach((entry) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = entry.surname;
                    entriesDisplay.appendChild(listItem);
                });
            }
            else {
                console.error("Error retrieving entries");
            }
        }
        catch (error) {
            console.error("Network error:", error);
        }
    }));
});
