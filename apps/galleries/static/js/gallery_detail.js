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

    // Selecting images
    $('.gallery_image_item').click(function() {
        var ele = $(this);
        var image_pk = ele.data('pk');
        var thumb_overlay = ele.find('.gallery_thumbnail_overlay')

        thumb_overlay.show();
        thumb_overlay.fadeOut(400);

        var jqxhr = $.post('/toggle_select_gallery_image/', {'image_pk': image_pk}, function() {
            console.log(jqxhr.responseText);
            console.log(ele);
            if (jqxhr.responseText == "True") {
                ele.addClass('selected');
            } else {
                ele.removeClass('selected');
            }

            update_selected_images();
        })
            .fail(function() {
                alert(
                "Oops, couldn't change that image.  If this keeps happening, please contact SparrowBleu with this error:" +
                '\n\n' +
                jqxhr.responseText
                );
            });

    });

    // Selected images widget
    function update_selected_images() {
        var widget_included = $('#selected_images .included');
        var widget_at_cost = $('#selected_images .at_cost');
        var max = widget_included.data('max');
        var current = $('.gallery_image_item.selected').length;

        var remaining;
        var at_cost;
        var at_cost_text;

        // update remaining images, min of 0
        if (current <= max) {
            remaining = max - current;
        } else {
            remaining = 0;
        }

        // update images at_cost
        if (current > max) {
            at_cost = Math.abs(max - current);
        } else {
            at_cost = 0;
        }

        // update the widget readout
        if (at_cost > 0) {
            at_cost_text = at_cost + " extra = $" + at_cost * 20;
        } else {
            at_cost_text = at_cost + " extra";
        }

        widget_included.text( remaining + " remaining");
        widget_at_cost.text(at_cost_text);

    }
    update_selected_images();

});

