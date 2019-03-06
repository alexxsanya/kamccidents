function generateRoute() {

    var kampalaCity = new google.maps.LatLng(0.316644, 32.589536);
    
    var map = new google.maps.Map(document.getElementById('route-map'), {
      mapTypeControl: false,
      center: kampalaCity,
      zoom: 13
    });
  
    //new AutocompleteDirectionsHandler(map).route();
    
    origin = new google.maps.LatLng(0.291080391, 32.58045209)
    destination = new google.maps.LatLng(0.336644, 32.589536)
    new AutocompleteDirectionsHandler(map).generate(origin,destination);
  }
  
  /**
   * @constructor
   */
  function AutocompleteDirectionsHandler(map) {
    this.map = map;
    this.travelMode = 'WALKING';
    this.directionsService = new google.maps.DirectionsService;
    this.directionsDisplay = new google.maps.DirectionsRenderer;
    this.directionsDisplay.setMap(map);
  
    var modeSelector = document.getElementById('mode-selector');

    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
  }
  
  AutocompleteDirectionsHandler.prototype.route = function() {
    var me = this;
    
    var request = {
      origin:new google.maps.LatLng(0.291080391, 32.58045209),
      destination:new google.maps.LatLng(0.336644, 32.589536),
      travelMode: this.travelMode
      /*travelMode: google.maps.TravelMode.DRIVING,*/
      
    };

    this.directionsService.route(
        request,
        function(response, status) {
          if (status === 'OK') {
            me.directionsDisplay.setDirections(response);
            me.map.zoom = 13;
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
  };

  AutocompleteDirectionsHandler.prototype.generate = function(
      origin,
      destination
    ) {
    var me = this;
    var request = {
      origin:origin,
      destination:destination,
      travelMode: this.travelMode
      /*travelMode: google.maps.TravelMode.DRIVING,*/
      
    };

    this.directionsService.route(
        request,
        function(response, status) {
          if (status === 'OK') {
            me.directionsDisplay.setDirections(response);
            me.map.zoom = 13;
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
  };

  function geocodeLatLng() {
    
    var geocoder = new google.maps.Geocoder;
    //var input = document.getElementById('latlng').value;
    var input = '0.314069, 32.587187'
    var latlngStr = input.split(',', 2);
    var latlng = {lat: parseFloat(latlngStr[0]), lng: parseFloat(latlngStr[1])};
    geocoder.geocode({'location': latlng}, function(results, status) {
      if (status === 'OK') {
        if (results[0]) {
          console.log(results[0].formatted_address)
          return results[0].formatted_address
        } else {
          window.alert('No results found');
        }
      } else {
        window.alert('Geocoder failed due to: ' + status);
      }
    });
  }
