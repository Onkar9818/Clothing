const priceContainer = document.querySelector("#price-container");
const availableStock = document.querySelector("#available-stock");
const ctaButtonsContainer = document.querySelector("#cta-buttons-container");

const redirectToCheckout = () => location.href = "/checkout"

const frmAddToCart = document.querySelector("#frmAddToCart");
if (frmAddToCart) {
  frmAddToCart.addEventListener("submit", (e) => {
    e.preventDefault();
    addProductToCart(e.target, reloadPage)
  });
}

const btnBuyNow = document.querySelector('#btnBuyNow');
if(btnBuyNow && frmAddToCart) {
  btnBuyNow.addEventListener('click', (e) => {
    addProductToCart(frmAddToCart, redirectToCheckout)
  })
}

const addProductToCart = (target, callback) => {
  const data = new FormData(target);
  const inputs = target.querySelectorAll("input, button");
  disableFields(inputs, true);
  fetch("/add-to-cart", { method: "POST", body: data })
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
            result.status ? callback : null
          );
        });
      }
    })
    .finally(() => disableFields(inputs, false));
};

const sizeButtons = document.querySelectorAll(
  '.size-input-radio input[type="radio"]'
);
if (sizeButtons.length) {
  sizeButtons.forEach((button) => {
    button.addEventListener("change", (e) => {
      if (e.target.checked) {
        const data = new FormData();
        data.append("spec-id", e.target.value);
        fetch("/get-product-price", { method: "POST", body: data }).then(
          (response) => {
            if (!response.ok) throw new Error(response.statusText);
            response.json().then((result) => {
              if (result.status) {
                removeAllChildNodes(priceContainer);
                priceContainer.classList.remove("text-muted", "small");
                priceContainer.classList.add("display-6");
                priceContainer.textContent = result.amt;
                if (result.qnt) {
                  ctaButtonsContainer.classList.remove("d-none");
                  availableStock.textContent = `${result.qnt} items left.`;
                  availableStock.classList.remove("text-danger", "fs-5");
                  availableStock.classList.add("text-muted", "small");
                } else {
                  ctaButtonsContainer.classList.add("d-none");
                  availableStock.classList.remove("text-muted", "small");
                  availableStock.classList.add("text-danger", "fs-5");
                  availableStock.textContent = `Currently unavailable`;
                }
              } else {
                priceContainer.classList.remove("display-6");
                priceContainer.classList.add("text-muted", "small");
                priceContainer.textContent = "Select size to view price";
                availableStock.textContent = "";
                if (!ctaButtonsContainer.classList.contains("d-none")) {
                  ctaButtonsContainer.classList.add("d-none");
                }
              }
            });
          }
        );
      }
    });
  });
}
