(function strict() {
    "use strict";

    $(document).ready(function() {

        // Selected images widget
        function update_selected_images() {
            var widget_included = $('#selected_images .included'),
                widget_extra = $('#selected_images .extra'),
                max = widget_included.data('max'),
                current = $('.gallery_image_item.selected').length,
                cost_per_extra_image = $('#cost_per_extra_image').data('cost'),
                remaining,
                extra,
                extra_text;

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
                extra_text = extra + " extra = $" + extra * cost_per_extra_image;

                widget_included.removeClass('primary');

                if (!widget_extra.hasClass('primary')) {
                    widget_extra.addClass('primary');
                }

            } else {
                extra_text = extra + " extra";

                widget_extra.removeClass('primary');

                if (!widget_included.hasClass('primary')) {
                    widget_included.addClass('primary');
                }
            }

            widget_included.text(remaining + " remaining");
            widget_extra.text(extra_text);

        }

        // Image size controls
        $('.controls .medium_thumbs').click(function() {
            $('.gallery_image_container')
                .removeClass('full_screen')
                .addClass('medium_thumbs');
        });
        $('.controls .full_screen').click(function() {
            $('.gallery_image_container')
                .removeClass('medium_thumbs')
                .addClass('full_screen');
        });

        // Selecting images
        $('.gallery_image_item').click(function() {
            var ele = $(this),
                image_pk = ele.data('pk'),
                thumb_overlay = ele.find('.gallery_thumbnail_overlay'),
                jqxhr;

            thumb_overlay.show();
            thumb_overlay.fadeOut(400);

            jqxhr = $.post('/toggle-select-gallery-image/', {'image_pk': image_pk}, function() {
                if (jqxhr.responseText === "True") {
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

        function init() {
            update_selected_images();
        }
    });

})();
