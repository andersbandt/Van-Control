

$(document).ready(function() {
    
    var item1Click = false;

    function clickHandler(){
        item1Click = true;
        alert("youve been clicked!")
}

var element = document.getElementById('item1');

element.addEventListener('click', clickHandler);

});
