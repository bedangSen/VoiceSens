function mobileCheck() {
  if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    return true;
  }
  return false;
}

function showLoader(show){
  var loadingContainer = document.querySelector('#messageLabel');
  if(show){
    loadingContainer.style.display = '';
  } else {
    loadingContainer.style.display = 'none';
  }
}

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

function hideElement(elSelector){
  document.querySelector(elSelector).style.display = 'none';
}

function showElement(elSelector){
  var el = document.querySelector(elSelector);
  el.style.display = 'block';
  el.style.opacity = '1.0';
}

function showForTime(elementSelector, timeInSeconds){
  var elem = document.querySelector(elementSelector);
  if(!elem){ return ; }
  elem.style.opacity = 0.0;
  elem.style.transition = 'opacity 300 ms';
  elem.style.opacity = 1.0;
  setTimeout(function(){
    elem.style.transition = null;
    elem.style.transition = 'opacity 300 ms';
    elem.style.opacity = 0.0;
  }, timeInSeconds + 200);
}

function exampleLoginAPICall(values, callback) {
    var bodyString = '?email=' + values.email + '&password=' + values.password;
    var http = new XMLHttpRequest();
    http.open("GET", "/login" + bodyString, true);
    http.send(bodyString);
    http.onreadystatechange = function() {
      if (http.readyState === 4) {
        var response = JSON.parse(http.responseText.trim());
        callback(response);
      }
    }
}

function isLivenessEnabled(){
  return document.querySelector('#livenessToggle').checked;
}

function takeToConsole(){
  window.location.href = '/console';
}

function setupFrontEnd() {
  window.myVoiceIt = new VoiceIt2.initialize('example_endpoint/', 'resources/face_detector.wasm');
  document.querySelector('#voiceEnrollmentBtn').addEventListener('click', function() {
    myVoiceIt.encapsulatedVoiceEnrollment({
      contentLanguage:'en-US',
      phrase:'never forget tomorrow is a new day',
      completionCallback:function(success){
        if(success){
          showMessage('Voice Enrollments Done!');
        } else {
          showMessage('Voice Enrollments Failed!', true);
        }
      }
    });
  });

  document.querySelector('#voiceVerificationBtn').addEventListener('click', function() {
    myVoiceIt.encapsulatedVoiceVerification({
      contentLanguage:'en-US',
      phrase:'never forget tomorrow is a new day',
      needEnrollmentsCallback:function(){
        // Three voice enrollments needed
        showForTime('#enrollVoice', 1600);
      },
      completionCallback:function(success){
        if(success){
          takeToConsole();
        }
      }
    });
  });

  document.querySelector('#faceVerificationBtn').addEventListener('click', function() {
    myVoiceIt.encapsulatedFaceVerification({
      doLiveness:isLivenessEnabled(),
      needEnrollmentsCallback:function(){
        // Three voice enrollments needed
        showForTime('#enrollFace', 1600);
      },
      completionCallback:function(success){
        if(success){
          takeToConsole();
        }
      }
    });
  });

  document.querySelector('#faceEnrollmentBtn').addEventListener('click', function() {
    myVoiceIt.encapsulatedFaceEnrollment({
      completionCallback:function(success){
        if(success){
          showMessage('Face Enrollment Done!');
        } else {
          showMessage('Face Enrollment Failed!', true);
        }
      }
    });
  });

  document.querySelector('#videoVerificationBtn').addEventListener('click', function() {
    myVoiceIt.encapsulatedVideoVerification({
      doLiveness:isLivenessEnabled(),
      contentLanguage:'en-US',
      phrase:'never forget tomorrow is a new day',
      needEnrollmentsCallback:function(){
        // Three video enrollments needed
        showForTime('#enrollVideo', 1600);
      },
      completionCallback:function(success){
        if(success){
          takeToConsole();
        }
      }
    });
  });

  document.querySelector('#videoEnrollmentBtn').addEventListener('click', function() {
    myVoiceIt.encapsulatedVideoEnrollment({
      contentLanguage:'en-US',
      phrase:'never forget tomorrow is a new day',
      completionCallback:function(success){
        if(success){
          showMessage('Video Enrollments Done!');
        } else {
          showMessage('Video Enrollments Failed!', true);
        }
      }
    });
  });

  window.frontEndInitialized = true;
  showLoader(false);
  if(window.loggedIn){
    showElement('#biometricOptions');
  }
}

window.onload = function(event) {
  window.frontEndInitialized = false;
  window.loggedIn = false;
  setupFrontEnd();

  if (mobileCheck()) {
    hideElement('#livenessContainer');
  }

  document.querySelector('input[name="email"]').addEventListener('keydown', function(){
    hideElement('#messageLabel');
  });

  document.querySelector('input[name="password"]').addEventListener('keydown', function(){
    hideElement('#messageLabel');
  });

  // Simulate login click when user presses Enter/Return key
  document.querySelector('#mainForm').addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
      document.querySelector('#loginBtn').click();
    }
  });

  function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
  }

  function validateCredentialsFormat(loginCreds){
    var passedCheck = true;
    var passwordField = document.querySelector('#passwordField');
    var emailField = document.querySelector('#emailField');
    if (loginCreds.password.length < 6) {
      passwordField.classList.add('error');
      passedCheck = false;
    } else {
      passwordField.classList.remove('error');
    }
    if (!isValidEmailAddress(loginCreds.email)) {
      emailField.classList.add('error');
      passedCheck = false;
    } else {
      emailField.classList.remove('error');
    }
    return passedCheck;
  }

  document.querySelector('#loginBtn').addEventListener('click', function() {
    var em = document.querySelector('input[name="email"]').value;
    var pass = document.querySelector('input[name="password"]').value;
    var loginCreds = {
      email: em,
      password: pass
    };

    if (validateCredentialsFormat(loginCreds)) {
      showLoader(true);
      exampleLoginAPICall(loginCreds, function(response) {
        if (response.ResponseCode === "SUCC") {
          window.loggedIn = true;
          window.myVoiceIt.setSecureToken(response.Token);
          if(window.frontEndInitialized){
            showLoader(false);
            showElement('#biometricOptions');
          }
          hideElement('#loginBtn');
          hideElement('#formOverlay');
          showMessage('Please choose a 2FA verification option below');
        } else {
          if(window.frontEndInitialized){
            showLoader(false);
          }
          showMessage('Sorry, user not found. Make sure you enter the right credentials', true);
        }
      });
    }

  });

};
