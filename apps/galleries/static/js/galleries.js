/*
 * Delete gallery
 */

// delete
$('.delete').click(function() {
    var gallery = $(this).parents('.gallery_list_item');

    gallery.find('.edit_delete').hide();
    gallery.find('.delete_confirm').show();
    gallery.find('.controls').css({"top": "0"});
});


// confirm delete
$('.confirm_delete_yes').click(function() {
    var gallery = $(this).parents('.gallery_list_item');
    var gallery_pk = gallery.data('pk');

    gallery.fadeOut(200);

    var jqxhr = $.post('/delete-gallery/', {'gallery_pk': gallery_pk}, function() {

    })
        .fail(function() {
            alert(jqxhr.responseText);
            gallery.fadeIn(200);
        });
});

// cancel delete
$('.confirm_delete_no').click(function() {
    var gallery = $(this).parents('.gallery_list_item');

    gallery.find('.edit_delete').show();
    gallery.find('.delete_confirm').hide();
    gallery.find('.controls').css({"top": ""});
});
