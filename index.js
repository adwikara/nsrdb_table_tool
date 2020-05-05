let {PythonShell} = require('python-shell');

//[42.3505, -71.1054]

let results = "";
latitude = document.getElementById("Latitude")
longitude = document.getElementById("Longitude")
resultBtn = document.getElementById("resultBtn")
outputField = document.getElementById("outputs")
let loadWheel = document.querySelectorAll('.loading')


//ONLY FOR NSRDB DATA
function getData(lat, lon) {
    var options = {
        mode: "text",
        scripPath: "./",
        args: [lat, lon]
    }

    let test = new PythonShell('irradiance_backend.py', options);
    test.on('message', function (message) {
        results  = results + message;
        
    });
}

// Click the Get Data Button
resultBtn.addEventListener('click', function() {
    // error check the latitude and longitude inputs
    if (latitude.value == "" || longitude.value == "") {
        latitude.style.color = "red";
        longitude.style.color = "red";
        latitude.value = "Please Enter Valid Input";
        longitude.value = "Please Enter Valid Input";
    } else {
        // turn on wheel
        loadWheel[0].style.display = "block";

        // get the nsrdb data from the python script
        getData(latitude.value, longitude.value)

        // show the table
        setTimeout(function() {
            // turn off wheel
            loadWheel[0].style.display = "none";
            // check if result was error
            if (results == "") {
                // most likely its because coordinates are not in US, so API failed
                let errorMsg = document.createElement('h3');
                errorMsg.className = 'error-msg';
                errorMsg.innerHTML = "API Data Not Available For This Location";
                errorMsg.align = "center";
                errorMsg.style.color = "red";       
                outputField.appendChild(errorMsg);
            } else {
                let div = document.createElement('div');
                div.className = 'table-div';
                div.innerHTML = results;
                console.log(results)
                
                outputField.appendChild(div)
                //console.log(results)
            }
        }, 7000)
    }
})

refreshBtn.addEventListener('click', function() {
    latitude.style.color = "black";
    longitude.style.color = "black";
    latitude.value = "";
    longitude.value = "";
    outputField.removeChild(outputField.childNodes[1])
    results = "";
});

