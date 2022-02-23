
/* Using HTML5 Text to Speech API For Implementing Text to Speech Functionality 
   Reference Article :- https://www.studytonight.com/post/javascript-text-to-speech-using-speechsynthesis-interface */

function textToAudio() {
    let msg = document.getElementById("text-to-speech").value;
                
    let speech = new SpeechSynthesisUtterance();
    speech.lang = "en-US";
                
    speech.text = msg;
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;
                
    window.speechSynthesis.speak(speech);
}

$('#smoke-effect, #smoke-effect-canvas').SmokeEffect();