// load the DOM first
document.addEventListener('DOMContentLoaded', function() {

    document.getElementsByClassName('filter-view').style.display = 'none'

    document.getElementById('submit').onsubmit = function() {
       var city = document.getElementById('search').innerHTML
       search(city)
   }

});

function search (city) {

    fetch('/all')
    .then(response => response.json())
    .then(search => { 
        Array.prototype.forEach.call(search.search, filter => {
            if (city.toUpperCase() == filter.toUpperCase()) {
                document.getElementsByClassName('filter-view').style.display = 'block'
                document.getElementsByClassName('filter-view').style.display = 'none'

                var filter_city = createElement('div')
                filter_city.className = 'container shadow-lg p-3 mb-5 bg-white rounded'
            }
        })
    })
}