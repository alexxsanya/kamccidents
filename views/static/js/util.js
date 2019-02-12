function display_this(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        $(".photo-display").css("display","inline-table");

        reader.onload = function (e) {
            $('#accident_image')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function close_display(){
    $(".photo-display").css("display","none");
    console.log("clicked")
}

function pickCoordinates() {
    var output = $("#accident-address");
  
    if (!navigator.geolocation){
      output.value = "Geolocation is not supported by your browser";
      return;
    }
  
    function success(position) {
      var latitude  = position.coords.latitude;
      var longitude = position.coords.longitude;
      output.value = latitude + ',' + longitude;
    }
  
    function error() {
      output.value = "Unable to retrieve your location";
    }
  
    output.value = "Decoding…";
  
    navigator.geolocation.getCurrentPosition(success, error);
    
  }