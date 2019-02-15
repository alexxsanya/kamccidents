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