let displayPassword = document.querySelector(".password-show-button"),
    usernameInput = document.querySelector('#username'),
    passwordInput = document.querySelector("#password");
let lowerCaseLetters = /[a-z]/g,
    upperCaseLetters = /[A-Z]/g,
    numbers = /[0-9]/g;

// regex that checks whether input is letters only
// https://www.w3resource.com/javascript/form/all-letters-field.php#:~:text=To%20get%20a%20string%20contains,expression%20against%20the%20input%20value.
function validateInput(element, type = 'letters') {
    element.addEventListener("keypress", (evt) => {
        if (type === 'letters' && !regexValidateLetters(evt.key)) {
            evt.preventDefault();
        } else if (type === 'nosymbols' && (evt.key === ' ' || !evt.key.match(/^[a-zA-Z0-9]+$/))) {
            evt.preventDefault();
        } else if (type === 'nospaces' && evt.key === ' ') {
            evt.preventDefault();
        }
    })

}

function regexValidateLetters(text) {
    var re = /^[A-Za-z]+$/;
    return text.toString().match(re);
}

function regexValidateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return email.toString().match(re);
}

function showPassword(element, field) {
    element.addEventListener("click", () => {
        if (field.type === "password") {
            field.type = "text";
            element.innerText = "hide";
        } else {
            field.type = "password";
            element.innerText = "show";
        }
    })

}

