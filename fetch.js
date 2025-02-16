fetch('/stations')
    .then(response => response.json())
    .then(data => { stations = data; })
    .catch(error => console.error('Error fetching stations:', error));
