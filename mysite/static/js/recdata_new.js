function initMap() {
 // Initialize Firebase
  var config = {
   apiKey: "AIzaSyDxKuTN_37C3dcJWkrlJSAYq1fW_UpKOzQ",
   //apiKey: "AIzaSyDxIMPruYEmxjt21qme-k0fQHK3RAXytpY",
   authDomain: "file2net-a30e6.firebaseapp.com",
   databaseURL: "https://file2net-a30e6.firebaseio.com",
   projectId: "file2net-a30e6",
   storageBucket: "file2net-a30e6.appspot.com",
   messagingSenderId: "505532311925"
  };
  firebase.initializeApp(config);
 // ref storage
  var storage = firebase.storage();
  var storageRef = storage.ref();

// original
  var gpsid = new firebase.database().ref();
  var provi = new google.maps.LatLng( -33.4266216,-70.6222754);
  var map = new google.maps.Map(document.getElementById('map'), {
    center: provi,
    zoom: 15
    });
// Despliega todos los puntos de la base de datos
 gpsid.orderByKey().on("value", function(snapshot) {
   snapshot.forEach(function(data) {
       var lat = data.child("lat").val().replace("@",".");
       console.log("# " + data.key + " Contando " + data.val());
       console.log(lat);
       var lon = data.child("lon").val().replace("@",".");
       var fecha = data.child("Fecha").val();
       var cosas = data.child(fecha).toJSON();
       var Lista = "";

       // Obteniendo todas las claves del JSON
       for (var clave in cosas){
         // Controlando que json realmente tenga esa propiedad
         if (cosas.hasOwnProperty(clave)) {
           // Mostrando en pantalla la clave junto a su valor
        var Lista = Lista + "<br>" + clave+ ": " + cosas[clave];
         console.log(Lista);
         }
       }

       var santago = new google.maps.LatLng( lat , lon);
       var key = data.key;
    //   var getDownloadURL=storageRef.child('images/'+key+'.png').getDownloadURL().then(function(url){
    //     return url;
    //       });
      addMarker({
        coords:{lat:parseFloat(lat),lng:parseFloat(lon)},
        content:'<h2>Letrero NNNN...</h2>'+
                'Ubicado en Lat:' + lat + ' Lon:'+ lon+
                '<p><strong>Flujo el día: ' + fecha+'</p>'
                 + Lista
                //JSON.stringify(cosas)
      });

       function addMarker(props){
         var marker = new google.maps.Marker({
                   position:props.coords,
                   map:map
         });
         var coordInfoWindow = new google.maps.InfoWindow(
           {content:props.content}
         );

         marker.addListener('click', function(){
             coordInfoWindow.open(map, marker);
           });

         };


   });
});
// Segmento que levanta la información en cuanto algo cambia en la base.
  gpsid.orderByKey().on("child_changed", function(snapshot) {

          snapshot.forEach(function(data) {
            console.log("# " + data.key + " Contando " + data.val());
          });

          var key = snapshot.key;
          var cal = storageRef.child('images/'+key+'.png').getDownloadURL().then(function(url){
              var getDownloadURL = url;
              //  var spaceRef = storageRef.child('images/lat:-33@423@lon:-70@612.png');
              //console.log("gpsid: "+key);
              var lat = snapshot.child("lat").val().replace("@",".");
              var lon = snapshot.child("lon").val().replace("@",".");
              var fecha = snapshot.child("Fecha").val();
              var cosas = snapshot.child(fecha).val();
              var santago = new google.maps.LatLng( lat , lon);
              var provi = new google.maps.LatLng( -33.4266216,-70.6222754);
              var map = new google.maps.Map(document.getElementById('map'), {
                center: santago,
                zoom: 15
                });

              var marker = new google.maps.Marker({
                  position:{lat:parseFloat(lat),lng:parseFloat(lon)},
                  map:map
                });
              marker.addListener('click', function(){
                  coordInfoWindow.open(map, marker);
                });
              var coordInfoWindow = new google.maps.InfoWindow();
              coordInfoWindow.setContent(createInfoWindowContent(santago, map.getZoom()));
              coordInfoWindow.setPosition(santago);
              coordInfoWindow.open(map);
              map.addListener('zoom_changed', function() {
                  coordInfoWindow.setContent(createInfoWindowContent(santago, map.getZoom()));
                  coordInfoWindow.open(map);
              });
              function createInfoWindowContent(latLng, zoom) {
                var scale = 1 << zoom;
                return [
                    'Santiago, CL',
                    //'LatLng: ' + latLng,
                    'Lat:' + lat,
                    'Lon:'+ lon,
                    //  'Zoom level: ' + zoom,
                    'Fecha: ' + fecha,
                    '<strong>Objetos: ' + JSON.stringify(cosas) ,
                    'Persona: '+cosas.persona,
                    '<img style="-webkit-user-select: none;cursor: zoom-in;" src="'+ getDownloadURL +'" width="100" height="100">'
                  ].join('</strong><br>');
                };
                //finaliza la consulta para el jpg
              });
            // finaliza el forEach
          //});
        //Finaliza consulta
        });
};