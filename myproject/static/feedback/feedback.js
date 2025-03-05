document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("FeedbackForm");
  const rating1Input = document.getElementById("id_rating_1");
  const rating2Input = document.getElementById("id_rating_2");
  const textFeedbackInput = document.getElementById("id_text_feedback");
  const feedbackButton = document.getElementById("feedbackButton");

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!validateForm()) {
      return;
    }

    const formData = new FormData(form);

    fetch(form.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"), // CSRF-Token setzen
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          alert("Your feedback has been successfully submitted!");
          form.reset();
        } else {
          alert("Error submitting feedback: " + JSON.stringify(data.errors));
        }
      })
      .catch((error) => console.error("Error:", error));
  });

  function validateForm() {
    if (rating1Input.value.trim() === "" || rating2Input.value.trim() === "") {
      alert("Please answer all rating questions.");
      return false;
    }
    return true;
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      document.cookie.split(";").forEach((cookie) => {
        let trimmedCookie = cookie.trim();
        if (trimmedCookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(trimmedCookie.split("=")[1]);
        }
      });
    }
    return cookieValue;
  }
});
