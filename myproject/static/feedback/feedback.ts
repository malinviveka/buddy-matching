document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("FeedbackForm") as HTMLFormElement;
    const q1Input = document.getElementById("id_q1") as HTMLInputElement;
    const q2Input = document.getElementById("id_q2") as HTMLInputElement;
    const q3Input = document.getElementById("id_q3") as HTMLInputElement;
    const q4Input = document.getElementById("id_q4") as HTMLInputElement;
    const q5Input = document.getElementById("id_q5") as HTMLInputElement;
    const q5_details = document.getElementById("id_q5_details") as HTMLTextAreaElement;
    const q6Input = document.getElementById("id_q6") as HTMLInputElement;
    const q7Input = document.getElementById("id_q7") as HTMLInputElement;
    const q8Input = document.getElementById("id_q8") as HTMLInputElement;
    const q8_details = document.getElementById("id_q8_details") as HTMLTextAreaElement;
    const q9Input = document.getElementById("id_q9") as HTMLInputElement;
    const q9_details = document.getElementById("id_q9_details") as HTMLTextAreaElement;
    const q10Input = document.getElementById("id_q10") as HTMLTextAreaElement;
    const feedbackButton = document.getElementById("feedbackButton") as HTMLButtonElement;
  
    //listener for submit feedback button 
    form.addEventListener("submit", (event) => {
      event.preventDefault();
  
      if (!validateForm()) {
        return;
      }
  
      //submit feedback with the respective values for each question 
      console.log("Feedback submitted:", {
        q1: q1Input.value,
        q2: q2Input.value,
        q3: q3Input.value,
        q4: q4Input.value,
        q5: q5Input.value,
        q5_details: q5_details.value.trim() !== "" ? q5_details.value : "No comment", //if last field is empty, overwrite with "no comment" instead
        q6: q6Input.value,
        q7: q7Input.value,
        q8: q8Input.value,
        q8_details: q8_details.value.trim() !== "" ? q8_details.value : "No comment", //if last field is empty, overwrite with "no comment" instead
        q9: q9Input.value,
        q9_details: q9_details.value.trim() !== "" ? q9_details.value : "No comment", //if last field is empty, overwrite with "no comment" instead
        q10: q10Input.value.trim() !== "" ? q10Input.value : "No comment", //if last field is empty, overwrite with "no comment" instead
      });
  
      form.reset();
      alert("Your feedback has been successfully submitted!");
    });
  
    function validateForm(): boolean {
      if (q1Input.value.trim() === "" || q2Input.value.trim() === "" || q3Input.value.trim() === "" || q4Input.value.trim() === "" || q5Input.value.trim() === "" || q6Input.value.trim() === "" || q7Input.value.trim() === "" || q8Input.value.trim() === "" || q9Input.value.trim() === "") {
        alert("Please answers all rating questions."); //check if all rating questions are answered 
        return false;
      }
      return true;
    }
  });