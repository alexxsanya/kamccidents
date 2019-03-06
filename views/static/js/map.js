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
  /* Data points defined as an array of LatLng objects */
/* Data points defined as a mixture of WeightedLocation and LatLng objects */
  var heatMapData = [
    {location: new google.maps.LatLng(0.318522, 32.595459), weight: 0.5},
    new google.maps.LatLng(0.317127, 32.593764),
    {location: new google.maps.LatLng(0.318726, 32.591650), weight: 15},
    {location: new google.maps.LatLng(0.314885, 32.594622), weight: 40},
    {location: new google.maps.LatLng(0.316762, 32.588399), weight: 2},
    new google.maps.LatLng(0.313898, 32.586843),
    {location: new google.maps.LatLng(0.314069, 32.587187), weight: 17},
    {location: new google.maps.LatLng(0.313501, 32.592562), weight: 3},
    {location: new google.maps.LatLng(0.312224, 32.587670), weight: 7},
    new google.maps.LatLng(0.316805, 32.585309),
    {location: new google.maps.LatLng(0.318704, 32.585889), weight: 0.5},
    new google.maps.LatLng(0.313887, 32.586886),
    {location: new google.maps.LatLng(0.318543, 32.584719), weight: 21},
    {location: new google.maps.LatLng(0.319251, 32.587948), weight: 6}
  ];

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
    zoom: 15,
    mapTypeId: 'roadmap',
    styles: style
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatMapData
  });

  heatmap.setMap(map);
}


function loadHospitalMap(){
  console.log(lat+" "+lng);
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

  function calculateRoute(to) {
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

  function addClicker(marker, content) {
    var infowindow = new google.maps.InfoWindow();
    google.maps.event.addListener(marker, 'click', function() {
      if (infowindow) {infowindow.close();}
      destination = new google.maps.LatLng(content.latitude, content.longitude); 
      var info = "<div style = 'width:250px;min-height:40px'>"+
                    "<p>"+content.Name+"</p>"+ 
                    "<p> Hour: "+content.Working_hours+"</p>"+
                    "<p> Tel: "+content.Phone_Contact+"</p>"+ 
                    "<div onclick='"+calculateRoute(destination)+"'>Get Direction</div>"+
                 "</div>"; 

      infowindow.setContent(info); 

      infowindow.open(map, marker);
    });
  }
}