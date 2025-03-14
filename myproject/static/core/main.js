// helloapp/static/helloapp/main.ts
var __awaiter =
  (this && this.__awaiter) ||
  function (thisArg, _arguments, P, generator) {
    function adopt(value) {
      return value instanceof P
        ? value
        : new P(function (resolve) {
            resolve(value);
          });
    }
    return new (P || (P = Promise))(function (resolve, reject) {
      function fulfilled(value) {
        try {
          step(generator.next(value));
        } catch (e) {
          reject(e);
        }
      }
      function rejected(value) {
        try {
          step(generator["throw"](value));
        } catch (e) {
          reject(e);
        }
      }
      function step(result) {
        result.done
          ? resolve(result.value)
          : adopt(result.value).then(fulfilled, rejected);
      }
      step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
  };
const retrieveButton = document.getElementById("retrieveButton");
const entriesDisplay = document.getElementById("entriesDisplay");
retrieveButton.addEventListener("click", (event) =>
  __awaiter(this, void 0, void 0, function* () {
    event.preventDefault();
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
      } else {
        console.error("Error retrieving entries");
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  }),
);
