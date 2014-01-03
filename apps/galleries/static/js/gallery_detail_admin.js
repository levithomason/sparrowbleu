/**
 * Drag and drop uploads
 */
var dropzone = $('#dropzone');
var hideDropzoneTimer;
var fileInput = $('#image');
var fileList = fileInput.prop('files');
var total_uploads = fileList.length;
var total_percent_uploaded = 0;
var current_upload;
var imageUploads = {};
var max_retries = 10;

// Dropzone
function showDropzone() {
    dropzone.show();
    window.clearTimeout(hideDropzoneTimer);
}
function hideDropzone() {
    hideDropzoneTimer = window.setTimeout(function() {
        dropzone.fadeOut(100);
    });
}
function transferFilesToFileInput(files) {
    fileInput.prop('files', files);
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
    fileList = $('#image').prop('files');
    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function updateTotalUploads() {
    total_uploads = fileList.length;
}

// Upload metrics
function initUploadMetrics(callback) {
    updateFileList(function() {
        total_uploads = fileList.length;
        current_upload = 1;
        updateTotalUploads();
        setImageUploads();

        if (typeof(callback) === 'function') {
            callback.call();
        }
    });
}
function setImageUploads(callback) {
    for (var i = 0; i < fileList.length; i++) {
        imageUploads[fileList[i].name] = {
            'name': fileList[i].name,
            'total': fileList[i].size,
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
    if (typeof(imageUploads[name]) !== 'undefined') {
        // console.log(name + " (" + imageUploads[name].percent_uploaded() + ")");
        imageUploads[name].uploaded = loaded;
    }
    console.log('(+' + loaded + ' ' + name + ')');
    for (data in imageUploads) {
        console.log(imageUploads[data].uploaded + ' | ' + imageUploads[data].total + ' | ' + imageUploads[data].name);
    }
    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function resetImageUploadData(name) {
    if (typeof(imageUploads[name]) !== 'undefined') {
        imageUploads[name].uploaded = 0;
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
                console.log('Upload Started');
            },
            onProgress: function(file, loaded) {
                updateImageUploadData(file.name, loaded, function() {
                    updateTotalPercentUploaded(function() {
                        updateProgressBar();
                    });
                });
            },
            onFinishS3Put: function(file, url) {
                /**
                 // update the image uploaded to 100% as there is no on progress event for the final put
                 updateImageUploadData(file.name, (imageUploads[file.name].total - imageUploads[file.name].uploaded), function() {
                    updateTotalPercentUploaded(function() {
                        updateProgressBar();
                    });
                });
                 incrementCurrentUpload();
                 */
                console.log('###');
                console.log('Final Put: ' + file.name);
                console.log(file);
                console.log(imageUploads[file.name]);
                console.log('###');
                console.log(' ');
                appendGalleryImage(file, url);
            },
            onError: function(file, status) {
                incrementCurrentUpload();
                resetImageUploadData(file.name);
                if (imageUploads[file.name].retries > 0) {
                    this.uploadFile(file);
                    imageUploads[file.name].retries -= 1;
                    $('.gallery_image_container').append('<div class="text-warning">Retry ' + (max_retries - imageUploads[file.name].retries) + ': ' + file.name + '</div>');
                } else {
                    $('.gallery_image_container').append('<div class="text-danger">' + status + ': ' + file.name + '</div>');
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
    var total = 0;
    var uploaded = 0;
    total_percent_uploaded = 0;

    for (var image in imageUploads) {
        total += imageUploads[image].total;
        uploaded += imageUploads[image].uploaded;

        total_percent_uploaded += (imageUploads[image].percent_uploaded() / total_uploads);
    }

    total_percent_uploaded = Math.ceil(total_percent_uploaded * 100) / 100;
    console.log('--------------------------------------');
    console.log(uploaded + ' | ' + total + ' | ' + total_percent_uploaded);
    console.log('');

    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function appendGalleryImage(file, url) {
    var retries = imageUploads[file.name].retries;
    var retry_string = '';
    if (retries < max_retries) {
        retry_string = '(retries: ' + (max_retries - retries) + ')';
    }
    $('.gallery_image_container').append('<div><a target="_blank" href="' + url + '"> ' + file.name + ' ' + retry_string + '</a></div>');
    /*
     '<div class="gallery_image_item" data-pk="{{ image.pk }}">' +
     '<div class="gallery_image_item_inner">' +
     '<img class="gallery_thumbnail" src="' + image_url + '">' +
     '<span class="favorite">' +
     '<i class="fa fa-heart-o"></i>' +
     '</span>' +
     '<div class="gallery_thumbnail_overlay"></div>' +
     '</div>' +
     '</div>'
     );
     */
}
