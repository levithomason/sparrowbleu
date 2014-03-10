"use strict"

/**
 * Drag and drop uploads
 */
var dropzone = $('#dropzone');
var hide_dropzone_timer;
var file_input = $('#image');
var total_percent_uploaded = 0;
var image_uploads = {};
var current_upload;
var max_retries = 10;
var gallery_image_template =
    '<div class="gallery_image_item" data-pk="">' +
        '<div class="gallery_image_item_inner">' +
            '<span class="favorite">' +
                '<i class="fa fa-heart-o"></i>' +
            '</span>' +
            '<div class="gallery_thumbnail_overlay"></div>' +
        '</div>' +
    '</div>'


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
            'thumbnail_appended': false,
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
    // console.log('(+' + loaded + ' ' + name + ')');

    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function setImageUploadThumbnailAppended(file) {
    image_uploads[file.name].thumbnail_appended = true;
}
function resetImageUploadData(name) {
    if (typeof(image_uploads[name]) !== 'undefined') {
        image_uploads[name].uploaded = 0;
    }
}
function incrementCurrentUpload() {
    current_upload += 1;
}
function initUploadMetrics(callback) {
    current_upload = 1;
    setImageUploads();

    if (typeof(callback) === 'function') {
        callback.call();
    }
}



/**
 Amazon S3 upload
 */
function s3_upload() {
    initUploadMetrics(function() {
        var s3upload = new S3Upload({
            gallery_id: $('#gallery_id').text(),
            file_dom_selector: 'image',
            s3_sign_put_url: '/s3-sign-upload/',

            onUploadStart: function() {
                console.log('Uploading ' + file_input.prop('files').length + ' images.');
            },
            onProgress: function(file, loaded) {
                if (image_uploads[file.name].thumbnail_appended === false) {
                    setImageUploadThumbnailAppended(file);
                    appendGalleryThumbnail(file);
                }
                updateImageUploadData(file.name, loaded, function() {
                    updateTotalPercentUploaded(function() {
                        updateProgressBar();
                    });
                });
            },
            onFinishS3Put: function(file, url) {
                uploadImageToServer(file, url);

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




















// Visual feedback
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
function imageUploadComplete(file, pk) {
    $('#' + safeString(file.name))
        .removeClass('uploading')
        .removeAttr('id')
        .attr('data-pk', pk);

    incrementCurrentUpload();
}

function appendGalleryThumbnail(file) {
    thumbDimension(file, 320, false, function(thumbnail) {

        $('.gallery_image_container').append(gallery_image_template);

        $(thumbnail).addClass('gallery_thumbnail');

        $('.gallery_image_item').last()
            .attr('id', safeString(file.name))
            .addClass('uploading')
            .find('.gallery_image_item_inner')
                .prepend(thumbnail);
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

function uploadImageToServer(file, url) {
    $.ajax({
        url: "/create-gallery-image/",
        method: "POST",
        data: {
            gallery: $('#gallery_id').text(),
            amazon_s3_url: url
        },
        complete: function(data) {
            imageUploadComplete(file, data.responseText);
        }
    })
}
