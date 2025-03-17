document.addEventListener("DOMContentLoaded", () => {
  function toggleDetails(selectId, detailsBoxId, triggerValue) {
    const selectElement = document.getElementById(selectId);
    const detailsBox = document.getElementById(detailsBoxId);
    if (selectElement && detailsBox) {
      //Hiding detailsBox
      detailsBox.style.display = "none";
      selectElement.addEventListener("change", () => {
        detailsBox.style.display =
          selectElement.value.toLowerCase() === triggerValue.toLowerCase()
            ? "block"
            : "none";
      });
    }
  }
  //Initialize dynamic fields as hidden
  const q5Details = document.getElementById("q5_details_box");
  if (q5Details && q5Details.parentElement) {
    q5Details.style.display = "none";
  }
  const q8Details = document.getElementById("q8_details_box");
  if (q8Details && q8Details.parentElement) {
    q8Details.style.display = "none";
  }
  const q9Details = document.getElementById("q9_details_box");
  if (q9Details && q9Details.parentElement) {
    q9Details.style.display = "none";
  }
  //Setup event listeners for dynamic fields
  toggleDetails("id_q5", "q5_details_box", "No");
  toggleDetails("id_q8", "q8_details_box", "Yes/Sometimes");
  toggleDetails("id_q9", "q9_details_box", "No/Maybe");

  //Function showing the modal with message
  function showModal(message) {
    const modalOverlay = document.createElement("div");
    modalOverlay.classList.add("modal-overlay");

    const modalContent = document.createElement("div");
    modalContent.classList.add("modal-content");
    modalContent.innerHTML = `<p>${message}</p><button id="closeModal">Close</button>`;

    modalOverlay.appendChild(modalContent);
    document.body.appendChild(modalOverlay);

    //Show modal
    modalOverlay.style.display = "flex";

    //Closing modal
    document.getElementById("closeModal").addEventListener("click", () => {
      modalOverlay.style.display = "none";
      document.getElementById("content-container").classList.remove("blur");
      modalOverlay.remove();
    });
  }

  //Form submission handler
  const feedbackForm = document.getElementById("FeedbackForm");
  feedbackForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(feedbackForm);

    fetch(feedbackForm.action, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        //Showing popup field, depending on answer
        if (data.message) {
          showModal(data.message);
        } else if (data.errors) {
          showModal(
            "Es gab ein Problem mit dem Feedback: " +
              JSON.stringify(data.errors),
          );
        }
      })
      .catch((error) => {
        showModal("Ein Fehler ist aufgetreten: " + error);
      });

    //Adding blurr effect on container
    document.getElementById("content-container").classList.add("blur");
  });
});
