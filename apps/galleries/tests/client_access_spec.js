describe("client_access", function() {

    var is_mobile = jQuery.browser.mobile;

    it("should set jQuery.browser.mobile to true or false: " + is_mobile, function() {

        var has_mobile_property = jQuery.browser.mobile === true || jQuery.browser.mobile === false;

        expect(has_mobile_property).toBe(true);

    });
});
