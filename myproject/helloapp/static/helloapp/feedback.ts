document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("FeedbackForm") as HTMLFormElement;
    const rating1Input = document.getElementById("id_rating_1") as HTMLInputElement;
    const rating2Input = document.getElementById("id_rating_2") as HTMLInputElement;
    const textFeedbackInput = document.getElementById("id_text_feedback") as HTMLTextAreaElement;
    const feedbackButton = document.getElementById("feedbackButton") as HTMLButtonElement;
  
    form.addEventListener("submit", (event) => {
      event.preventDefault();
  
      if (!validateForm()) {
        return;
      }
  
      console.log("Feedback submitted:", {
        rating_1: rating1Input.value,
        rating_2: rating2Input.value,
        text_feedback: textFeedbackInput.value.trim() !== "" ? textFeedbackInput.value : "No comment",
      });
  
      form.reset();
      alert("Your feedback has been successfully submitted!");
    });
  
    function validateForm(): boolean {
      if (rating1Input.value.trim() === "" || rating2Input.value.trim() === "") {
        alert("Please answers all rating questions.");
        return false;
      }
      return true;
    }
  });