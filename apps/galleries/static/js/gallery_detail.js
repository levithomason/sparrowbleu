/*
 * Isotope
 */
var runIsotope = function() {
    /**
     var container = $('.gallery_image_container');

     container.isotope({
        itemSelector: '.gallery_image_item',
        layoutMode: 'cellsByRow',
        cellsByRow: {
            columnWidth: 360,
            rowHeight: 360
        }
     });
     */
};

$(window).load(function(){
     runIsotope();
});

/**
 * Selecting images
 */
$(document).ready(function() {

    // Selecting images
    $('.gallery_image_item').click(function() {
        var ele = $(this);
        var image_pk = ele.data('pk');
        var thumb_overlay = ele.find('.gallery_thumbnail_overlay')

        thumb_overlay.show();
        thumb_overlay.fadeOut(400);

        var jqxhr = $.post('/toggle-select-gallery-image/', {'image_pk': image_pk}, function() {
            if (jqxhr.responseText == "True") {
                ele.addClass('selected');
            } else {
                ele.removeClass('selected');
            }

            update_selected_images();
        })
            .fail(function() {
                alert(
                "Oops, couldn't change that image.  If this keeps happening, please contact SparrowBleu"
                );
            });

    });

    // Selected images widget
    function update_selected_images() {
        var widget_included = $('#selected_images .included');
        var widget_extra = $('#selected_images .extra');
        var max = widget_included.data('max');
        var current = $('.gallery_image_item.selected').length;
        var cost_per_extra_image = $('#cost_per_extra_image').data('cost');

        var remaining;
        var extra;
        var extra_text;

        // update remaining images, min of 0
        if (current <= max) {
            remaining = max - current;
        } else {
            remaining = 0;
        }

        // update images extra
        if (current > max) {
            extra = Math.abs(max - current);
        } else {
            extra = 0;
        }

        // update the widget readout
        if (extra > 0) {
            extra_text = extra + " extra = $" + extra * cost_per_extra_image;

            widget_included.removeClass('primary');

            if (!widget_extra.hasClass('primary')) {
                widget_extra.addClass('primary');
            }

        } else {
            extra_text = extra + " extra";

            widget_extra.removeClass('primary');

            if (!widget_included.hasClass('primary')) {
                widget_included.addClass('primary');
            }
        }

        widget_included.text( remaining + " remaining");
        widget_extra.text(extra_text);

    }
    update_selected_images();
});


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

        // image uploads object
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
    });
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
                var retries = imageUploads[file.name].retries;

                incrementCurrentUpload();

                if (retries > 0) {
                    this.uploadFile(file);
                    imageUploads[file.name].retries -= 1;
                    $('.gallery_image_container').append('<div class="text-warning">Retry #' + (max_retries - retries) + ': ' + file.name + '</div>');
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