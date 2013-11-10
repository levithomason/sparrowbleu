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

        var jqxhr = $.post('/toggle-select-gallery-image/', {'image_pk': image_pk}, function() {
            if (jqxhr.responseText == "True") {
                ele.addClass('selected');
            } else {
                ele.removeClass('selected');
            }

            update_selected_images();
        })
            .fail(function() {
                alert(
                "Oops, couldn't change that image.  If this keeps happening, please contact SparrowBleu"
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

