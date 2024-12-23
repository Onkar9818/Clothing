const removeFromCartButtons = document.querySelectorAll(
  ".btn-remove-from-cart"
);
if (removeFromCartButtons.length) {
  removeFromCartButtons.forEach((button) => {
    button.addEventListener("click", async (e) => {
      e.preventDefault();
      const spec = e.currentTarget.dataset.spec;
      const color = e.currentTarget.dataset.color;
      if (spec && color) {
        const confirm = await showConfirm(
          "Are you sure",
          "Are you sure you want to remove this product from cart?",
          "Yes",
          "danger",
          "No",
          "secondary"
        );
        if (confirm.isConfirmed) {
          const data = new FormData();
          data.append("spec", spec);
          data.append("color", color);
          fetch("/remove-cart-item", { method: "POST", body: data }).then(
            (response) => {
              if (!response.ok) {
                throw new Error(response.statusText);
              }
              response.json().then((result) => {
                Swal.fire({
                  title: result.status ? "Success" : "Error!",
                  text: result.message,
                  icon: result.status ? "success" : "error",
                  confirmButtonText: "OK",
                }).then((res) => {
                  if (result.status) {
                    location.reload();
                  }
                });
              });
            }
          );
        }
      }
    });
  });
}

const quantitySelects = document.querySelectorAll(".form-select");
if (quantitySelects.length) {
  quantitySelects.forEach(function (select) {
    select.addEventListener("change", function (e) {
      const productPrice = select
        .closest(".card")
        .querySelector("#product-price");
      if (
        productPrice &&
        e.target.dataset.spec &&
        e.target.dataset.color &&
        e.target.value
      ) {
        const data = new FormData();
        data.append("spec-id", e.target.dataset.spec);
        data.append("color", e.target.dataset.color);
        data.append("quantity", e.target.value);
        fetch("/get-calc-product-price", { method: "POST", body: data }).then(
          (response) => {
            if (!response.ok) throw new Error(response.statusText);
            response.json().then((result) => {
              if (result.status) {
                productPrice.textContent = result.price;
              } else {
                Swal.fire({
                  title: "Error!",
                  text: result.message,
                  icon: "error",
                  confirmButtonText: "OK",
                }).then(() => {
                  e.target.value = "1";
                  e.target.dispatchEvent(new Event("change"));
                });
              }
            });
          }
        );
      }
    });
  });
}
