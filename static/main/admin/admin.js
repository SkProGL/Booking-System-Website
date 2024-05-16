// ajax request to server
// https://gist.github.com/KentaYamada/2eed4af1f6b2adac5cc7c9063acf8720


currentTable = document.querySelector('#current-table');
changeTable = document.querySelector('#change-table');
changeTable.value = currentTable.innerText;
changeTable.addEventListener('change', () => {
    window.location = document.getElementById('base-url').href + 'admin/' + changeTable.value.toString()
})
let generatedInputs = document.querySelectorAll('.generated-input')

function getTableRow(row) {
    let myList = document.querySelector('table').rows[row].cells;
    let text = ''

    for (let i = 0; i < myList.length; i++) {
        text += myList[i].innerText + '\n';
        generatedInputs[i].value = myList[i].innerText;

    }
    document.querySelector('[for="database-action"]').scrollIntoView({behavior: 'smooth'});

}

let action = document.querySelector('#database-action');
action.addEventListener('change', () => {
    let label = document.querySelectorAll('.generated-input-label')[0],
        input = document.querySelectorAll('.generated-input')[0]
    console.log(action.value)
    if (action.value === 'update') {
        label.style.display = 'block'
        input.style.display = 'block'
    } else if (action.value === 'delete') {
        label.style.display = 'block'
        input.style.display = 'block'
    } else if (action.value === 'create') {
        label.style.display = 'none'
        input.style.display = 'none'
        generatedInputs.forEach(n => n.value = '')
    }
})

function validateForm() {
    if (action.value === 'create') {

    }
    if ((action.value === 'update' && !generatedInputs[0].value) || (action.value === 'delete' && !generatedInputs[0].value)) {
        alert('Make sure to choose row to ' + action.value.toString());
        return false;
    }
    return true;
}