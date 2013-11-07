/*
 * Isotope
 */
 $(window).load(function(){

    $(function(){
        var $container = $('.gallery_image_container');

        $container.isotope({
            itemSelector: '.gallery_image_item',
            layoutMode: 'cellsByRow',
            cellsByRow: {
                columnWidth: 360,
                rowHeight: 360
            }
        });
    });

});


/*
 * CSRF for ajax requests
 */
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


/*
 * Selecting images
 */
$(document).ready(function() {

    $('.gallery_image_item').click(function() {
        var ele = $(this);
        var image_pk = ele.data('pk');

        // register the click as a success in the ui immediately
        ele.toggleClass('selected');

        if (ele.hasClass('selected')) {
            var thumb = ele.find('.gallery_thumbnail')
            thumb.hide();
            thumb.fadeIn(800);
        }

        console.log('post: ' + "/select_gallery_image/, " + image_pk);

        var jqxhr = $.post('/select_gallery_image/', {'image_pk': image_pk}, function() {
            console.log('it worked!');
        })
            .done(function() {
                console.log( "done" );
            })
            .fail(function() {
                ele.removeClass('selected');
                alert("Oops, couldn't select that image.  If this continues to happen contact SparrowBleu.")
            })
            .always(function() {
                console.log( "always" );
        });

        // Perform other work here ...

        // Set another completion function for the request above
        jqxhr.always(function() {
            console.log( "second always" );
        });
    });



});

