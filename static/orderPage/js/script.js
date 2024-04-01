let searchForm = document.querySelector(".search-form");
let shoppingCart = document.querySelector(".shopping-cart");
let navbar = document.querySelector(".navbar");
let cart = document.getElementById("cart");
let addToCart = document.getElementById("addToCart");
let del = document.getElementsByClassName("fa fa-trash");
let total = document.getElementById("total");

var totalCost = 0;

document.querySelector("#search-btn").onclick = () => {
  searchForm.classList.toggle("active");
  shoppingCart.classList.remove("active");
  navbar.classList.remove("active");
};

document.querySelector("#cart-btn").onclick = () => {
  shoppingCart.classList.toggle("active");
  searchForm.classList.remove("active");
  navbar.classList.remove("active");
};

document.querySelector("#menu-btn").onclick = () => {
  navbar.classList.toggle("active");
  searchForm.classList.remove("active");
  shoppingCart.classList.remove("active");
};

window.onscroll = () => {
  searchForm.classList.remove("active");
  shoppingCart.classList.remove("active");
  navbar.classList.remove("active");
};

var swiper = new Swiper(".product-slider", {
  loop: true,
  spaceBetween: 20,
  autoplay: {
    delay: 1800,
    disableOnInteraction: false,
  },

  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1020: {
      slidesPerView: 3,
    },
  },
});

document.getElementById("cart").addEventListener("click", function (event) {
  // Check if the clicked element is the "fa fa-trash" icon
  if (event.target.classList.contains("fa-trash")) {
    // Remove the parent box element of the clicked trash icon
    let productDetails = getProductDetails(event.target.closest(".box"));
    let existingProduct = cart.querySelector(
      `.box[data-name="${productDetails.name}"]`
    );
    let quantityElement = existingProduct.querySelector(".quantity-value");
    let currentQuantity = parseInt(quantityElement.textContent);
    totalCost -=
      parseFloat(productDetails.price.substring(1, 5)) * currentQuantity;
    if (totalCost >= 0) {
      total.textContent = "Total: $" + totalCost.toFixed(2);
    } else {
      total.textContent = "Total: $0";
    }

    event.target.closest(".box").remove();
  }
});

document.addEventListener("click", function (event) {
  // Check if the clicked element is a button with the class "btn" and has an ancestor with the class "products"
  if (
    event.target.classList.contains("btn") &&
    event.target.closest(".products")
  ) {
    // Check if the clicked button is an "Add to Cart" button
    if (event.target.textContent === "Add to Cart") {
      // Get the details of the product
      let productDetails = getProductDetails(event.target.closest(".box"));
      // Check if the product is already in the cart
      let existingProduct = cart.querySelector(
        `.box[data-name="${productDetails.name}"]`
      );
      if (existingProduct) {
        // Update the quantity of the existing product
        let quantityElement = existingProduct.querySelector(".quantity-value");
        let currentQuantity = parseInt(quantityElement.textContent);

        // Update the quantity value
        quantityElement.textContent = currentQuantity + 1; // Update the quantity directly
      } else {
        // Add the product to the cart
        cart.insertAdjacentHTML(
          "afterbegin",
          `
          <div class="box" data-name="${productDetails.name}">
            <i class="fa fa-trash"></i>
            <img src="${productDetails.image}" />
            <div class="content">
              <h1>${productDetails.name}</h1>
              <span class="price">${productDetails.price}</span>
              <div class="quantity">
                <button class="quantity-btn" data-action="decrease">-</button>
                <span class="quantity-value">1</span>
                <button class="quantity-btn" data-action="increase">+</button>
              </div>
            </div>
          </div>
        `
        );
      }
      totalCost += parseFloat(productDetails.price.substring(1, 5));
      total.textContent = "Total: $" + totalCost.toFixed(2);
    }
  }
});

