/**
 * Creates an image thumbnail
 *
 * @param file     - a file api file object.
 * @param scale    - integer scale multiplier
 * @param callback - a function which receives the thumbnail
 *
 * Example:
 *   thumbnailer($('#image_input').prop('files')[0], 0.5, function(thumbnail) {
 *      doSomething(thumbnail);
 *   };
 */
function thumbScale(file, scale, callback) {
    readFile(file, function(dataURL) {

        createImage(dataURL, function(image) {

            createThumbnail.byScale(image, scale, function(thumb) {
                if (typeof(callback) === 'function') {
                    callback(thumb);
                }
            });
        });
    });
}

function thumbDimension(file, x, y, callback) {
    readFile(file, function(dataURL) {

        createImage(dataURL, function(image) {

            createThumbnail.byDimensions(image, x, y, function(thumb) {
                if (typeof(callback) === 'function') {
                    // console.log('thumb:');
                    // console.log(thumb);
                    callback(thumb);
                }
            });
        });
    });
}

/***********************************************************************************************************************
 * Utilities
 **********************************************************************************************************************/

/**
 * Generates a DataURL from a File API image file object
 *
 * @param file                - a file api file object.
 * @param callback (optional) - a function which receives the read file
 *
 * Example:
 *   readFile($('#image_input').prop('files')[0], function(file) {
 *      doSomething(file);
 *   };
 */
function readFile(file, callback) {
    if (file.hasOwnProperty('type') && file.type.match('image/').length) {
        var reader = new FileReader();
        // console.log('reading the file returns undefined here:  why???');
        reader.readAsDataURL(file);

        reader.onload = function(e) {
            var DataURL = e.target.result;

            if (typeof(callback) === 'function') {
                callback(DataURL);
            }
        };

    } else {
        console.error('readFile() expected a File API Object but received "' + typeof(file) + '".')
    }
}

/**
 * Creates an image element from a DataURL
 *
 * @param dataURL             - a base64 encoded image file
 * @param callback (optional) - a function which receives the image element
 *
 * Example:
 *   createImage(someDataURL, function(imageElement) {
 *      doSomething(imageElement);
 *   }
 */
function createImage(dataURL, callback) {
    var img = new Image();
    img.src = dataURL;

    img.onload = function() {
        if (typeof(callback) === 'function') {
            callback(img);
        }
    };
}

// TODO: doc this properly, maybe break it up or reorganize this whole js file to be better name spaced
var createThumbnail = {
    /**
     * Creates a canvas property if it does not yet exist
     *
     * @param callback
     */
    'withCanvas': function(callback) {
        if (typeof(this.canvas) === 'undefined') {
            this.canvas = document.createElement("canvas");
        }
        if (typeof(callback) === 'function') {
            callback();
        }
    },
    /**
     * Creates a canvas thumbnail with specified scale
     * @param image     - a File API image file
     * @param scale     - an integer scale multiplier
     * @param callback  - a function which is passed the thumbnail
     */
    'byScale': function(image, scale, callback) {
        var root = this;

        this.withCanvas(function() {
            var canvas = root.canvas;
            canvas.width = image.width * scale;
            canvas.height = image.height * scale;

            canvas.getContext("2d").drawImage(image, 0, 0, canvas.width, canvas.height);

            if (typeof(callback) === 'function') {
                callback(canvas);
            }
        });
    },

    /**
     * Creates a canvas thumbnail with specified dimensions
     * @param image        - a File API image file
     * @param x            - an integer pixel width of the thumbnail
     * @param y (optional) - an integer pixel height of the thumbnail, aspect ratio retained if omitted
     * @param callback     - a function which is passed the thumbnail
     */
    'byDimensions': function(image, x, y, callback) {
        var canvas = document.createElement("canvas");
        canvas.width = x;
        canvas.height = y | (x / image.width) * image.height;

        canvas.getContext("2d").drawImage(image, 0, 0, canvas.width, canvas.height);

        if (typeof(callback) === 'function') {
            callback(canvas);
        }
    }
};
