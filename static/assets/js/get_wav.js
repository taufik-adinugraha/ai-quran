//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
var gumStream;
//stream from getUserMedia()
var rec;
//Recorder.js object
var input;
//MediaStreamAudioSourceNode we'll be recording
// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext;


function startRecording() {
	/* Simple constraints object, for more advanced audio features see
	https://addpipe.com/blog/audio-constraints-getusermedia/ */

	var constraints = {
	    audio: true,
	    video: false
	}

	/* We're using the standard promise based getUserMedia()
	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */
	audioContext.resume().then(() => {
		navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
			/* assign to gumStream for later use */
			gumStream = stream;
			/* use the stream */
			input = audioContext.createMediaStreamSource(stream);
			/* Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size */
			rec = new Recorder(input, {
			    numChannels: 1
			})
			//start the recording process
			rec.record()
		})
	});
}

function stopRecording() {
    rec.stop(); //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(upload);
}

function uploadRecording() {
		rec.stop();
    rec.exportWAV(upload);
		rec.clear();
		rec.record(); // record next ayat
}

// Required for Django CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var recordInterval
function countUp(start) {
	if (start) {
		var minutesLabels = document.getElementsByClassName("minutes");
	  var secondsLabels = document.getElementsByClassName("seconds");
	  var totalSeconds = 0;
	  recordInterval = setInterval(setTime, 1000);
	  function setTime(){
	      ++totalSeconds;
				[].forEach.call(secondsLabels, function (secondsLabel) {
					secondsLabel.innerHTML = pad(totalSeconds%60);
				});
				[].forEach.call(minutesLabels, function (minutesLabel) {
					minutesLabel.innerHTML = pad(parseInt(totalSeconds/60));
				});
	  }
	  function pad(val){
	    var valString = val + "";
	    if(valString.length < 2){
	        return "0" + valString;
	    }
	    else{
	        return valString;
	    }
	  }
	} else {
		clearInterval(recordInterval);
	}
}

function toggleRecordBtn(){
	$('.rekam').toggleClass("btn btn-danger  btn-round");
	$('.rekam').toggleClass("btn btn-success btn-round");
	if($('.rekam').hasClass("pulsate-fwd")){
		$('.rekam').removeClass("pulsate-fwd");
	}else{
		$('.rekam').addClass("pulsate-fwd");
	}
	if ($(".icon-rekam")[0].textContent == "mic_none"){
		$(".rekam").html('<span class="minutes">00</span>:<span class="seconds">00</span><br/><i class="icon-rekam material-icons">stop_circle</i> Stop');
		countUp(true);
		startRecording();
	} else {
		$(".rekam").html('<span class="minutes">00</span>:<span class="seconds">00</span><br/><i class="icon-rekam material-icons">mic_none</i> Rekam');
		countUp(false);
		stopRecording();
	}
}
// toggle record button
$('.rekam').click(function() {
	toggleRecordBtn()
});
