function deleteProduct(productId) {
    fetch('/delete_product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ Product_ID: productId })
    })
    .then(response => {
        if (response.ok) {
            alert("Product deleted successfully.");
            location.reload(); // Reload the page after delete
        } else {
            alert("Failed to delete product.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}