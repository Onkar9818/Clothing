const orderButtons = document.querySelectorAll(".btn-check");
const frmPlaceOrder = document.querySelector("#frmPlaceOrder");
const paymentMethods = document.querySelectorAll('[name="payment_method"]');
if (orderButtons.length && paymentMethods.length && frmPlaceOrder) {
  orderButtons.forEach((button) => {
    button.addEventListener("change", (e) => {
      if (e.target.checked) {
        if (Array.from(paymentMethods).some((method) => method.checked)) {
          frmPlaceOrder.submit();
        } else {
          e.target.checked = false;
          showAlert(
            "Error!",
            "Please select payment method",
            "error",
            "OK",
            "danger"
          );
        }
      }
    });
  });
}
