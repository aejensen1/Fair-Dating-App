window.onload = function() {
    var bioTextarea = document.getElementById('bio');
    var bioCounter = document.getElementById('bio-char-count');

    bioTextarea.addEventListener('input', function() {
        var count = bioTextarea.value.length;
        bioCounter.textContent = count;

        if (count > 250) {
            bioTextarea.value = bioTextarea.value.slice(0, 250);
            bioCounter.textContent = 250;
        }
    });

    var interestsTextarea = document.getElementById('interests');
    var interestsCounter = document.getElementById('interests-char-count');

    interestsTextarea.addEventListener('input', function() {
        var count = interestsTextarea.value.length;
        interestsCounter.textContent = count;

        if (count > 50) {
            interestsTextarea.value = interestsTextarea.value.slice(0, 50);
            interestsCounter.textContent = 50;
        }
    });
};