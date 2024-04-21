
const signupForm = document.querySelector('form');


function checkUsernameAvailability(username) {
  return fetch('/check-username', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username: username })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    return data.available;
  })
  .catch(error => {
    console.error('Error checking username availability:', error);
    return false;
  });
}
function checkForm() {
  const firstName = document.getElementById('first_name').value;
  const lastName = document.getElementById('last_name').value;
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const phoneNumber = document.getElementById('phone_number').value;
  const email = document.getElementById('Email').value;
  const storeAddress = document.getElementById('Store_address').value;

  if (!firstName || !lastName || !username || !password || !phoneNumber || !email) {
    alert('Please fill in all required fields.');
    return;
  }

    // Check if first and last names are strings
  if (!/^[a-zA-Z]+$/.test(firstName) || !/^[a-zA-Z]+$/.test(lastName)) {
    alert('First and last names must contain only letters.');
    return;
  }

  // Check if username starts with a string
  if (!/^[a-zA-Z]/.test(username)) {
    alert('Username must start with a letter.');
    return;
  }

  //email validation
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

  checkUsernameAvailability(username)
    .then(available => {
      if (!available) {
        alert('Username is already taken. Please choose a different username.');
      } else {
        alert('Account created successfully!');
        signupForm.submit();
      }
    })
    .catch(error => {
      console.error('Error checking username availability:', error);
    });
};

