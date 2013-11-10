/*
 * Delete gallery
 */

// delete
$('.delete').click(function() {
    $(this).hide();
    $(this).siblings('.delete_confirm').show()
    $(this).parents('.controls').css({"top": "0"});
});


// confirm delete
$('.confirm_delete_yes').click(function() {
    var gallery = $(this).parents('.gallery_list_item');
    var gallery_pk = gallery.data('pk');

    var jqxhr = $.post('/delete-gallery/', {'gallery_pk': gallery_pk}, function() {
        if (jqxhr.responseText = "Image deleted successfully") {
            gallery.fadeOut(200);
        }
    })
        .fail(function() {
            alert(
                "Oops, couldn't delete that gallery."
            );
        });
});

// cancel delete
$('.confirm_delete_no').click(function() {
    var delete_confirm = $(this).parent('.delete_confirm');

    delete_confirm.prev('.delete').show();
    delete_confirm.hide();

    $(this).parents('.controls').css({"top": ""});

});