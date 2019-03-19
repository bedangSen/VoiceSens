function showLoader(show){
  var loadingContainer = document.querySelector('#messageLabel');
  if(show){
    loadingContainer.style.display = '';
  } else {
    loadingContainer.style.display = 'none';
  }
}

var usernamePointer = document.querySelector('#usernamePointer');
var passwordPointer = document.querySelector('#passwordPointer');
var repasswordPointer = document.querySelector('#repasswordPointer');

usernamePointer.style.display = 'none';
passwordPointer.style.display = 'none';
repasswordPointer.style.display = 'none';

function showMessage(message, error){
  var messageLabel = document.querySelector('#messageLabel');
  messageLabel.innerHTML = message;
  messageLabel.style.opacity = 1.0;
  messageLabel.style.display = '';
  if(error){
    messageLabel.style.opacity = 1.0;
    messageLabel.classList.add('red');
    messageLabel.classList.remove('viBtnColor');
  } else {
    messageLabel.classList.remove('red');
    messageLabel.classList.add('viBtnColor');
  }
}

window.onload = function(event) {
    // window.frontEndInitialized = false;
    // window.loggedIn = false;
    // setupFrontEnd();

    // if (mobileCheck()) {
    //   hideElement('#livenessContainer');
    // }

    // document.querySelector('input[name="email"]').addEventListener('keydown', function(){
    //   hideElement('#messageLabel');
    // });

    // document.querySelector('input[name="password"]').addEventListener('keydown', function(){
    //   hideElement('#messageLabel');
    // });

    // Simulate login click when user presses Enter/Return key
    document.querySelector('#mainForm').addEventListener('keydown', function(event) {
      if (event.keyCode === 13) {
        document.querySelector('#nextButton').click();
      }
    });

    function isValidEmailAddress(emailAddress) {
      var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
      return pattern.test(emailAddress);
    }

    function isValidUsername(username) {
      var pattern = /^[a-zA-Z0-9.\-_$@*!]{3,30}$/;
      return pattern.test(username);
    }


    function validateCredentialsFormat(loginCreds){
      var passedCheck = true;
      var passwordField = document.querySelector('#passwordField');
      var userField = document.querySelector('#userField');
      if (loginCreds.password.length < 6) {

        passwordPointer.style.display = '';

        passwordField.classList.add('error');
        passedCheck = false;
      } else {
        passwordField.classList.remove('error');
        passwordPointer.style.display = 'none';
      }
      if (loginCreds.repassword != loginCreds.password) {

        repasswordPointer.style.display = '';

        repasswordField.classList.add('error');
        passedCheck = false;
      }
      else {
        repasswordPointer.style.display = 'none';
        repasswordField.classList.remove('error');
      }
      // if (!isValidEmailAddress(loginCreds.email)) {
      //   emailField.classList.add('error');
      //   passedCheck = false;
      // } else {
      //   emailField.classList.remove('error');
      // }

      if(!isValidUsername(loginCreds.username)){
        usernamePointer.style.display = '';

        userField.classList.add('error');
        passedCheck = false;
      }
      else {
        usernamePointer.style.display = 'none';
        userField.classList.remove('error');
      }
      return passedCheck;
    }

    document.querySelector('#nextButton').addEventListener('click', function() {
      var us = document.querySelector('input[name="username"]').value;
      var pass = document.querySelector('input[name="password"]').value;
      var repass = document.querySelector('input[name="repassword"]').value;
      var loginCreds = {
        username: us,
        password: pass,
        repassword: repass
      };

      if (validateCredentialsFormat(loginCreds)) {
        showLoader(true);
        // exampleLoginAPICall(loginCreds, function(response) {
        //   if (response.ResponseCode === "SUCC") {
        //     window.loggedIn = true;
        //     window.myVoiceIt.setSecureToken(response.Token);
        //     if(window.frontEndInitialized){
        //       showLoader(false);
        //       showElement('#biometricOptions');
        //     }
        //     hideElement('#loginBtn');
        //     hideElement('#formOverlay');
        //     showMessage('Please choose a 2FA verification option below');
        //   } else {
        //     if(window.frontEndInitialized){
        //       showLoader(false);
        //     }
        //     showMessage('Sorry, user not found. Make sure you enter the right credentials', true);
        //   }
        // });

        // if (There is a user like that in the database) {
        //   ////showMessage('Please choose a 2FA verification option below');
        //   // Go to the next page.
        // }
        // else {
        //   showMessage('Sorry, user not found. Make sure you enter the right credentials', true);
        // }

        showMessage('There are no errors in your Login Credentials. But I do not know if there is such a user, until Kunal helps me set up Object storage. :)')
      }

      console.log("You clicked the login Next button");
    });

  };
