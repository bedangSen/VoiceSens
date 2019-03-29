// hideElement('#progress');
hideElement('#environmentMessage');
hideElement('#vadMessage');
hideElement('#passphraseMessage');
hideElement('#acceptMessage');
hideElement('#rejectMessage');

document.querySelector('#stopRecButton').classList.add('disabled');

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

// number of attempts for enrollment.
var number_of_attempts = 3; 

// One-liner to resume playback when user interacted with the page.
document.querySelector('#startRecButton').addEventListener('click', function () {

  console.log("number of attempts : ", number_of_attempts);
  

  // if (number_of_attempts <= 0 ) {
  //   //Or something like this. 
  //   document.querySelector('#startRecButton').classList.add('disabled');
  // }

  // For the background sound
  if (document.querySelector('#passphraseMessage').style.display == 'none') {
    showElement('#environmentMessage');

    console.log("You have started recording passphrase...");
    recorder.record(soundFile);
  } else {

    console.log("You have started recording the background...");
    recorder.record(soundFile);
  }
  
  document.querySelector('#startRecButton').classList.add('disabled');
  document.querySelector('#stopRecButton').classList.remove('disabled');

  // startRecording();
});

document.querySelector('#stopRecButton').addEventListener('click', function () {
  document.querySelector('#startRecButton').classList.remove('disabled');
  document.querySelector('#stopRecButton').classList.add('disabled');  
 
  if (document.querySelector('#passphraseMessage').style.display == '') {
    hideElement("#passphraseMessage");
    showElement("#vadMessage");

    stopRecording();
  }
  // For the background sound
  else{
    hideElement("#environmentMessage");
    showElement("#vadMessage");

    stopBackgroundRecording();
  }

  

  
});

function startRecording() {
  if (mic.enabled) {
    console.log("You have started recording...");
    recorder.record(soundFile, 30);
    
  }
}

function stopRecording() {
  console.log("You have stopped recording...");
  recorder.stop(); // stop recorder, and send the result to soundFile

  // console.log("Playing the audioifle now...");
  // soundFile.play();

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
      console.log(xhr.response);      
    }
  }

  xhr.open("POST", "/voice", true);
  xhr.send(soundBlob);  

  console.log("Your http message has been sent.");
}

function stopBackgroundRecording() {
  console.log("You have stopped recording...");
  recorder.stop(); // stop recorder, and send the result to soundFile

  // console.log("Playing the audioifle now...");
  // soundFile.play();

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
      console.log(xhr.response);      
    }
  }

  xhr.open("POST", "/vad", true);
  xhr.send(soundBlob);  

  console.log("Your http message has been sent.");
}

function hideElement(elSelector) {
  document.querySelector(elSelector).style.display = 'none';
}

function showElement(elSelector) {
  document.querySelector(elSelector).style.display = '';
}
