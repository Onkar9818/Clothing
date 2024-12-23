const frmLogin = document.querySelector("#frmLogin");
if (frmLogin) {
  frmLogin.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    const inputs = e.target.querySelectorAll("input, button");
    disableFields(inputs, true);
    fetch("/login", { method: "POST", body: data })
      .then((response) => {
        if (!response.ok) throw new Error(response.statusText);
        response.json().then((result) => {
          if (result.status) {
            reloadPage();
          } else {
            showAlert("Error!", result.message, "error", "OK", "danger");
          }
        });
      })
      .finally(() => disableFields(inputs, false));
  });
}
