function goBack() {
    window.location.href = '/user_PurchaseList';
}

function submitForm() {
    const form = document.querySelector('form');
    const formData = new FormData(form);
    fetch('/rate_ProductPage', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            window.location.href = '/user_PurchaseList';
        } else {
            alert(data.message);
            window.location.href = '/user_PurchaseList';
        }
    })
    .catch(error => {
        alert("An error occurred while processing your request.");
        window.location.href = '/user_PurchaseList';
    });
}

