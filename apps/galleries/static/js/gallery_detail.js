"use strict";

// Selected images widget
function update_selected_images() {
    var widget_selected = $('.selected_images .selected'),
        widget_extra = $('.selected_images .extra'),
        max = widget_selected.data('max'),
        selected = $('.gallery_image_item.selected').length,
        cost_per_extra_image = $('#cost_per_extra_image').data('cost'),
        extra,
        extra_text;

    // update selected images, min of 0
    if (selected > max) {
        extra = Math.abs(selected - max);
        selected = max;
    } else {
        extra = 0;
    }

    // update the widget readout
    if (extra > 0) {
        extra_text = extra + " extra = $" + extra * cost_per_extra_image;

        widget_selected.removeClass('primary');

        if (!widget_extra.hasClass('primary')) {
            widget_extra.addClass('primary');
        }

    } else {
        extra_text = extra + " extra";

        widget_extra.removeClass('primary');

        if (!widget_selected.hasClass('primary')) {
            widget_selected.addClass('primary');
        }
    }

    widget_selected.text(selected + " selected");
    widget_extra.text(extra_text);
}


function selectImage(image_element) {
    var ele = $(image_element),
        image_pk = ele.data('pk'),
        thumb_overlay = ele.find('.gallery_thumbnail_overlay'),
        these_images = $('[data-pk="' + image_pk + '"]'),
        jqxhr;

    thumb_overlay.show();
    thumb_overlay.fadeOut(400);

    jqxhr = $.post('/toggle-select-gallery-image/', {'image_pk': image_pk}, function() {
        if (jqxhr.responseText === "True") {
            these_images.addClass('selected');
        } else {
            these_images.removeClass('selected');
        }

        update_selected_images();
    })
        .fail(function() {
            alert(
                "Oops, couldn't change that image.  If this keeps happening, please contact SparrowBleu"
            );
        });
}

var fullscreen = {
    'image_container': $('.fullscreen_view .image_container'),
    'first_image': null,
    'last_image': null,
    'previous_element': $('.fullscreen_view .controls .previous'),
    'next_element': $('.fullscreen_view .controls .next'),
    'currentImageIndex': null,
    'next': function() {
        var current = fullscreen.image_container.children('.active'),
            next = current.next();

        current.removeClass('active');

        if (next.length) {
            next.addClass('active');
        } else {
            fullscreen.first_image.addClass('active');
        }
    },
    'previous': function() {
        var current = fullscreen.image_container.children('.active'),
            previous = current.prev();

        current.removeClass('active');

        if (previous.length) {
            previous.addClass('active');
        } else {
            fullscreen.last_image.addClass('active');
        }
    },
    'init': function() {

        fullscreen.first_image = $('.fullscreen_view .image_container .fullscreen_image_item:first-child');
        fullscreen.last_image = $('.fullscreen_view .image_container .fullscreen_image_item:last-child');

        fullscreen.first_image.addClass('active');
        fullscreen.currentImageIndex = 0;

        // controls
        $('body').on('keydown', function(e) {

            if ($('body').hasClass('fullscreen')) {
                // left
                if (e.keyCode === 37) {
                    fullscreen.previous();
                }

                // right
                if (e.keyCode === 39) {
                    fullscreen.next();
                }

                // space || enter
                if (e.keyCode === 32 || e.keyCode === 13) {
                    selectImage($('.fullscreen_view .image_container .fullscreen_image_item.active'));
                }
            }
        });
    }
};


$(document).ready(function() {

    // Image size controls
    $('.controls .thumbnails').click(function() {
        $('body')
            .removeClass('fullscreen')
            .addClass('thumbnails');

        // swap controls
        $('.controls .thumbnails').hide();
        $('.controls .fullscreen').show();

        // show all images, show view favs control
        $('.controls .view_all').hide();
        $('.controls .view_selected').show();
        $('.gallery_image_container').find('.gallery_image_item:not(.selected)').fadeIn();

        $('.fullscreen_view').fadeOut();
        $('.gallery_image_container').find('.gallery_image_item').fadeIn();
    });
    $('.controls .fullscreen').click(function() {
        $('body')
            .removeClass('thumbnails')
            .addClass('fullscreen');

        // swap controls
        $('.controls .fullscreen').hide();
        $('.controls .thumbnails').show();

        // hide fav controls
        $('.controls .view_all').hide();
        $('.controls .view_selected').hide();

        $('.fullscreen_view').fadeIn();
        $('.gallery_image_container').find('.gallery_image_item').fadeOut();
    });

    $('.controls .view_all').click(function() {
        $('body')
            .removeClass('view_selected')
            .addClass('view_all');

        // swap controls
        $('.controls .view_all').hide();
        $('.controls .view_selected').show();

        // show non selected
        $('.gallery_image_container').find('.gallery_image_item:not(.selected)').fadeIn();
    });
    $('.controls .view_selected').click(function() {
        $('body')
            .removeClass('view_all')
            .addClass('view_selected');

        // swap controls
        $('.controls .view_selected').hide();
        $('.controls .view_all').show();

        // hide non selected
        $('.gallery_image_container').find('.gallery_image_item:not(.selected)').fadeOut();
    });

    // Selecting images
    $('.gallery_image_item').click(function() {
        selectImage(this);
    });

    $('.fullscreen_image_item').click(function() {
        selectImage(this);
    });


    // Init
    function init() {
        update_selected_images();

        $('.controls .view_all').hide();
        $('.controls .thumbnails').hide();

        $('.fullscreen_view').hide();

        fullscreen.init();
    }
    init();

});
