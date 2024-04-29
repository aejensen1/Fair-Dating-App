// validation.js

function validateBirthdate() {
    var dobInput = document.getElementById('birthdate');
    var dobValue = dobInput.value;
    var dobDate = new Date(dobValue);
    var today = new Date();
    var age = today.getFullYear() - dobDate.getFullYear();
    var monthDiff = today.getMonth() - dobDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dobDate.getDate())) {
        age--;
    }
    if (age < 18) {
        alert("You must be 18 years or older to register.");
        return false;
    }
    return true;
}
