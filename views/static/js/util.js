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