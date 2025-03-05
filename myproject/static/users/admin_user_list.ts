document.addEventListener("DOMContentLoaded", () => {
  // Select all buttons with the class 'toggle-permission'
  const buttons =
    document.querySelectorAll<HTMLButtonElement>(".toggle-permission");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const userId = button.dataset.userId;
      if (!userId) {
        console.error("User ID is not defined on the button.");
        return;
      }

      // CSRF token value from the hidden input field
      const csrfToken =
        document.querySelector<HTMLInputElement>(
          'input[name="csrfmiddlewaretoken"]',
        )?.value || "";

      // Fetch API call to toggle permission
      fetch(`/cadmin/users/toggle_permission/${userId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          const row = document.querySelector(`#user-${userId}`);
          if (!row) {
            console.error(`Row for user ID ${userId} not found.`);
            return;
          }

          const statusCell = row.querySelector(".status");
          if (statusCell) {
            statusCell.textContent = data.is_permitted
              ? "Zugelassen"
              : "Nicht zugelassen";
          }

          // Update button text
          button.textContent = data.is_permitted ? "Entziehen" : "Zulassen";
        })
        .catch((error) => {
          console.error("Error while toggling permission:", error);
          alert("Fehler beim Aktualisieren des Status");
        });
    });
  });
});
