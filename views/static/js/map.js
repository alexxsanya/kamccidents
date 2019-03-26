var hospital_json = "./hospitals.json";
var lng = 0;
var lat = 0;
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(getPosition);
} else {
  alert("Geolocation is not supported by this browser.");
}

function getPosition(position) {
  lat = position.coords.latitude;
  lng = position.coords.longitude; 
}

function loadHeatMap(){
  document.querySelector('beacon').setAttribute('style',"display:inline");
  document.getElementById('hospital-map-label').setAttribute('hidden','hidden');

  headmap_db = []
  $.getJSON('/all-accidents', function(json1) {
      $.each(json1, function(key, data) {
        var geo = data.acc_location.split(',') 
        console.log(data)
        headmap_db.push({location: new google.maps.LatLng(geo[0], geo[1]), weight: 0.5})
      });
  });

  console.log(headmap_db)
  var style = [
    {
      "featureType": "administrative",
      "elementType": "geometry",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "administrative.land_parcel",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "administrative.neighborhood",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "poi",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "poi",
      "elementType": "labels.text",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "road",
      "elementType": "labels",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "road",
      "elementType": "labels.icon",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "transit",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "water",
      "elementType": "labels.text",
      "stylers": [
        {
          "visibility": "off"
        }
      ]
    }
  ]
 
  var kampalaCity = new google.maps.LatLng(0.316644, 32.589536);

  map = new google.maps.Map(document.getElementById('mapCanvas'), {
    center: kampalaCity,
    zoom: 14,
    mapTypeId: 'roadmap',
    styles: style
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: headmap_db
  });

  heatmap.setMap(map);

}


function loadHospitalMap(){
  document.querySelector('beacon').setAttribute('style',"display:none");
  document.getElementById('hospital-map-label').removeAttribute('hidden');
  var myCurrentPosition = new google.maps.LatLng(lat, lng);
  map = new google.maps.Map(document.getElementById('mapCanvas'), {
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
                    "<button onclick='get_direction()' data='"+
                    destination+"'>Get Direction</button>"+
                 "</div>"; 

      infowindow.setContent(info); 

      infowindow.open(map, marker);
    });
  }

}
function calculateRoute(to) {
  if(lat==0 & lng==0){
    lat= 0.3499986
    lng = 32.56716
    navigator.geolocation.watchPosition(getPosition);
  } 

  myCurrentPosition = new google.maps.LatLng(lat, lng);

  var myOptions = {
    zoom: 13,
    center: myCurrentPosition,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }; 
  var mapObject = new google.maps.Map(document.getElementById("mapCanvas"), myOptions);

  var directionsService = new google.maps.DirectionsService();
  var directionsRequest = {
    origin: myCurrentPosition,
    destination: to,
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

function get_direction(e){
  e = e || window.event;
  var target = e.target || e.srcElement;
  var geocord =  target.getAttribute('data')
  geocord = geocord.split(',') 
  console.log(geocord)
  var latLng = new google.maps.LatLng(parseFloat(geocord[0]),parseFloat(geocord[1]));   
  calculateRoute(latLng)
}