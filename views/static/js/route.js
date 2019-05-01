var hospital_json = "./hospitals.json";
var lng = 0.316644; 
var lat = 32.589536;
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(getPosition);
} else {
  alert("Geolocation is not supported by this browser.");
}

function getPosition(position) {
  lat = position.coords.latitude;
  lng = position.coords.longitude; 
}
function loadHospitalMap(){
    navigator.geolocation.watchPosition(getPosition);
    var myCurrentPosition = new google.maps.LatLng(lat, lng);
    map = new google.maps.Map(document.getElementById('route-map'), {
      center: myCurrentPosition,
      zoom: 18,
      mapTypeId:'roadmap',
    });
  
    var marker = new google.maps.Marker({
      position: myCurrentPosition, 
      map: map,
      icon:'/static/uploaded_files/icon-mee.png'
    });
  
     $.getJSON('/static/uploaded_files/hospitals.json', function(json1) {
        $.each(json1, function(key, data) {
      
            var latLng = new google.maps.LatLng(data.latitude, data.longitude); 
            // Creating a marker and putting it on the map
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                title: data.Name,	
                icon: '/static/uploaded_files/icon-hospital.png'
            });
  
          var clicker = addClicker(marker, data);
        });
    });
  
    function addClicker(marker, content) {
      var infowindow = new google.maps.InfoWindow();
      google.maps.event.addListener(marker, 'click', function() {
        if (infowindow) {infowindow.close();}
        destination = content.latitude+","+content.longitude; 
        var info = "<div style = 'width:250px;min-height:40px'>"+
                      "<p>"+content.Name+"</p>"+ 
                      "<p> Hour: "+content.Working_hours+"</p>"+
                      "<p> Tel: "+content.Phone_Contact+"</p>"+                         
                      "<button onclick='load_direction()' data='"+
                      destination+"'>Get Direction</button>"+
                   "</div>"; 
  
        infowindow.setContent(info); 
  
        infowindow.open(map, marker);
      });
    }
  
  }  

  function generateRoute(togeocord) {
    navigator.geolocation.watchPosition(getPosition);
    myCurrentPosition = new google.maps.LatLng(lat, lng);
    to = togeocord.split(',') 
    toDestination = new google.maps.LatLng(parseFloat(to[0]),parseFloat(to[1]));   
    var myOptions = {
      zoom: 13,
      center: myCurrentPosition,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }; 
    var mapObject = new google.maps.Map(document.getElementById("route-map"), myOptions);
  
    var directionsService = new google.maps.DirectionsService();
    var directionsRequest = {
      origin: myCurrentPosition,
      destination: toDestination,
      travelMode: google.maps.DirectionsTravelMode.DRIVING,
      unitSystem: google.maps.UnitSystem.METRIC
    };
    directionsService.route(
      directionsRequest,
      function(response, status)
      {
        if (status == google.maps.DirectionsStatus.OK)
        {
          new google.maps.DirectionsRenderer({
            map: mapObject,
            directions: response
          });
        }
        else
          $("#error").append("Unable to retrieve your route<br />");
      }
    );
  }
  
  function load_direction(e){
    e = e || window.event;
    var target = e.target || e.srcElement;
    var geocord =  target.getAttribute('data')
    generateRoute(geocord)
  }