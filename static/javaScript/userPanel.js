function goToMainPage() {
    window.location.href = '/mainPage';  // Replace '/mainPage' with the actual URL of your main page
}

const updateUserForm = document.querySelector('form');

function checkUpdate() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const phoneNumber = document.getElementById('phone_number').value;
  const email = document.getElementById('Email').value;
  const storeAddress = document.getElementById('store_address').value;

  if (!password || !phoneNumber || !email) {
    alert('Please fill in all required fields.');
    return;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert('Please enter a valid email address.')
    return;
  }
  const phoneRegex = /^\d{11}$/; // 11-digit phone number
  if (!phoneRegex.test(phoneNumber)) {
    alert('Please enter a valid 10-digit phone number.');
    return;
  }

  const data = {
    password: password,
    phone_number: phoneNumber,
    Email: email,
    store_address: storeAddress
  };

  fetch('/user_panel', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (response.ok) {
      alert('Information Updated successfully!');
      location.reload(); // Reload the page after update
    } else {
      alert('Failed to update user information.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred while updating user information.');
  });
}