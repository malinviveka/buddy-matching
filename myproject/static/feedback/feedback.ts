document.addEventListener("DOMContentLoaded", () => {
  
  function toggleDetails(selectId: string, detailsBoxId: string, triggerValue: string) {
    const selectElement = document.getElementById(selectId) as HTMLSelectElement | null;
    const detailsBox = document.getElementById(detailsBoxId) as HTMLDivElement | null;

    if (selectElement && detailsBox) {
        // Verstecke das gesamte umschließende Element
        detailsBox.style.display = "none";

        selectElement.addEventListener("change", () => {
            detailsBox.style.display = selectElement.value.toLowerCase() === triggerValue.toLowerCase() ? "block" : "none";
        });
    }
}

  // Initialisiere die Felder als versteckt auf der Seite
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

  // Setup event listeners für die Auswahlfelder
  toggleDetails("id_q5", "q5_details_box", "no");
  toggleDetails("id_q8", "q8_details_box", "yes");
  toggleDetails("id_q9", "q9_details_box", "no");

});




