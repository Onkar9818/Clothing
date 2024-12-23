const frmRegister = document.querySelector("#frmRegister");
const password = document.querySelector("#password");
const confirmPassword = document.querySelector("#confirm-password");

if (frmRegister && password && confirmPassword) {
  frmRegister.addEventListener("submit", (e) => {
    e.preventDefault();
    if (password.value === confirmPassword.value) {
      const data = new FormData(e.target);
      const inputs = e.target.querySelectorAll("input, button");
      disableFields(inputs, true);
      fetch("/register", { method: "POST", body: data })
        .then((response) => {
          if (!response.ok) throw new Error(response.statusText);
          response.json().then((result) => {
            showAlert(
              result.status ? "Success" : "Error!",
              result.message,
              result.status ? "success" : "error",
              "OK",
              result.status ? "success" : "danger",
              result.status ? reloadPage : null
            );
          });
        })
        .finally(() => disableFields(inputs, false));
    } else {
      showAlert("Error!", "Passwords do not match", "error", "OK", "danger");
    }
  });
}
