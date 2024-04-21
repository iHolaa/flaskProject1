
const addProductForm = document.querySelector('form');

function checkProduct() {
  const Name = document.getElementById('Name').value;
  const Categorie = document.getElementById('Categorie').value;
  const Color = document.getElementById('Color').value;
  const Weight = document.getElementById('Weight').value;
  const Quantity = document.getElementById('Quantity').value;
  const Additional_description = document.getElementById('Additional_description').value;
  const Price = document.getElementById('Price').value;


  if (!Name || !Categorie || !Color || !Weight || !Price || !Quantity) {
    alert('Please fill in all required fields.');
    return;
  }
  if (!/^[a-zA-Z]/.test(Name)) {
    alert('Name must start with a letter.');
    return;
  }
  // Check if first and last names are strings
  if (!/^[a-zA-Z]+$/.test(Color) || !/^[a-zA-Z]+$/.test(Categorie)) {
    alert('Color and Categorie must contain only letters.');
    return;
  }
  // Check if weight is a number
  if (Weight && isNaN(Weight)) {
    alert('Weight must be a number.');
    return;
  }
  // Check if price is a number
  if (isNaN(Price) || isNaN(Quantity)) {
    alert('Price and Quantity must be a number.');
    return;
  }
  if (Quantity > 20 && Quantity <= 0) {
    alert('You can sell maximum of 20 products (Quantity) ! ');
    return;
  }

  alert('Product created successfully!');
  addProductForm.submit();
};

function checkPurchase() {
    const product_id = document.getElementById('product_id').innerText;
    const p_name = document.getElementById('p_name').innerText;
    const p_categorie = document.getElementById('p_categorie').innerText;
    const p_color = document.getElementById('p_color').innerText;
    const p_weight = document.getElementById('p_weight').innerText;
    const p_price = document.getElementById('p_price').innerText;
    const p_seller = document.getElementById('p_seller').innerText;
    const p_quantity = document.getElementById('p_quantity').innerText;
    const Quantity_purchase = document.getElementById('Quantity_purchase').value;

    fetch('/purchase_product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_id: product_id,
          p_name: p_name,
          p_categorie: p_categorie,
          p_color: p_color,
          p_weight: p_weight,
          p_quantity: p_quantity,
          p_price: p_price,
          p_seller: p_seller,
          Quantity_purchase: Quantity_purchase
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message === 'Successful') {
            alert('You have successfully Purchased!');
            window.location.href = '/mainPage';
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error during Purchase:', error);
    });
}

