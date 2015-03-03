$(document).unload(function(){
    google.maps.Unload();
});

$(document).ready(function(){
    $("input.location_picker").each(function (i) {
        var me = $(this),
            wrap = $('<div>').insertBefore(me).addClass('location-picker-wrap'),
            mapDiv = $('<div>').appendTo(wrap).addClass('location-picker-map');
        
        me.prependTo(wrap);
        
        var lat = 27.7000;
        var lng = 85.3333;
        if (me.val().split(/,\s*/).length == 2) {
            values = this.value.split(',');
            lat = values[0];
            lng = values[1];
        }
        var center = new google.maps.LatLng(lat, lng);

        var map = new google.maps.Map(mapDiv[0], {
            zoom: 15,
            center: center,
            // scaleControl: false,
            // navigationControl: false,
            // navigationControlOptions: {
            //     position: google.maps.ControlPosition.RIGHT
            // },
            disableDefaultUI: false,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var marker = new google.maps.Marker({
            position: center,
            map: map
        });

        google.maps.event.addListener(map, 'click', function (e) {
            me.val(e.latLng.lat() + ',' + e.latLng.lng());
            marker.setPosition(e.latLng);
        });
        function update() {
            var bits = $(this).val().split(/,\s*/),
                latLng = new google.maps.LatLng(parseFloat(bits[0]), parseFloat(bits[1]));
            marker.setPosition(latLng);
            map.setCenter(latLng);
        }
        me.change(update);
        me.keyup(update);
    });
});

$.noConflict();
