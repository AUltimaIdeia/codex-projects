const form = document.querySelector(".submission-form");
const note = document.querySelector(".form-note");

for (const input of document.querySelectorAll(".submission-form input")) {
  const label = input.closest("label")?.querySelector("span")?.textContent || "";
  input.placeholder = label;
}

form?.addEventListener("submit", (event) => {
  event.preventDefault();
  note.textContent = "Ideia recebida. Agora ela será lida com critério.";
  form.reset();
});
