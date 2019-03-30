// hideElement('#progress');
hideElement('#environmentMessage');
hideElement('#vadMessage');
hideElement('#passphraseMessage');
hideElement('#acceptMessage');
hideElement('#rejectMessage');
hideElement('#authenticationComplete');
hideElement('#authenticationInComplete');
hideElement('#enrollmentComplete');

document.querySelector('#stopRecButton').classList.add('disabled');

var x = document.referrer;
console.log("The refferer of this page is : ", x);

var wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: '#01BAB6',
  interact: false,
  cursorWidth: 0,
  barGap: 2,
  barHeight: 2,
  barWidth: 0,
  fillParent: true,
  forceDecode: true,
  plugins: [
    WaveSurfer.microphone.create()
  ]
});

wavesurfer.microphone.on('deviceReady', function (stream) {
  console.log('Device ready!', stream);
});
wavesurfer.microphone.on('deviceError', function (code) {
  console.warn('Device error: ' + code);
});

// start the microphone
wavesurfer.microphone.start();

// pause rendering
//wavesurfer.microphone.pause();

// resume rendering
//wavesurfer.microphone.play();

// stop visualization and disconnect microphone
//wavesurfer.microphone.stopDevice();

// same as stopDevice() but also clears the wavesurfer canvas
//wavesurfer.microphone.stop();

// destroy the plugin
//wavesurfer.microphone.destroy();

// create an audio in
mic = new p5.AudioIn();

// users must manually enable their browser microphone for recording to work properly!
mic.start();

// create a sound recorder
recorder = new p5.SoundRecorder();

// connect the mic to the recorder
recorder.setInput(mic);

// create an empty sound file that we will use to playback the recording
soundFile = new p5.SoundFile();

if (document.referrer == "http://localhost:8080/enroll") {
  // number of attempts for enrollment.
  var number_of_attempts = 3;
  console.log("number of attempts : ", number_of_attempts);
}
else {
  // number of attempts for enrollment.
  var number_of_attempts = 1;
  console.log("number of attempts : ", number_of_attempts);
}


// One-liner to resume playback when user interacted with the page.
document.querySelector('#startRecButton').addEventListener('click', function () {

  // For the background sound
  if (document.querySelector('#passphraseMessage').style.display == 'none') {
    showElement('#environmentMessage');

    console.log("You have started recording passphrase...");
    recorder.record(soundFile);
  } else {
    document.querySelector('#passphraseMessage').classList.add('green');;

    console.log("You have started recording the background...");
    recorder.record(soundFile);
  }

  document.querySelector('#startRecButton').classList.add('disabled');
  document.querySelector('#stopRecButton').classList.remove('disabled');
});

document.querySelector('#stopRecButton').addEventListener('click', function () {

  if (document.querySelector('#passphraseMessage').style.display == '') {

  document.querySelector('#stopRecButton').classList.add('disabled');
  document.querySelector('#passphraseMessage').classList.remove('green');

    hideElement("#passphraseMessage");
    showElement("#vadMessage");

    stopRecording();
  }
  // For the background sound
  else {
    document.querySelector('#startRecButton').classList.remove('disabled');
  document.querySelector('#stopRecButton').classList.add('disabled');

    hideElement("#environmentMessage");
    showElement("#vadMessage");

    stopBackgroundRecording();
  }

});

function stopRecording() {
  console.log("You have stopped recording...");
  recorder.stop(); // stop recorder, and send the result to soundFile

  console.log("Playing the audioifle now...");
  soundFile.play();

  // console.log("Saving the audio file now...");
  // p5.prototype.saveSound(soundFile, file_name); // save file

  console.log("Saving the SoundFile to a blob file ...");
  var soundBlob = soundFile.getBlob();

  // Now we can send the blob to a server...
  var xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
      console.log("xhr.resposne : ", xhr.response);

      if (xhr.response == "fail") {
        hideElement('#vadMessage');
        showElement('#rejectMessage');


      } else if (xhr.response == "pass") {
        hideElement('#vadMessage');
        showElement('#acceptMessage');

        number_of_attempts--;
        console.log("number of attempts : ", number_of_attempts);
      } else {
        showElement('#passphraseMessage');
        hideElement('#vadMessage');

        document.getElementById('randomPassphrase').innerHTML = xhr.response;
      }
    }
  }

  xhr.open("POST", "/voice", true);
  xhr.send(soundBlob);

  console.log("Your http message has been sent.");
}

