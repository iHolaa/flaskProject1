function checkLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message === 'Successful') {
            alert('You have successfully logged in!');
            window.location.href = '/mainPage'; // Redirect to mainPage.html
        } else {
            alert('Username or password is wrong!');
        }
    })
    .catch(error => {
        console.error('Error during login:', error);
    });
}