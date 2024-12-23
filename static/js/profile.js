const frmAddAddress = document.querySelector("#frmAddAddress");
if (frmAddAddress) {
  frmAddAddress.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    const inputs = e.target.querySelectorAll("input, button");
    disableFields(inputs, true);
    fetch("/add-address", { method: "POST", body: data })
      .then((response) => {
        if (response.status === 401) location.replace("/login");
        if (!response.ok && response.status !== 401)
          throw new Error(response.statusText);
        if (response.ok && response.status === 200) {
          response.json().then((result) => {
            showAlert(
              result.status ? "Success" : "Error!",
              result.message,
              result.status ? "success" : "error",
              "OK",
              result.status ? "success" : "danger",
              reloadPage
            );
          });
        }
      })
      .finally(() => disableFields(inputs, false));
  });
}
