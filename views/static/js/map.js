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

function loadHeatMap(){
  document.querySelector('beacon').setAttribute('style',"display:inline");
  document.getElementById('hospital-map-label').setAttribute('hidden','hidden');
  navigator.geolocation.watchPosition(getPosition);
  headmap_db = []
  $.getJSON('/all-accidents', function(json1) {
      $.each(json1, function(key, data) {
        var geo = data.acc_location.split(',')
        headmap_db.push({location: new google.maps.LatLng(geo[0], geo[1]), weight: 0.8,radius:"200px"})
      });
  });

  //console.log(headmap_db)
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
    zoom: 13,
    mapTypeId: 'roadmap',
    styles: style
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: headmap_db
  });

  function getRadius(){
    var radius;
    var currentZoom = map.getZoom();
    if (currentZoom === 7){
        radius=2
    }
    else if (currentZoom === 8) {
        radius = 4;
    }
    else if (currentZoom === 9) {
        radius = 6;
    }
    else if (currentZoom === 10) {
        radius = 8;
    }
    else if (currentZoom === 11) {
        radius = 10;
    }
    else if (currentZoom === 12) {
        radius = 12;
    }
    else if (currentZoom === 13) {
        radius = 14;
    }
    else if (currentZoom === 14) {
        radius = 16;
    }
    else if (currentZoom === 15) {
        radius = 18;
    }
    else if (currentZoom === 16) {
        radius = 20;
    }
    else if (currentZoom === 17) {
        radius = 22;
    }
    else if (currentZoom === 18) {
        radius = 24;
    }
    else if (currentZoom > 18) {
      radius = 24;
    }
    return radius*5.5;
  }
  heatmap.setOptions({
      radius: 14*5.5,
  });
  heatmap.setMap(map);

  map.addListener('zoom_changed', function() {
      // zoom level changed... adjust heatmap layer options!
      heatmap.setOptions({
          radius: getRadius(),
      });
      // render the new options
      heatmap.setMap(map);
  });

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