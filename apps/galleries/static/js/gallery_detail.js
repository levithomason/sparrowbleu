"use strict";

var view_is_fullscreen = false;
var view_selected_only = false;

// remove fullscreen on mobile
if (jQuery.browser.mobile) {
    $('.fullscreen_view').remove();
    $('.controls .fullscreen').remove();
}

// Selected images widget
function update_selected_images() {
    var widget_selected = $('.selected_images .selected'),
        widget_extra = $('.selected_images .extra'),
        summary_selected = $('.summary .badge .selected'),
        summary_total = $('.summary .badge .total'),
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

    widget_selected.text(selected + " favs");
    widget_extra.text(extra_text);

    summary_selected.text(selected + extra);
    summary_total.text(extra * cost_per_extra_image);
}


function selectImage(image_element) {
    var ele = $(image_element),
        image_pk = ele.data('pk'),
        thumb_overlay = ele.find('.gallery_thumbnail_overlay'),
        image = $('[data-pk="' + image_pk + '"]'),
        jqxhr;

    thumb_overlay.show();
    thumb_overlay.fadeOut(400);
    image.toggleClass('selected');


    jqxhr = $.post('/toggle-select-gallery-image/', {'image_pk': image_pk}, function() {
        if (jqxhr.responseText === "True") {
            image.addClass('selected');
        } else {
            image.removeClass('selected');
        }

        update_selected_images();
    })
        .fail(function() {
            image.removeClass('selected');
            alert(
                "Oops, couldn't change that image.  If this keeps happening, please contact SparrowBleu"
            );
        });
}

var fullscreen = {
    'image_container': $('.fullscreen_view .image_container'),
    'images': $('.fullscreen_image_item'),
    'currentImage': function() {
        return fullscreen.image_container.children('.active');
    },
    'showNext': function() {
        var nextImage;

        if (view_selected_only) {
            nextImage = fullscreen.currentImage().nextAll('.selected').first();

            if (!nextImage.length) {
                nextImage = fullscreen.images.filter('.selected').first();
            }
        } else {
            nextImage = fullscreen.currentImage().next();

            if (!nextImage.length) {
                nextImage = fullscreen.images.first();
            }
        }

        fullscreen.currentImage().removeClass('active');
        nextImage.addClass('active');
    },
    'showPrev': function() {
        var prevImage;

        if (view_selected_only) {
            prevImage = fullscreen.currentImage().prevAll('.selected').first();

            if (!prevImage.length) {
                prevImage = fullscreen.images.filter('.selected').last();
            }
        } else {
            prevImage = fullscreen.currentImage().prev();

            if (!prevImage.length) {
                prevImage = fullscreen.images.last();
            }
        }

        fullscreen.currentImage().removeClass('active');
        prevImage.addClass('active');
    },
    'showSelected': function() {
        var currentImage = fullscreen.image_container.children('.active'),
            nextSelected = currentImage.next('.selected');

        if (!nextSelected.length) {
            nextSelected = $('.fullscreen_image_item.selected').first();
        }

        fullscreen.images.removeClass('active');
        nextSelected.addClass('active');
    },
    'init': function() {

        fullscreen.images.first().addClass('active');

        // controls
        $('body').on('keydown', function(e) {

            if (view_is_fullscreen) {
                // left
                if (e.keyCode === 37) {
                    fullscreen.showPrev();
                }

                // right
                if (e.keyCode === 39) {
                    fullscreen.showNext();
                }

                // space || enter
                if (e.keyCode === 32 || e.keyCode === 13) {
                    selectImage($('.fullscreen_image_item.active'));
                }
            }
        });
    }
};


$(document).ready(function() {
    var updateGalleryView = function() {
        var fullscreen_view = $('.fullscreen_view'),
            thumbnails_view = $('.thumbnails_view'),
            fullscreen_btn = $('.controls .fullscreen'),
            thumbnails_btn = $('.controls .thumbnails'),
            view_all = $('.controls .view_all'),
            view_selected = $('.controls .view_selected'),
            not_selected_thumbnails = $('.gallery_image_item:not(.selected)');

        if (view_is_fullscreen) {
            thumbnails_view.addClass('hide');
            thumbnails_btn.removeClass('hide');

            fullscreen_view.removeClass('hide');
            fullscreen_btn.addClass('hide');

            if (view_selected_only) {
                view_selected.addClass('hide');
                view_all.removeClass('hide');
                fullscreen.showSelected();
            } else {
                view_selected.removeClass('hide');
                view_all.addClass('hide');
            }
        }

        if (!view_is_fullscreen) {
            thumbnails_view.removeClass('hide');
            thumbnails_btn.addClass('hide');

            fullscreen_view.addClass('hide');
            fullscreen_btn.removeClass('hide');

            if (view_selected_only) {
                not_selected_thumbnails.addClass('hide');
                view_selected.addClass('hide');
                view_all.removeClass('hide');
            } else {
                not_selected_thumbnails.removeClass('hide');
                view_selected.removeClass('hide');
                view_all.addClass('hide');
            }
        }

    };

    /*
      Controls
     */

    // thumbnails
    $('.controls .thumbnails').on('tap', function() {
        view_is_fullscreen = false;
        updateGalleryView();
    });

    // fullscreen
    $('.controls .fullscreen').on('tap', function() {
        view_is_fullscreen = true;
        updateGalleryView();
    });

    // view all
    $('.controls .view_all').on('tap', function() {
        view_selected_only = false;
        updateGalleryView();
    });

    // view selected
    $('.controls .view_selected').on('tap', function() {
        view_selected_only = true;
        updateGalleryView();
    });

    /*
     Selecting images
     */
    $('.gallery_image_item').on('tap', function() {
        selectImage(this);
    });

    $('.fullscreen_image_item').on('tap', function() {
        selectImage(this);
    });


    /*
     Init
     */
    update_selected_images();
    fullscreen.init();
});
