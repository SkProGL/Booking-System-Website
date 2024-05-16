document.getElementById('manage').style.display = 'none';
let action = document.querySelector('#database-action');

var selectedId = {};
var selectedField = [];
let generatedInputs = document.querySelectorAll('.generated-input');
if (action.value === 'update') {
    fieldAccess();
}

checkIn = generatedInputs[2];
checkOut = generatedInputs[3];
checkIn.style.width = "163px";
checkOut.style.width = "163px";
checkIn.type = "date";
checkOut.type = "date";
checkIn.min = new Date().toISOString().split('T')[0];
checkOut.min = checkIn.value
checkIn.addEventListener('change', () => {
    let inDate = new Date(checkIn.value);
    inDate.setDate(inDate.getDate() + 1);
    checkOut.min = inDate.toISOString().split('T')[0];
    checkOut.showPicker();
})

document.getElementById('invoice-button').addEventListener('click', () => {
    if (selectedId) {
        window.location = document.getElementById('base-url').href + 'generate_invoice/' + selectedId.toString()

    }
})

function fieldAccess() {
    generatedInputs[2].classList.remove("disable");
    generatedInputs[3].classList.remove("disable");

}

function getTableRow(row) {
    let tableRow = document.querySelector('table').rows[row].cells;
    let headerRow = document.querySelector('table').rows[0].cells;
    let text = ''


    for (let i = 0; i < tableRow.length; i++) {
        if (i === 0) {
            selectedId = tableRow[i].innerText;
        }
        text += headerRow[i].innerText + ' ' + tableRow[i].innerText + '\n';
        selectedField.push(tableRow[i].innerText);
        generatedInputs[i].value = tableRow[i].innerText;
    }
    document.getElementById('manage').style.display = 'block'
    // alert(text)
}

action.addEventListener('change', () => {
    let label = document.querySelectorAll('.generated-input-label')[0],
        input = document.querySelectorAll('.generated-input')[0]
    // console.log(action.value)
    if (action.value === 'update') {
        label.style.display = 'block'
        input.style.display = 'block'
        fieldAccess();
    } else if (action.value === 'delete') {
        label.style.display = 'block';
        input.style.display = 'block';
        generatedInputs[2].classList.add("disable");
        generatedInputs[3].classList.add("disable");
        generatedInputs[2].value = selectedField[2];
        generatedInputs[3].value = selectedField[3];

    }
})

function validateForm() {
    if (action.value === 'delete') {
        if (confirm("Note: Cancellation of booking may incur charges of up to 100%")) {
            return true;
        }
        return false;

    }
}