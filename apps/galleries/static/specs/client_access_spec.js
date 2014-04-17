define(['jQuery', 'detectmobilebrowser', 'client_access'], function(jQuery, client_access) {

    describe("client_access", function() {

        it("should set jQuery.browser.mobile to true or false", function() {

            var has_mobile_property = jQuery.browser.mobile === true || jQuery.browser.mobile === false;

            expect(has_mobile_property).toBe(true);

        });
    });
});
