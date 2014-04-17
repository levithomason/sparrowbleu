require(['jQuery'], function(jQuery) {

    /**
     * Delete gallery
     */

    // delete
    jQuery('.delete').click(function() {
        var gallery = jQuery(this).parents('.gallery_list_item');

        gallery.find('.edit_delete').hide();
        gallery.find('.delete_confirm').show();
        gallery.find('.controls').css({"top": "0"});
    });


    // confirm
    jQuery('.confirm_delete_yes').click(function() {
        var gallery = jQuery(this).parents('.gallery_list_item');
        var gallery_pk = gallery.data('pk');

        gallery.addClass('deleting');

        var jqxhr = jQuery.post('/delete-gallery/', {'gallery_pk': gallery_pk}, function() {
            gallery.fadeOut(200);
        })
            .fail(function() {
                alert(jqxhr.responseText);
                gallery.removeClass('deleting');
            });
    });

    // cancel
    jQuery('.confirm_delete_no').click(function() {
        var gallery = jQuery(this).parents('.gallery_list_item');

        gallery.find('.edit_delete').show();
        gallery.find('.delete_confirm').hide();
        gallery.find('.controls').css({"top": ""});
    });

});
