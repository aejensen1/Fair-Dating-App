window.onload = function() {
    var textarea = document.getElementById('bio');
    var counter = document.getElementById('char-count');

    textarea.addEventListener('input', function() {
        var count = textarea.value.length;
        counter.textContent = count;

        if (count > 250) {
            textarea.value = textarea.value.slice(0, 250);
            counter.textContent = 250;
        }
    });
};