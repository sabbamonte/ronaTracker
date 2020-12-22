// load the DOM first
document.addEventListener('DOMContentLoaded', function() {

    button =  document.getElementsByClassName('submit_post')
    document.getElementsByClassName('submit_post').onsubmit = function () {
        var states = getElementById('inputState')
        var selected_state= states.options[states.selectedIndex].value;
        console.log(selected_state)
        if (document.getElementsByClassName('checkbox').checked === true) {
            status = document.getElementsByClassName('checkbox').value
            console.log(status)
            add_post(status, state)
        }

    }

});

function add_post(status, state) {

    fetch('/add', {
        method: "POST",
        body: JSON.stringify ({
            state: state,
            diagnosis: status
        })

    })
}