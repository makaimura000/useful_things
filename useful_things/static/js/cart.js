$(document).ready(function() {
    var counter_text = document.getElementById('cart-product-conter-text');
    var counter = document.getElementById('cart-product-counter').dataset.counter;
    var last_digit = counter.slice(-1)
    var added_ending = null
    if (last_digit == 0) {
        added_ending = 'ов';
    } else if (last_digit == 1) {
        added_ending = '';
    } else if (counter > 0 && counter < 5) {
        added_ending = 'а';
    } else if (counter >= 5 && counter <= 20) {
        added_ending = 'ов';
    } else if (last_digit > 0 && counter <= 4) {
        added_ending = 'а';
    } else {
        added_ending = 'ов';
    }
    counter_text.innerHTML += added_ending;
});