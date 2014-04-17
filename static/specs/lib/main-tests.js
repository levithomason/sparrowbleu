require.config({
    baseURL: '/static/js',
    urlArgs: 'cb=' + Math.random(),
    paths: {
        jQuery: 'jquery-1.10.2.min',
        spec: 'spec/'
    },
    shim: {
        jQuery: {
            exports: 'jQuery'
        },
        detectmobilebrowser: {
            deps: ['jQuery'],
            exports: 'detectmobilebrowser'
        },
        jasmine: {
            exports: 'jasmine'
        },
        'jasmine-html': {
            deps: ['jasmine'],
            exports: 'jasmine'
        },
        boot: {
            deps: ['jasmine', 'jasmine-html'],
            exports: 'jasmine'
        }
    }
});

// set global test vars here:

(function() {

    var specs = [
        '../specs/client_access_spec'
    ];

    require(specs, function() {
        window.executeTests();
    });

}());
