jQuery('input[name="is_mobile"]').prop('checked', isMobile.any);

$('[type="submit"]').on('click', function() {
    setTimeout(function() {
        $('[type="submit"]')
            .addClass('disabled')
            .attr("disabled", "disabled")
            .html('<i class="fa fa-spinner fa-spin"></i> Fetching');
    });
});
