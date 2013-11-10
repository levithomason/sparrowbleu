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
        var widget_at_cost = $('#selected_images .extra');
        var max = widget_included.data('max');
        var current = $('.gallery_image_item.selected').length;
        var cost_per_extra_image = $('#cost_per_extra_image').data('cost');

        var remaining;
        var extra;
        var at_cost_text;

        // update remaining images, min of 0
        if (current <= max) {
            remaining = max - current;
        } else {
            remaining = 0;
        }

        // update images extra
        if (current > max) {
            extra = Math.abs(max - current);
        } else {
            extra = 0;
        }

        // update the widget readout
        if (extra > 0) {
            at_cost_text = extra + " extra = $" + extra * cost_per_extra_image;
        } else {
            at_cost_text = extra + " extra";
        }

        widget_included.text( remaining + " remaining");
        widget_at_cost.text(at_cost_text);

    }
    update_selected_images();

});