document.addEventListener("click", function (event) {
  if (event.target.classList.contains("quantity-btn")) {
    // Get the parent box of the clicked button
    let boxElement = event.target.closest(".box");
    // Find the quantity value span element within the box
    let quantityElement = boxElement.querySelector(".quantity-value");
    // Check if quantityElement is not null or undefined
    if (quantityElement) {
      // Get the action (increase or decrease) from the data-action attribute of the button
      let action = event.target.getAttribute("data-action");
      // Get the current quantity value
      let currentQuantity = parseInt(quantityElement.textContent);
      let productDetails = getProductDetails(event.target.closest(".box"));
      // Update the quantity based on the action
      if (action === "increase") {
        totalCost += parseFloat(productDetails.price.substring(1, 5));
        total.textContent = "Total: $" + totalCost.toFixed(2);
        quantityElement.textContent = currentQuantity + 1;
      } else if (action === "decrease" && currentQuantity > 1) {
        quantityElement.textContent = currentQuantity - 1;
        totalCost -= parseFloat(productDetails.price.substring(1, 5));
        total.textContent = "Total: $" + totalCost.toFixed(2);
      }
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const checkoutButton = document.querySelector(".btn-checkout");

  checkoutButton.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default button behavior

    const username = document.getElementById("username").value; // Get the username
    const products = []; // Array to store the order details

    // Iterate over each product in the shopping cart
    document
      .querySelector(".shopping-cart")
      .querySelectorAll(".box")
      .forEach(function (productElement) {
        productElement = productElement.querySelector(".content");
        const name = productElement.querySelector("h1").textContent; // Get the product name

        // Check if the .quantity-value element exists inside the productElement
        const quantityElement = productElement.querySelector(".quantity-value");
        const quantity = quantityElement
          ? parseInt(quantityElement.textContent)
          : 0; // Get the product quantity, or 0 if not found

        const price = parseFloat(
          productElement.querySelector(".price").textContent.substring(1, 5) *
            quantity
        ).toFixed(2); // Get the product price

        // Push the product details to the products array
        products.push({ name, price, quantity });
      });

    // Create an object containing the order details
    const orderDetails = {
      username: username,
      products: products,
    };

    if (products.length > 0) {
      // Send the order details to the Flask server using an AJAX request
      fetch("/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(orderDetails),
      })
        .then((response) => {
          if (response.ok) {
            // If the response indicates success, redirect the user to the payment page
            window.location.href = "/payment";
          } else {
            // If the response indicates an error, display an error message
            displayErrorMessage(
              "Error processing order. Please try again.",
              1500
            );
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else {
      displayErrorMessage("Please choose any item", 1500);
    }
    shoppingCart.classList.remove("active");
  });
});

function getProductDetails(boxElement) {
  // Retrieve the product details from the box element
  let productName = boxElement.querySelector("h1").textContent;
  let productPrice = boxElement.querySelector(".price").textContent;
  let productImage = boxElement.querySelector("img").src;
  return { name: productName, price: productPrice, image: productImage };
}

// Function to display an error message for a specified duration
function displayErrorMessage(message, duration) {
  const errorMessage = document.createElement("div");
  errorMessage.textContent = message;

  errorMessage.style.background = "#eee";
  errorMessage.style.padding = "50px"; // Padding around the text
  errorMessage.style.position = "fixed"; // Fixed position so it stays in place even when scrolling
  errorMessage.style.top = "50%"; // Distance from the top of the viewport
  errorMessage.style.left = "50%"; // Center horizontally
  errorMessage.style.transform = "translateX(-50%)"; // Center horizontally
  errorMessage.style.zIndex = "9999"; // Ensure it's on top of other elements
  errorMessage.style.display = "block"; // Display as a block element
  errorMessage.style.borderRadius = "10px"; // Rounded corners
  errorMessage.style.border = "2px solid black"; // Black border
  errorMessage.style.width = "fit-content"; // Adjust width to fit content
  errorMessage.style.fontSize = "24px";

  // Append the error message to the document body
  document.body.appendChild(errorMessage);

  // Hide the error message after the specified duration
  setTimeout(function () {
    errorMessage.style.display = "none";
  }, duration);
}
