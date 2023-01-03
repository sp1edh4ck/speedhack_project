document.getElementById("submit").onclick = function() {
    var password = document.getElementById("password");
    var confirmPassword = document.getElementById("confirmPassword");
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");

    password.onkeyup = function() {
        var lowerCaseLetters = /[a-z]/g;
        if (password.value.match(lowerCaseLetters)) {
            letter.classList.remove("invalid");
            letter.classList.add("valid");
        }
        else {
            letter.classList.remove("valid");
            letter.classList.add("invalid");
        }

        var upperCaseLetters = /[A-Z]/g;
        if (password.value.match(upperCaseLetters)) {
            capital.classList.remove("invalid");
            capital.classList.add("valid");
        }
        else {
            capital.classList.remove("valid");
            capital.classList.add("invalid");
        }

        var numbers = /[0-9]/g;
        if (password.value.match(numbers)) {
            number.classList.remove("invalid");
            number.classList.add("valid");
        }
        else {
            number.classList.remove("valid");
            number.classList.add("invalid");
        }

        if (password.value.length >= 12) {
            length.classList.remove("invalid");
            length.classList.add("valid");
        }
        else {
            length.classList.remove("valid");
            length.classList.add("invalid");
        }
    }
};
