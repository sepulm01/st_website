$(document).ready(function() {
///// AJAX  - INICIO ////////////////////
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({

    beforeSend: function(xhr, settings) {
    $('.loader').show();
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
      complete: function(){
     $('.loader').hide();
  },
  success: function() {
  //$('#loader').hide();
}
});


var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;
var mic_volume;
var hablando = false;
if (!('webkitSpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = function() {
    recognizing = true;
    showInfo('info_speak_now');
    start_img.src = '{% static '/img/mic-animate.gif' %}';
  };

  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      start_img.src ='{% static '/img/mic.gif' %}';
      showInfo('info_no_speech');
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      start_img.src = '{% static '/img/mic.gif' %}';
      showInfo('info_no_microphone');
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        showInfo('info_blocked');
      } else {
        showInfo('info_denied');
      }
      ignore_onend = true;
    }
  };

  recognition.onend = function() {
    recognizing = false;
    if (ignore_onend) {
      return;
    }
    start_img.src = '{% static '/img/mic.gif' %}';
    if (!final_transcript) {
      showInfo('info_start');
      return;
    }
    showInfo('');
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
      var range = document.createRange();
      range.selectNode(document.getElementById('final_span'));
      window.getSelection().addRange(range);
    }

  };

  recognition.onresult = function(event) {
    var interim_transcript = '';
    if (typeof(event.results) == 'undefined') {
      recognition.onend = null;
      recognition.stop();
      upgrade();
      return;
    }
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
        console.log("se calló?");
        recognition.stop();
        //readOutLoud(final_transcript)
        // envia mensaje al servidor
        chat_bot(final_transcript);

      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = capitalize(final_transcript);
    final_span.innerHTML = linebreak(final_transcript);
    interim_span.innerHTML = linebreak(interim_transcript);
    if (final_transcript || interim_transcript) {
      showButtons('inline-block');

    }
  };
}

function upgrade() {
  start_button.style.visibility = 'hidden';
  showInfo('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}

function startButton(event) {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = "es-CL";
  recognition.start();
  ignore_onend = false;
  final_span.innerHTML = '';
  interim_span.innerHTML = '';
  start_img.src = '{% static '/img/mic-slash.gif' %}';
  showInfo('info_allow');
  showButtons('none');
  start_timestamp = event.timeStamp;
}

function showInfo(s) {
  if (s) {
    for (var child = info.firstChild; child; child = child.nextSibling) {
      if (child.style) {
        child.style.display = child.id == s ? 'inline' : 'none';
      }
    }
    info.style.visibility = 'visible';
  } else {
    info.style.visibility = 'hidden';
  }
}

var current_style;
function showButtons(style) {
  if (style == current_style) {
    return;
  }
  current_style = style;
}

var speech = new SpeechSynthesisUtterance();
function readOutLoud(message) {
  // Set the text and voice attributes.
  speech.text = message;
  speech.volume = 1;
  speech.rate = 1;
  speech.pitch = 1;
  speech.lang = "es-CL";
  hablando = true
  recognition.stop();
  window.speechSynthesis.speak(speech);
  speech.onend = function() {
    hablando = false
  console.log('speech.onend');
  }
}


/////////////////////////////////////////////////////////////////////////////

var rec = 0
var name = "nadie"
var desc = ""
var sexo = ""
var anos = ""
var recon = 0
var anterior = ""
var caras = 0


function guarda(){
  rec = 1
  readOutLoud("¿Me puedes decir tu nombre por favor?")
  envia_desc(name, desc, rec, sexo, anos)
  console.log('Recorad@:', name)
  }

const video = document.getElementById('video')
const isScreenSmall = window.matchMedia("(max-width: 700px)");
let predictedAges = [];
console.log("cargando los modelos")
Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('{% static '/models' %}'),
  faceapi.nets.faceLandmark68Net.loadFromUri('{% static '/models' %}'),
  faceapi.nets.faceRecognitionNet.loadFromUri('{% static '/models' %}'),
  faceapi.nets.faceExpressionNet.loadFromUri('{% static '/models' %}'),
  faceapi.nets.ageGenderNet.loadFromUri('{% static '/models' %}'),
  //faceapi.nets.ssdMobilenetv1.loadFromUri('{% static '/models' %}')
]).then(startVideo)
//console.log(faceapi.nets)
function startVideo() {
  navigator.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video)
  //document.body.append(canvas)
  canvas.style.position = "absolute";
  canvas.style.left = "0";
  canvas.style.top = "0";
  canvas.style.zIndex = "10";
  $('.canvas-placement').append(canvas);

