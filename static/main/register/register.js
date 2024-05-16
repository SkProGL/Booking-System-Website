let nameInput = document.querySelector('#name'),
    surnameInput = document.querySelector('#surname'),
    emailInput = document.querySelector('#email'),
    phone = document.querySelector("#phone");


const phoneInput = intlTelInput(phone, {
    initialCountry: "gb",
    strictMode: true,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@21.1.1/build/js/utils.js",

});
nameInput.focus()
validateInput(nameInput, 'letters');
validateInput(surnameInput, 'letters');
validateInput(usernameInput, 'nosymbols');
validateInput(emailInput, 'nospaces');
validateInput(passwordInput, 'nospaces');

showPassword(displayPassword, passwordInput)

passwordInput.addEventListener('input', () => {
    lowercase = passwordInput.value.toString().match(lowerCaseLetters) ? 'none' : 'inline-block';
    uppercase = passwordInput.value.toString().match(upperCaseLetters) ? 'none' : 'inline-block';
    number = passwordInput.value.toString().match(numbers) ? 'none' : 'inline-block';

    document.querySelector('#password-hint-1').style.display = number;
    document.querySelector('#password-hint-2').style.display = uppercase;
    document.querySelector('#password-hint-3').style.display = lowercase;
})

function validateForm() {
    // HTML form already handles minimum and maximum number of characters for each of these fields
    // this code checks the validity of data, using regular expressions
    let message = '';

    message += regexValidateLetters(nameInput.value) ? '' : "Make sure your name contains letters only.\n";
    message += regexValidateLetters(surnameInput.value) ? '' : "Make sure your surname contains letters only.\n";
    message += regexValidateEmail(emailInput.value) ? '' : 'Make sure your email is valid.\n';
    message += (phoneInput.isValidNumber()) ? '' : 'Make sure your phone is valid.\n';
    message += (passwordInput.value.toString().match(lowerCaseLetters)) ? '' : 'Password must contain 1 lowercase letter.\n';
    message += (passwordInput.value.toString().match(upperCaseLetters)) ? '' : 'Password must contain 1 uppercase letter.\n';
    message += (passwordInput.value.toString().match(numbers)) ? '' : 'Password must contain 1 number.\n';
    if (message.length > 0) {
        alert("Some of the provided information is wrong.\n" + message);
        return false;
    } else {
        alert("Everything is fine now.")
        // return false;
        return true
    }
}

