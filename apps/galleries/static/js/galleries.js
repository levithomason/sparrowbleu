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

    $.ajax('/delete-gallery/', {
        method: 'POST',
        data: {'gallery_pk': gallery_pk},
        success: function() {
            gallery.fadeOut(200);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Error: ' + errorThrown + '\n\n' + jqXHR.responseText);
            gallery.removeClass('deleting');
        }
    });
});

// cancel
jQuery('.confirm_delete_no').click(function() {
    var gallery = jQuery(this).parents('.gallery_list_item');

    gallery.find('.edit_delete').show();
    gallery.find('.delete_confirm').hide();
    gallery.find('.controls').css({"top": ""});
});
