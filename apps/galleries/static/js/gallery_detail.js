"use strict";

var fullscreen = {
    'image_element': $('.fullscreen_view .image_container .image'),
    'previous_element': $('.fullscreen_view .controls .previous'),
    'next_element': $('.fullscreen_view .controls .next'),
    'url_elements': $('#fullscreen_urls').find('.url'),
    'urls': [],
    'currentImageIndex': null,
    'next': function() {
        if (fullscreen.currentImageIndex === fullscreen.urls.length) {
            fullscreen.currentImageIndex = 0;
        } else {
            fullscreen.currentImageIndex += 1;
        }

        fullscreen.image_element.attr('src', fullscreen.urls[fullscreen.currentImageIndex]);
    },
    'previous': function() {
        if (fullscreen.currentImageIndex === 0) {
            fullscreen.currentImageIndex = fullscreen.urls.length;
        } else {
            fullscreen.currentImageIndex -= 1;
        }

        fullscreen.image_element.attr('src', fullscreen.urls[fullscreen.currentImageIndex]);
    },
    'init': function() {
        var urls = [],
            i;

        for (i = 0; i < fullscreen.url_elements.length; i++) {
            urls[i] = $(fullscreen.url_elements[i]).text();
        }

        fullscreen.urls = urls;
        fullscreen.currentImageIndex = 0;
        fullscreen.image_element.attr('src', fullscreen.urls[fullscreen.currentImageIndex]);
    }
};


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


    function init() {
        update_selected_images();
        $('.controls .thumbnails').click();
        fullscreen.init();
    }
    init();

});
