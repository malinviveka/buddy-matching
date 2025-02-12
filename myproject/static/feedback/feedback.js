document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("FeedbackForm");
    const rating1Input = document.getElementById("id_rating_1");
    const rating2Input = document.getElementById("id_rating_2");
    const textFeedbackInput = document.getElementById("id_text_feedback");
    const feedbackButton = document.getElementById("feedbackButton");
    //listener for submit feedback button 
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!validateForm()) {
            return;
        }
        //submit feedback with the respective values for each question 
        console.log("Feedback submitted:", {
            rating_1: rating1Input.value,
            rating_2: rating2Input.value,
            text_feedback: textFeedbackInput.value.trim() !== "" ? textFeedbackInput.value : "No comment", //if last field is empty, overwrite with "no comment" instead
        });
        form.reset();
        alert("Your feedback has been successfully submitted!");
    });
    function validateForm() {
        if (rating1Input.value.trim() === "" || rating2Input.value.trim() === "") {
            alert("Please answers all rating questions."); //check if all rating questions are answered 
            return false;
        }
        return true;
    }
});
