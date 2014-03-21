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
        $('.controls .thumbnails').click(function() {
            $('body')
                .removeClass('fullscreen')
                .addClass('thumbnails');
            $('.fullscreen_view').fadeOut();
            $('.gallery_image_container').find('.gallery_image_item').fadeIn();
        });
        $('.controls .fullscreen').click(function() {
            $('body')
                .removeClass('thumbnails')
                .addClass('fullscreen');
            $('.fullscreen_view').fadeIn();
            $('.gallery_image_container').find('.gallery_image_item').fadeOut();
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

        function fullscreen() {
            var fullscreen_url_elements = $('#fullscreen_urls').find('.url'),
                fullscreen_urls = [],
                fullscreen_image = $('.fullscreen_view .image');

            for (var i = 0; i < fullscreen_url_elements.length; i++) {
                fullscreen_urls[i] = $(fullscreen_url_elements[i]).text();
            }

            fullscreen_image.attr('src', fullscreen_urls[0]);

            function nextFullscreen() {
                console.log(fullscreen_urls.indexOf());
            }
        }

        function init() {
            update_selected_images();
            $('.controls .thumbnails').click();
            fullscreen();
        }
        init();
    });
})();
