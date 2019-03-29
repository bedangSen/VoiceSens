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

    var xhttp = new XMLHttpRequest();

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        window.location.href = '/voice';
      }
    }

    xhr.open("GET", "/voice", true);
    xhr.setRequestHeader("Content-type", "application/json");

    xhr.send();

    console.log("The enroll button works!");

    xhttp.open("POST", "/auth", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    xhttp.send(JSON.stringify(loginCreds));

    console.log("Your http message has been sent.");

    console.log("You clicked the login Next button");
  });

};
