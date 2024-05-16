function validateForm() {
    // HTML form already handles minimum and maximum number of characters for each of these fields
    // this code checks the validity of data, using regular expressions
    let message = '';
    email = document.getElementById('email');
    if (email) {
        message += regexValidateEmail(email.value) ? '' : 'Make sure your email is valid.\n';
    } else if (passwordInput) {
        message += (passwordInput.value.toString().match(lowerCaseLetters)) ? '' : 'Password must contain 1 lowercase letter.\n';
        message += (passwordInput.value.toString().match(upperCaseLetters)) ? '' : 'Password must contain 1 uppercase letter.\n';
        message += (passwordInput.value.toString().match(numbers)) ? '' : 'Password must contain 1 number.\n';
    }
    if (message.length > 0) {
        alert(message);
        return false;
    } else {
        alert("Everything is fine now.")
        // return false;
        return true
    }
}


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