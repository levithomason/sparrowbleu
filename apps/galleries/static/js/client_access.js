require(['jQuery', 'detectmobilebrowser'], function(jQuery) {

    jQuery('input[name="is_mobile"]').prop('checked', jQuery.browser.mobile);

});
