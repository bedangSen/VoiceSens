var usernamePointer = document.querySelector('#usernamePointer');
var passwordPointer = document.querySelector('#passwordPointer');


usernamePointer.style.display = 'none';
passwordPointer.style.display = 'none';

window.onload = function (event) {

  // Simulate login click when user presses Enter/Return key
  document.querySelector('#mainForm').addEventListener('keydown', function (event) {
    if (event.keyCode === 13) {
      document.querySelector('#nextButton').click();
    }
  });

  document.querySelector('#nextButton').addEventListener('click', function () {
    var us = document.querySelector('input[name="username"]').value;
    var pass = document.querySelector('input[name="password"]').value;

    var loginCreds = {
      username: us,
      password: pass
    };

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        console.log("Response : ", xhr.response);
        
        if (xhr.response == "Doesn't exist") {
          usernamePointer.style.display = '';
        }
        else{
          window.location.href = '/voice';
        }
      }
    }

    // xhr.open("GET", "/voice", true);
    // xhr.setRequestHeader("Content-type", "application/json");

    // xhr.send();

    // console.log("The enroll button works!");

    xhr.open("POST", "/auth", true);
    xhr.setRequestHeader("Content-type", "application/json");

    xhr.send(JSON.stringify(loginCreds));

    console.log("Your http message has been sent.");

    console.log("You clicked the login Next button");
  });

};
//
// function hideElement(elSelector) {
//   document.querySelector(elSelector).style.display = 'none';
// }
//
// function showElement(elSelector) {
//   document.querySelector(elSelector).style.display = '';
// }
