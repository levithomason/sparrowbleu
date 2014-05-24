"use strict";

jQuery(document).ready(function() {
    var view_is_fullscreen = false,
        view_selected_only = false,
        selected_images_count = jQuery('.selected_images .selected').data('selected');

    var fullscreen = {
        'image_container': jQuery('.fullscreen_view .image_container'),
        'images': jQuery('.fullscreen_image_item'),
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
                nextSelected = jQuery('.fullscreen_image_item.selected').first();
            }

            fullscreen.images.removeClass('active');
            nextSelected.addClass('active');
        },
        'init': function() {

            fullscreen.images.first().addClass('active');

            // controls
            jQuery('body').on('keydown', function(e) {

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
                        selectImage(jQuery('.fullscreen_image_item.active'));
                    }
                }
            });
        }
    };

    // Selected images widget
    function update_selected_images() {
        var widget_selected = jQuery('.selected_images .selected'),
            widget_extra = jQuery('.selected_images .extra'),
            summary_selected = jQuery('.summary .badge .selected'),
            summary_total = jQuery('.summary .badge .total'),
            max = widget_selected.data('max'),
            cost_per_extra_image = jQuery('#cost_per_extra_image').data('cost'),
            favs_count,
            extra_count,
            extra_text;

        // update selected images, min of 0
        if (selected_images_count > max) {
            extra_count = Math.abs(selected_images_count - max);
            favs_count = max;
        } else {
            extra_count = 0;
            favs_count = selected_images_count;
        }

        // update the widget readout
        if (extra_count > 0) {
            extra_text = extra_count + " extra = $" + extra_count * cost_per_extra_image;

            widget_selected.removeClass('primary');

            if (!widget_extra.hasClass('primary')) {
                widget_extra.addClass('primary');
            }

        } else {
            extra_text = extra_count + " extra";

            widget_extra.removeClass('primary');

            if (!widget_selected.hasClass('primary')) {
                widget_selected.addClass('primary');
            }
        }

        widget_selected.text(favs_count + " favs");
        widget_extra.text(extra_text);

        summary_selected.text(favs_count + extra_count);
        summary_total.text(extra_count * cost_per_extra_image);
    }


    function selectImage(image_element) {
        var ele = jQuery(image_element),
            image_pk = ele.data('pk'),
            thumb_overlay = ele.find('.gallery_thumbnail_overlay'),
            image = jQuery('[data-pk="' + image_pk + '"]'),
            jqxhr;

        thumb_overlay.show();
        thumb_overlay.fadeOut(400);
        image.toggleClass('selected');

        jqxhr = jQuery.post('/toggle-select-gallery-image/', {'image_pk': image_pk}, function() {
            if (jqxhr.responseText === "True") {
                image.addClass('selected');
                selected_images_count += 1;
            } else {
                image.removeClass('selected');
                selected_images_count -= 1;
            }

            update_selected_images();
        })
            .fail(function() {
                image.toggleClass('selected');
                alert(
                    "Oops, couldn't select that image.  Is your internet connection working?"
                );
            });
    }

    var updateGalleryView = function() {
        var fullscreen_view = jQuery('.fullscreen_view'),
            thumbnails_view = jQuery('.thumbnails_view'),
            fullscreen_btn = jQuery('.controls .fullscreen'),
            thumbnails_btn = jQuery('.controls .thumbnails'),
            view_all = jQuery('.controls .view_all'),
            view_selected = jQuery('.controls .view_selected'),
            not_selected_thumbnails = jQuery('.gallery_image_item:not(.selected)');

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
     Top Nav Controls
     */

    // thumbnails
    jQuery('.gallery_detail_nav .controls .thumbnails').on('tap', function() {
        view_is_fullscreen = false;
        updateGalleryView();
    });

    // fullscreen
    jQuery('.gallery_detail_nav .controls .fullscreen').on('tap', function() {
        view_is_fullscreen = true;
        updateGalleryView();
    });

    // view all
    jQuery('.gallery_detail_nav .controls .view_all').on('tap', function() {
        view_selected_only = false;
        updateGalleryView();
    });

    // view selected
    jQuery('.gallery_detail_nav .controls .view_selected').on('tap', function() {
        view_selected_only = true;
        updateGalleryView();
    });

    /*
     Pagination Controls
     */
    jQuery('.sbp_mobile_pagination .select_page').on('tap', function() {
        jQuery('.sbp_mobile_pagination .page_selector').toggle();
    });

    jQuery('.sbp_mobile_pagination .page_current').on('tap', function() {
        jQuery('.sbp_mobile_pagination .page_selector').hide();
    });

    jQuery('.sbp_mobile_pagination .page_selector').on('tap', function(e) {
        if (!e.target.hasClass('page_link')) {
            jQuery('.sbp_mobile_pagination .page_selector').hide();
        }
    });

    /*
     Selecting images
     */
    jQuery('.gallery_image_item').on('tap', function() {
        selectImage(this);
    });

    jQuery('.fullscreen_image_item').on('tap', function() {
        selectImage(this);
    });


    /*
     Init
     */
    update_selected_images();
    fullscreen.init();
});