function stopBackgroundRecording() {
  console.log("You have stopped recording...");
  recorder.stop(); // stop recorder, and send the result to soundFile

  console.log("Playing the audioifle now...");
  soundFile.play();

  // console.log("Saving the audio file now...");
  // p5.prototype.saveSound(soundFile, file_name); // save file

  console.log("Saving the SoundFile to a blob file ...");
  var soundBlob = soundFile.getBlob();

  // Now we can send the blob to a server...
  var xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
      showElement('#passphraseMessage');
      hideElement('#vadMessage');
      document.getElementById('randomPassphrase').innerHTML = xhr.response;
      console.log("xjr.resposne : ", xhr.response);
    }
  }

  xhr.open("POST", "/vad", true);
  xhr.send(soundBlob);

  number_of_attempts--;
  console.log("Your http message has been sent.");
  console.log("number of attempts : ", number_of_attempts);
}

document.querySelector('#close_button_accept').addEventListener('click', function () {
  if (number_of_attempts < 0) {
    if (document.referrer == "http://localhost:8080/auth") {
      hideElement('#acceptMessage');
      showElement('#vadMessage');
      hideElement('#passphraseMessage');

      var analysis_text = 'Identifying user based on voice print';
      document.getElementById('recordBody').innerHTML = analysis_text;

      document.querySelector('#vadMessage').classList.add('green');
      document.querySelector('#vadMessage').classList.remove('yellow');

      var xhr = new XMLHttpRequest();

      xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
          // showElement('#passphraseMessage');
          // hideElement('#vadMessage');
          // document.getElementById('randomPassphrase').innerHTML = xhr.response;
          console.log("xjr.resposne : ", xhr.response);

          if (xhr.response == "success") {
            showElement('#authenticationComplete');
          } else {
            showElement('#authenticationIncomplete');
          }
        }
      }

      xhr.open("GET", "/verify", true);
      xhr.send();
    }
    else {
      hideElement('#acceptMessage');
      showElement('#vadMessage');
      hideElement('#passphraseMessage');

      var analysis_text = 'Building Voice Print';
      document.getElementById('recordBody').innerHTML = analysis_text;

      document.querySelector('#vadMessage').classList.add('green');
      document.querySelector('#vadMessage').classList.remove('yellow');

      var xhr = new XMLHttpRequest();

      xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
          // showElement('#passphraseMessage');
          hideElement('#vadMessage');
          // document.getElementById('randomPassphrase').innerHTML = xhr.response;
          console.log("xjr.resposne : ", xhr.response);

          showElement("#enrollmentComplete");
        }
      }

      xhr.open("GET", "/biometrics", true);
      xhr.send();
    }
  }
  else {
    document.querySelector('#startRecButton').classList.remove('disabled');

    hideElement('#acceptMessage');
    showElement('#vadMessage');
    hideElement('#passphraseMessage');

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        showElement('#passphraseMessage');
        hideElement('#vadMessage');
        document.getElementById('randomPassphrase').innerHTML = xhr.response;
        console.log("xjr.resposne : ", xhr.response);
      }
    }

    xhr.open("GET", "/vad", true);
    xhr.send();
  }
});

document.querySelector('#close_button_reject').addEventListener('click', function () {
  document.querySelector('#startRecButton').classList.remove('disabled');

  showElement('#vadMessage');
  hideElement('#rejectMessage');
  hideElement('#passphraseMessage');

  var xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
      showElement('#passphraseMessage');
      hideElement('#vadMessage');
      document.getElementById('randomPassphrase').innerHTML = xhr.response;
      console.log("xjr.resposne : ", xhr.response);
    }
  }

  xhr.open("GET", "/vad", true);
  xhr.send();
});

function hideElement(elSelector) {
  document.querySelector(elSelector).style.display = 'none';
}

function showElement(elSelector) {
  document.querySelector(elSelector).style.display = '';
}
