$(document).ready(function(){
    $('#testButton').click(function(){
        $.get('/test_mongodb_functions', function(data){
            alert(data);
        });
    });
});
