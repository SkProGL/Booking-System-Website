// date subtraction extracted code
// https://stackoverflow.com/questions/4944750/how-to-subtract-date-time-in-javascript

let checkIn = document.querySelector("#wh-form-checkin"),
    checkOut = document.querySelector("#wh-form-checkout"),
    navBar = document.querySelector('#navigation_bar'),
    count = document.querySelector('#wh-form-count'),
    room = document.querySelector('#wh-form-room'),
    bookingForm = document.querySelector('.booking-form'),
    imageTile = document.querySelectorAll(".grid-group-item");
window.onhashchange = function () {
    //blah blah blah
    if (room.value === 'separate') {
        console.log('check!')
        document.querySelector('.wh-form-options').style.display = 'flex';
        adjustCount();
    }
}
if (room.value === 'separate') {
    console.log('tick!')
    document.querySelector('.wh-form-options').style.display = 'flex';
    adjustCount();
}
checkIn.min = new Date().toISOString().split('T')[0];
checkIn.max = new Date(Date.now() + (3600 * 1000 * 24 * 90)).toISOString().split('T')[0];
checkOut.min = checkIn.min

imageTile.forEach(n => {
    // console.log(n.getAttribute('value'))
    n.onclick = () => {
        document.querySelector('#wh-form-city').value = n.getAttribute('value')
        document.querySelector('.wh-form').scrollIntoView({behavior: 'smooth'});

        setTimeout(() => {
            checkIn.showPicker();
        }, 1500)

    }

})

bookingForm.addEventListener('click', () => document.querySelector('.wh-form').scrollIntoView({behavior: 'smooth'}));

// shows makeSearch button on scroll when booking search menu is not visible
document.addEventListener('scroll', () => {
    a = document.querySelector(".booking").getBoundingClientRect();
    if (a.y + a.height > 0) {
        bookingForm.style.display = 'none';
    } else {
        bookingForm.style.display = 'block';
    }
})

// sets minimum checkOutDate = currentDate + 1 day
// then shows checkOutDate picker for convenience
checkIn.addEventListener('change', () => {
    let inDate = new Date(checkIn.value);
    inDate.setDate(inDate.getDate() + 1);
    checkOut.min = inDate.toISOString().split('T')[0];
    checkOut.showPicker();
})

// adjusts number of separate rooms
count.addEventListener('change', () => adjustCount());
count.addEventListener('keypress', () => adjustCount());

// depending on room options chosen, shows separate room menu
room.addEventListener('change', () => {
    if (room.value === 'separate') {
        document.querySelector('.wh-form-options').style.display = 'flex';
        adjustCount();
    } else {
        document.querySelector('.wh-form-options').style.display = 'none';
    }

})


// generates new input fields for separate rooms
function adjustCount() {
    document.querySelectorAll('.wh-form-field-generated').forEach(e => e.remove());
    if (count.value > 4) {
        count.value = 4;
    }
    for (let i = 0; i < count.value; i++) {
        let container = document.createElement('div');
        container.classList.add('wh-form-field');
        container.classList.add('wh-form-field-generated');


        let labelElement = document.createElement('span');
        labelElement.classList.add('wh-form-label');
        labelElement.innerText = 'Room ' + (i + 1).toString()
        let inputElement = document.createElement('select');
        inputElement.classList.add('wh-form-input');
        inputElement.name = 'Room' + (i + 1).toString()
        let option1 = document.createElement('option');
        let option2 = option1.cloneNode(true), option3 = option1.cloneNode(true);
        option1.value = 'standard';
        option2.value = 'double';
        option3.value = 'family';
        option1.innerText = 'Standard, 1 guest';
        option2.innerText = 'Double, 2 guests';
        option3.innerText = 'Family, maximum 4 guests';

        inputElement.append(option1);
        inputElement.append(option2);
        inputElement.append(option3);

        container.append(labelElement);
        container.append(inputElement);
        document.querySelector('.wh-form-options').append(container);
    }
}

function validateForm() {
    let message = '';
    if (checkIn.value.toString().length < 1) {
        message += 'Check in date is not chosen.\n'
    }
    if (checkOut.value.toString().length < 1) {
        message += 'Check out date is not chosen.\n'
    }
    if (message.length > 0) {
        alert("Please fill in all fields!" + message);
        return false;

    } else {
        stayDuration = Math.abs(new Date(checkOut.value.toString()) - new Date(checkIn.value.toString())) / 1000 / 60 / 60 / 24
        stayMessage = `Your stay duration will be ${stayDuration} `
        if (stayDuration > 1) {
            stayMessage += `days.\n`
            if (stayDuration > 30) {
                alert('If you want to book a room for more than 30 days, you are required to make a separate booking.')
                return false;
            }
        } else {
            stayMessage += `day.\n`
        }

        return true;

    }
    // if (room.value)

}