"use strict"

/**
 * Drag and drop uploads
 */
var dropzone = $('#dropzone');
var hide_dropzone_timer;
var file_input = $('#image');
var total_percent_uploaded = 0;
var image_uploads = {};
var max_retries = 10;


/**
 Dropzone
 */
function showDropzone() {
    dropzone.show();
    window.clearTimeout(hide_dropzone_timer);
}
function hideDropzone() {
    hide_dropzone_timer = window.setTimeout(function() {
        dropzone.fadeOut(100);
    }, 50);
}
function transferFilesToFileInput(files) {
    file_input.prop('files', files);
}

$(window)
    .on('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        showDropzone();
    })
    .on('dragenter', function(e) {
        e.preventDefault();
        e.stopPropagation();

        showDropzone();
    })
    .on('dragleave', function(e) {
        hideDropzone();
    })
    .on('drop', function(e) {
        if (e.originalEvent.dataTransfer) {
            if (e.originalEvent.dataTransfer.files.length) {
                e.preventDefault();
                e.stopPropagation();

                hideDropzone();
                transferFilesToFileInput(e.originalEvent.dataTransfer.files);
            }
        }
    });


/**
 Upload metrics
 */
function setImageUploads(callback) {
    for (var i = 0; i < file_input.prop('files').length; i++) {
        image_uploads[file_input.prop('files')[i].name] = {
            'name': file_input.prop('files')[i].name,
            'total': file_input.prop('files')[i].size,
            'uploaded': 0,
            'percent_uploaded': function() {
                return Math.ceil(this.uploaded / this.total * 100);
            },
            'retries': max_retries
        };
    }
    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function updateImageUploadData(name, loaded, callback) {
    if (typeof(image_uploads[name]) !== 'undefined') {
        image_uploads[name].uploaded = loaded;
    }

    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function resetImageUploadData(name) {
    if (typeof(image_uploads[name]) !== 'undefined') {
        image_uploads[name].uploaded = 0;
    }
}


/**
 Amazon S3 upload
 */
function s3_upload() {
    setImageUploads(function() {
        var s3upload = new S3Upload({
            gallery_pk: $('#gallery_pk').data('pk'),
            file_dom_selector: 'image',
            s3_sign_put_url: '/s3-sign-upload/',

            onUploadStart: function() {
                console.log('Uploading ' + file_input.prop('files').length + ' images.');

                for (var upload in image_uploads) {
                    $('.files_uploading')
                        .fadeIn()
                        .append('<div class="upload" id="' + safeString(upload) + '"><i class="fa fa-cloud-upload"></i> ' + upload + '</div>');
                }
            },
            onProgress: function(file, loaded) {
                updateImageUploadData(file.name, loaded, function() {
                    updateTotalPercentUploaded(function() {
                        updateProgressBar();
                    });
                });
            },
            onFinishS3Put: function(file, url, object_name) {
                uploadImageToServer(file, url, object_name);

                var retries = image_uploads[file.name].retries;
                var retry_string = '';
                if (retries < max_retries) {
                    retry_string = ' (' + (max_retries - retries) + ' retries)';
                }
                console.debug('Uploaded: ' + file.name + retry_string);

            },
            onError: function(file, status) {
                resetImageUploadData(file.name);
                if (image_uploads[file.name].retries > 0) {
                    this.uploadFile(file);
                    image_uploads[file.name].retries -= 1;
                    console.warn('Retry ' + (max_retries - image_uploads[file.name].retries) + ': ' + file.name);
                } else {
                    console.error(status + ': ' + file.name);
                }
            }
        });
    });
}


/**
 Visual feedback
 */
function updateProgressBar() {
    var progress = $('#status .progress');
    var bar = $('#status .progress-bar');

    if (total_percent_uploaded < 100) {
        progress.show();
    } else if (total_percent_uploaded >= 100) {
        bar.css("width", "100%");
        window.setTimeout(function() {
            progress.fadeOut(200);
        }, 1000)
    }
    bar.css("width", total_percent_uploaded + "%");
}
function updateTotalPercentUploaded(callback) {
    total_percent_uploaded = 0;

    for (var image in image_uploads) {
        total_percent_uploaded += (image_uploads[image].percent_uploaded() / file_input.prop('files').length);
    }

    total_percent_uploaded = Math.ceil(total_percent_uploaded * 100) / 100;

    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function imageUploadComplete(file) {
    $('#' + safeString(file.name)).fadeOut(function() {
        this.remove();

        var uploads_remaining = $('.files_uploading').children('.upload');

        if (uploads_remaining.length === 0) {
            location.reload();
        }
    });
}

function safeString(string) {
    return string
        .replace(/[\/\\()~%'"*?<>{}\[\]; ]/g, "")
        .replace(/[@#$&:+,. ]/g, "-")
}


/**
 Upload to our server
 */

function uploadImageToServer(file, url, object_name) {
    var url_no_args = url.replace(/\?.*/, '');

    $('#' + safeString(file.name)).html('<i class="fa fa-spin fa-spinner"></i> making thumbnails');

    $.ajax({
        url: "/create-gallery-image/",
        method: "POST",
        data: {
            gallery: $('#gallery_pk').data('pk'),
            full_size_url: url_no_args,
            name: file.name,
            s3_object_name: object_name
        },
        complete: function(data) {
            imageUploadComplete(file);
        }
    })
}
