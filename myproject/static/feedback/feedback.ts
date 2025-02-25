/* document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("FeedbackForm") as HTMLFormElement;
  const q1Input = document.getElementById("id_q1") as HTMLInputElement;
  const q2Input = document.getElementById("id_q2") as HTMLInputElement;
  const q3Input = document.getElementById("id_q3") as HTMLInputElement;
  const q4Input = document.getElementById("id_q4") as HTMLInputElement;
  const q5Input = document.getElementById("id_q5") as HTMLInputElement;
  const q5_details = document.getElementById("id_q5_details") as HTMLInputElement;
  const q6Input = document.getElementById("id_q6") as HTMLInputElement;
  const q7Input = document.getElementById("id_q7") as HTMLInputElement;
  const q8Input = document.getElementById("id_q8") as HTMLInputElement;
  const q8_details = document.getElementById("id_q8_details") as HTMLInputElement;
  const q9Input = document.getElementById("id_q9") as HTMLInputElement;
  const q9_details = document.getElementById("id_q9_details") as HTMLInputElement;
  const q10Input = document.getElementById("id_q10") as HTMLInputElement;
  const feedbackButton = document.getElementById("feedbackButton") as HTMLButtonElement;

  const updateDetailsFields = (): void => {
      // Anzeige von q5_details (Falls q5 = "No")
      if (q5Input.value === 'No') {
          q5_details.style.display = "block";
      } else {
          q5_details.style.display = "none";
      }

      // Anzeige von q8_details (Falls q8 = "Yes" oder "Sometimes")
      if (q8Input.value === 'Yes' || q8Input.value === 'Sometimes') {
          q8_details.style.display = "block";
      } else {
          q8_details.style.display = "none";
      }

      // Anzeige von q9_details (Falls q9 = "No")
      if (q9Input.value === 'No') {
          q9_details.style.display = "block";
      } else {
          q9_details.style.display = "none";
      }
  };

  // Listener for changes of q5, q8 and q9
  q5Input.addEventListener("change", updateDetailsFields);
  q8Input.addEventListener("change", updateDetailsFields);
  q9Input.addEventListener("change", updateDetailsFields);

  // Initial Update of Details Fields
  updateDetailsFields();

  // Listener for the submit button
  form.addEventListener("submit", (event: SubmitEvent) => {
      event.preventDefault();

      if (!validateForm()) {
          return;
      }

      // Collect and log feedback data
      console.log("Feedback submitted:", {
          q1: q1Input.value,
          q2: q2Input.value,
          q3: q3Input.value,
          q4: q4Input.value,
          q5: q5Input.value,
          q5_details: q5_details.value.trim() !== "" ? q5_details.value : "No comment",
          q6: q6Input.value,
          q7: q7Input.value,
          q8: q8Input.value,
          q8_details: q8_details.value.trim() !== "" ? q8_details.value : "No comment",
          q9: q9Input.value,
          q9_details: q9_details.value.trim() !== "" ? q9_details.value : "No comment",
          q10: q10Input.value.trim() !== "" ? q10Input.value : "No comment",
      });

      form.reset();
      alert("Your feedback has been successfully submitted!");
  });

  function validateForm(): boolean {
      const requiredFields = ["id_q1", "id_q2", "id_q3", "id_q4", "id_q5", "id_q6", "id_q7", "id_q8", "id_q9"];
      for (const fieldId of requiredFields) {
          const field = document.getElementById(fieldId) as HTMLInputElement;
          if (field.value.trim() === "") {
              alert("Please answer all rating questions.");
              return false;
          }
      }
      return true;
  }
});
*/

document.addEventListener("DOMContentLoaded", () => {
  function toggleDetails(selectId: string, detailsBoxId: string, triggerValue: string) {
      const selectElement = document.getElementById(selectId) as HTMLSelectElement | null;
      const detailsBox = document.getElementById(detailsBoxId) as HTMLDivElement | null;

      if (selectElement && detailsBox) {
          // Ensure the field is hidden initially
          detailsBox.style.display = "none";
          
          selectElement.addEventListener("change", () => {
              detailsBox.style.display = selectElement.value.toLowerCase() === triggerValue.toLowerCase() ? "block" : "none";
          });
      }
  }

  // Initialize fields as hidden on page load
  document.getElementById("q5_details_box")!.style.display = "none";
  document.getElementById("q8_details_box")!.style.display = "none";
  document.getElementById("q9_details_box")!.style.display = "none";

  // Setup event listeners for select fields
  toggleDetails("id_q5", "q5_details_box", "no");  // Falls "No" -> Zusatzfeld
  toggleDetails("id_q8", "q8_details_box", "yes"); // Falls "Yes" -> Zusatzfeld für Probleme
  toggleDetails("id_q9", "q9_details_box", "no");  // Falls "No" -> Zusatzfeld für Empfehlung

  const feedbackForm = document.getElementById("FeedbackForm") as HTMLFormElement | null;
  if (feedbackForm) {
      feedbackForm.addEventListener("submit", (event) => {
          event.preventDefault();
          alert("Feedback submitted successfully!");
          feedbackForm.reset();
      });
  }
});


