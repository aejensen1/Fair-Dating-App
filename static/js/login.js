$(document).ready(function(){
    // Test MongoDB Functions Button Click Event
    $('#testButton').click(function(){
        $.post('/test_mongodb_functions', function(data){
            alert(data);
        });
    });
    

    // Login AJAX Request
    $('#loginForm').submit(function(event){
        event.preventDefault(); // Prevent the default form submission

        // Get username and password from form inputs
        var username = $('#username').val();
        var password = $('#password').val();

        // Send AJAX request to login endpoint
        $.ajax({
            url: '/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(response) {
                console.log(response);
                // Handle successful login response
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                // Handle login error
            }
        });
    });
});
