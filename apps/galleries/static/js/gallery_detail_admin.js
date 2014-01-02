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
    updateFileList();
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
function updateImageUpload(name, loaded) {
    if (typeof(imageUploads[name]) !== 'undefined') {
        console.log(name + " (" + imageUploads[name].percent_uploaded() + ")");
        imageUploads[name].uploaded = loaded;
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

            onProgress: function(file_name, loaded) {
                updateProgressBar();
                updateImageUpload(file_name, loaded);
            },
            onFinishS3Put: function(url, file_name) {
                incrementCurrentUpload();
                appendGalleryImage(url, file_name);
            },
            onError: function(file, status) {
                incrementCurrentUpload();

                if (imageUploads[file.name].retries > 0) {
                    this.uploadFile(file);
                    imageUploads[file.name].retries -= 1;
                    $('.gallery_image_container').append('<div class="text-warning">Retry #' + (max_retries - imageUploads[file.name].retries) + ': ' + file.name + '</div>');
                } else {
                    $('.gallery_image_container').append('<div class="text-danger">' + status + ': ' + file.name + '</div>');
                }
            }
        });
    });
}

// Visual feedback
function updateProgressBar() {
    updateTotalUploaded(function() {
        var progress = $('#status .progress');
        var bar = $('#status .progress-bar');

        if (total_percent_uploaded < 100) {
            progress.show();
            bar.css("width", total_percent_uploaded + "%");
        } else if (total_percent_uploaded === 100) {
            bar.css("width", '0%');
            progress.fadeOut(50);
        }
    })
}
function updateTotalUploaded(callback) {
    var total_data = 0;
    var total_data_uploaded = 0;

    for (var image in imageUploads) {
        total_data += imageUploads[image].total;
        total_data_uploaded += imageUploads[image].uploaded;
    }

    total_percent_uploaded = Math.ceil(total_data_uploaded / total_data * 10000) / 100;
    if (typeof(callback) === 'function') {
        callback.call();
    }
}
function appendGalleryImage(image_url, file_name) {
    var retries = imageUploads[file_name].retries;
    var retry_string = '';
    if (retries < max_retries) {
        retry_string = '(retries: ' + (max_retries - retries) + ')';
    }
    $('.gallery_image_container').append('<div><a target="_blank" href="' + image_url + '"> ' + file_name + ' ' + retry_string + '</a></div>');
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