//   function resize_canvas(element)
// {
//   var w = element.offsetWidth;
//   var h = element.offsetHeight;
//   var cv = document.getElementById("cv1");
//   cv.width = w;
//   cv.height =h;
//  }

  const displaySize = { width: video.width, height: video.height }
  faceapi.matchDimensions(canvas, displaySize)

  // Loop sobre el video cada 100 milisegundos
  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions({inputSize: 512, scoreThreshold:0.75})).withFaceLandmarks().withFaceExpressions().withAgeAndGender().withFaceDescriptors()
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    if (resizedDetections.length != 0){
      const faceMatcher = new faceapi.FaceMatcher(resizedDetections)

      resizedDetections.forEach(fd => {
          const bestMatch = faceMatcher.findBestMatch(fd.descriptor)
          //downloadObject(fd.descriptor, 'descriptor.txt')
          name = bestMatch.toString()
          desc = fd.descriptor
          sexo = fd.gender
          anos = fd.age
          //console.log(name, bestMatch)
        })

      if (recon==0){
        revisa()
        recon = 1
      }

      var genero = resizedDetections[0].gender;
      if(genero=="male"){ var genero = "Hombre"} else { var genero = "Mujer"}
      const edad = parseInt(resizedDetections[0].age)
      const etiqueta = "Detección básica. "+ genero+", edad: "+edad+", nombre: "+ anterior; 
           
      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
      faceapi.draw.drawDetections(canvas, resizedDetections)
      faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
      faceapi.draw.drawFaceExpressions(canvas, resizedDetections)

      const box = { x: (video.width*.35), y: 50, width: 10, height: 0   }
      const drawOptions = {
        label: etiqueta,
        lineWidth: 2
      }
      const drawBox = new faceapi.draw.DrawBox(box, drawOptions)
      drawBox.draw(canvas)

      const brand = { x: 10, y: 32, width: 10, height: 0   }
      const brandOptions = {
        label: "Brand",
        lineWidth: 2
      }
      const brandBox = new faceapi.draw.DrawBox(brand, brandOptions)
      brandBox.draw(canvas)

    } else {
      if (recon==1){
        recognition.stop();
      }
      recon = 0

    }

  }, 1000) 
})

function envia_desc(name, desc, rec, sexo, anos){
  //console.log("desde func", name, desc)
  console.log(csrftoken)
  var claves = {
              'nombre': name,
              'descriptores' : desc.toString(),
              'record': rec,
              'sexo': sexo,
              'anos': anos,
              };
  $.ajax({
        method: "POST",
        //'async': false,
        url: '/ajax/descriptores/',
        data: claves ,
        success: function (data){
        console.log(data);
        }});
}

function revisa(){
  //recognition.stop();
  var claves = {
              'descriptores' : desc.toString(),
              'sexo': sexo,
              'anos': anos,
              };
    $.ajax({
        method: "GET",
        //'async': false,
        url: '/ajax/descriptores/',
        data: claves ,
        success: function (data){
        //console.log(data);
        
        //console.log("compara",data.nombre, anterior)
        if (data.nombre != anterior){

         message = 'Hola '+data.nombre+", Qué bebida deseas tomar?"
         $('#titulo').html(message)
        readOutLoud(message)
        }
        
        anterior = data.nombre
        }});
}

function chat_bot(mensaje){
  console.log("YO",mensaje)
  var chat = {
        "mensaje":mensaje,
      };
      $.ajax({
        method: "GET",
        //'async': false,
        url: '/ajax/chat/',
        data: chat ,
        success: function (data){
        console.log(data);
        readOutLoud(data.respuesta)

        }});
}

///////////////// microfono /////////////////////////////////////////

navigator.mediaDevices.getUserMedia({ audio: true, video: true })
.then(function(stream) {
  audioContext = new AudioContext();
  analyser = audioContext.createAnalyser();
  microphone = audioContext.createMediaStreamSource(stream);
  javascriptNode = audioContext.createScriptProcessor(2048, 1, 1);

  analyser.smoothingTimeConstant = 0.8;
  analyser.fftSize = 1024;

  microphone.connect(analyser);
  analyser.connect(javascriptNode);
  javascriptNode.connect(audioContext.destination);
  javascriptNode.onaudioprocess = function() {
      var array = new Uint8Array(analyser.frequencyBinCount);
      analyser.getByteFrequencyData(array);
      var values = 0;

      var length = array.length;
      for (var i = 0; i < length; i++) {
        values += (array[i]);
      }

      var average = values / length;

     mic_volume = Math.round(average)
     colorPids(average);
     if ( recognizing==false && hablando == false &&  mic_volume > 10 && recon==1){
     startButton(mic_volume)
     console.log('recognizing', recognizing, 'hablando',hablando);
      }
  }
  })
  .catch(function(err) {
    /* handle the error */
});


function colorPids(vol) {
  let all_pids = $('.pid');
  let amout_of_pids = Math.round(vol/10);
  let elem_range = all_pids.slice(0, amout_of_pids)
  for (var i = 0; i < all_pids.length; i++) {
    all_pids[i].style.backgroundColor="#e6e7e8";
  }
  for (var i = 0; i < elem_range.length; i++) {
    // console.log(elem_range[i]);
    elem_range[i].style.backgroundColor="#69ce2b";
  }
}

});