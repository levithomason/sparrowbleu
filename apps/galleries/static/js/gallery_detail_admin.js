/**
 * Drag and drop uploads
 */
var dropzone = $('#dropzone');
var hide_dropzone_timer;
var file_input = $('#image');
var file_list = file_input.prop('files');
var total_uploads = file_list.length;
var total_percent_uploaded = 0;
var current_upload;
var image_uploads = {};
var max_retries = 10;
// TODO: add the actual object pk at data-pk
var gallery_image_template =
    '<div class="gallery_image_item" data-pk="{{ image.pk }}">' +
        '<div class="gallery_image_item_inner">' +
            '<span class="favorite">' +
                '<i class="fa fa-heart-o"></i>' +
            '</span>' +
            '<div class="gallery_thumbnail_overlay"></div>' +
        '</div>' +
    '</div>'

// Dropzone
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

// File input
function updateFileList(callback) {
    file_list = $('#image').prop('files');
    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function updateTotalUploads() {
    total_uploads = file_list.length;
}

// Upload metrics
function initUploadMetrics(callback) {
    updateFileList(function() {
        total_uploads = file_list.length;
        current_upload = 1;
        updateTotalUploads();
        setImageUploads();

        if (typeof(callback) === 'function') {
            callback.call();
        }
    });
}
function setImageUploads(callback) {
    for (var i = 0; i < file_list.length; i++) {
        image_uploads[file_list[i].name] = {
            'name': file_list[i].name,
            'thumbnail_appended': false,
            'total': file_list[i].size,
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

// Amazon S3 upload
function s3_upload() {
    initUploadMetrics(function() {
        var s3upload = new S3Upload({
            gallery_id: $('#gallery_id').text(),
            file_dom_selector: 'image',
            s3_sign_put_url: '/s3-sign-upload/',

            onUploadStart: function() {
                console.log('Uploading ' + total_uploads + ' images.');
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
                 incrementCurrentUpload();
                // console.log('###');
                // console.log('Final Put: ' + file.name);
                // console.log(file);
                // console.log(image_uploads[file.name]);
                // console.log('###');
                // console.log(' ');
                imageUploadComplete(file, url);

                var retries = image_uploads[file.name].retries;
                var retry_string = '';
                if (retries < max_retries) {
                    retry_string = ' (' + (max_retries - retries) + ' retries)';
                }
                console.debug('Uploaded: ' + file.name + retry_string);

            },
            onError: function(file, status) {
                incrementCurrentUpload();
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
    // var total = 0;
    // var uploaded = 0;
    total_percent_uploaded = 0;

    for (var image in image_uploads) {
        //total += image_uploads[image].total;
        //uploaded += image_uploads[image].uploaded;

        total_percent_uploaded += (image_uploads[image].percent_uploaded() / total_uploads);
        // console.log(image_uploads[image].uploaded + ' | ' + image_uploads[image].total + ' | ' + image_uploads[image].name);
    }

    total_percent_uploaded = Math.ceil(total_percent_uploaded * 100) / 100;
    // console.log('--------------------------------------');
    // console.log('Total: ' + total_percent_uploaded + '%');
    //// console.log(uploaded + ' | ' + total + ' | ' + total_percent_uploaded);
    // console.log('');

    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function imageUploadComplete(file, url) {
    $('#' + safeString(file.name) + '.uploading').removeClass('uploading');
}

function appendGalleryThumbnail(file) {
    thumbDimension(file, 240, false, function(thumbnail) {

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