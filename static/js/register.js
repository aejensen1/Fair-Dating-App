// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Find the registration form element
    var registerForm = document.getElementById('registerForm');

    // Add a submit event listener to the form
    registerForm.addEventListener('submit', function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Extract the username and password from the form
        var usernameInput = document.getElementById('username');
        var passwordInput = document.getElementById('password');
        var username = usernameInput.value;
        var password = passwordInput.value;

        // Validate the form data (optional)
        if (!username || !password) {
            // Display an error message if the form data is invalid
            alert('Please enter both username and password.');
            return;
        }

        // Create a data object with the form data
        var formData = {
            username: username,
            password: password
        };

        // Send a POST request to the registration endpoint
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server
            console.log(data);
            // Optionally, display a success message or redirect the user
        })
        .catch(error => {
            // Handle any errors that occur during the fetch request
            console.error('Error:', error);
            // Optionally, display an error message to the user
        });
    });
});
