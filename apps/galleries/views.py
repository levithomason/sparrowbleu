import os
import base64
import hmac
import json
import hashlib
import urllib
import time
from django.http import HttpResponse
from django.shortcuts import render, redirect

from sorl.thumbnail import get_thumbnail

from apps.galleries.models import Gallery, GalleryImage
from apps.galleries.forms import GalleryForm, GalleryImageForm, ClientAccessForm


def galleries(request):
    if not request.user.is_authenticated():
        return redirect('/')
    
    galleries = []

    for gallery in Gallery.objects.all().order_by('name'):
        try:
            preview_image = GalleryImage.objects.get(gallery=gallery, is_preview_image=True)
            preview_image_thumbnail = get_thumbnail(preview_image.image, '500x500', crop='center', quality=99).url
            gallery_empty = False
        except GalleryImage.DoesNotExist:
            preview_image_thumbnail = ""
            gallery_empty = True

        selected_images = gallery.selected_images()
        if selected_images > gallery.number_of_images:
            total_cost = (selected_images - gallery.number_of_images) * gallery.cost_per_extra_image
        else:
            total_cost = 0

        galleries.append([gallery, preview_image_thumbnail, gallery_empty, selected_images, total_cost])

    return render(request, 'galleries.html', {
      'galleries': galleries
    })


def create_gallery(request):
    if not request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        form = GalleryForm(request.POST or None)
        errors = []

        if form.is_valid():

            name = form.cleaned_data['name']
            passcode = form.cleaned_data['passcode']
            number_of_images = form.cleaned_data['number_of_images']
            cost_per_extra_image = form.cleaned_data['cost_per_extra_image']

            try:
                gallery = Gallery.objects.get(passcode=passcode)
                errors.append('Gallery "%s" already has passcode "%s".' % (gallery, passcode))

                return render(request, 'create_edit_gallery.html', {'form': form, 'errors': errors})

            except Gallery.DoesNotExist:

                gallery = Gallery(name=name, passcode=passcode, number_of_images=number_of_images, cost_per_extra_image=cost_per_extra_image)
                gallery.save()

                return redirect('/gallery/%s/%s' % (gallery.pk, passcode))
        
        return render(request, 'create_edit_gallery.html', {'form': form, 'errors': errors})
    
    form = GalleryForm()
    return render(request, 'create_edit_gallery.html', {'form': form})


def edit_gallery(request, pk):
    if not request.user.is_authenticated():
        return redirect('/')

    if request.method == 'GET':
        try:
            gallery = Gallery.objects.get(pk=pk)
            form = {
                'name': {
                    'value': gallery.name,
                },
                'passcode': {
                    'value': gallery.passcode,
                },
                'number_of_images': {
                    'value': gallery.number_of_images,
                },
                'cost_per_extra_image': {
                    'value': gallery.cost_per_extra_image,
                },
            }

            return render(request, 'create_edit_gallery.html', {'gallery': gallery, 'form': form, 'editing': True})

        except Gallery.DoesNotExist:
            errors = []
            errors.append('Gallery ID %s could not be found' % pk)

            return render(request, 'create_edit_gallery.html', {'errors': errors})

    if request.method == 'POST':
        form = GalleryForm(request.POST or None)
        errors = []

        try:
            gallery = Gallery.objects.get(pk=pk)

            if form.is_valid():
                name = form.cleaned_data['name']
                passcode = form.cleaned_data['passcode']
                number_of_images = form.cleaned_data['number_of_images']
                cost_per_extra_image = form.cleaned_data['cost_per_extra_image']

                # make sure there isn't a different gallery with the edited passcode
                try:
                    duplicate = Gallery.objects.get(passcode=passcode)

                    if duplicate.pk != gallery.pk:
                        form = {
                            'name': {
                                'value': gallery.name,
                            },
                            'passcode': {
                                'value': duplicate.passcode,
                                'errors': ['%s\'s passcode is already "%s"' % (duplicate.name, duplicate.passcode)]
                            },
                            'number_of_images': {
                                'value': gallery.number_of_images,
                            },
                            'cost_per_extra_image': {
                                'value': gallery.cost_per_extra_image,
                            },
                        }
                        return render(request, 'create_edit_gallery.html', {'gallery': gallery, 'form': form, 'editing': True})

                except Gallery.DoesNotExist:
                    pass

                gallery.name = name
                gallery.passcode = passcode
                gallery.number_of_images = number_of_images
                gallery.cost_per_extra_image = cost_per_extra_image
                gallery.save()
                return redirect('/galleries/')

            return render(request, 'create_edit_gallery.html', {'gallery': gallery, 'form': form, 'editing': True})

        except Gallery.DoesNotExist:
            errors.append("Sorry, couldn't find a Gallery with id %s." % pk)
            return render(request, 'create_edit_gallery.html', {'form': form, 'errors': errors, 'editing': True})


def delete_gallery(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            gallery_pk = request.POST.get('gallery_pk')
            gallery = Gallery.objects.get(pk=gallery_pk)

            gallery.delete()

            return HttpResponse(content="Image deleted successfully", content_type=None, status=200)

        except Gallery.DoesNotExist:

            return HttpResponse(content="Sorry, couldn't find that gallery!", content_type=None, status=400)


def gallery_detail(request, pk=None, passcode=None):
    if pk is None or passcode is None:
        return redirect('/galleries/')
    else:
        try:
            gallery = Gallery.objects.get(pk=pk)
            gallery_images_qs = GalleryImage.objects.order_by('-is_selected').filter(gallery=pk)
            gallery_images = []

            for image_object in gallery_images_qs:

                image = GalleryImage.objects.get(pk=image_object.pk).image

                # landscape/portrait thumbs
                if image.width > image.height:
                    #thumb_large = get_thumbnail(image, "960x480", quality=80)
                    thumb_small = get_thumbnail(image, "320x240", quality=80)
                else:
                    #thumb_large = get_thumbnail(image, "480x960", quality=80)
                    thumb_small = get_thumbnail(image, "240x320", quality=80)

                gallery_image = {
                    "pk": image_object.pk,
                    "is_selected": image_object.is_selected,
                    #"thumb_large": thumb_large.url,
                    "thumb_small": thumb_small.url
                }
                gallery_images.append(gallery_image)

            return render(request, 'gallery_detail.html', {
                'gallery': gallery,
                'gallery_images': gallery_images
            })

        except Gallery.DoesNotExist:
            return redirect('/galleries/')


def create_gallery_image(request):
    debug = []
    debug.append('checking method...')
    if request.method == 'POST':
        debug.append('method is post')
        form = GalleryImageForm(request.POST, request.FILES)
        gallery = Gallery.objects.get(pk=request.POST['gallery'])
        debug.append('gallery is ' + str(gallery))

        debug.append('checking form valid...')
        if form.is_valid():

            counter = 0
            for image_file in request.FILES.getlist('images'):
                is_first_gallery_image = (gallery.galleryimage_set.count() == 0 and counter == 0)
                
                new_image = GalleryImage.objects.create(gallery=gallery)
                
                if is_first_gallery_image:
                    new_image.is_preview_image = True
                    
                new_image.image.save(image_file.name, image_file)
                counter += 1

            return redirect('/gallery/%s/%s' % (gallery.pk, gallery.passcode))
            
        else:
            debug.append('form is invalid')
            return render(request, 'gallery_image_failed.html', {'form': form, 'gallery': gallery, 'debug': debug})
    
    form = GalleryImageForm()
    return render(request, 'gallery_detail.html', {'form': form, 'debug': debug})


def s3_sign_upload(request):
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    S3_BUCKET = os.environ['S3_BUCKET']

    object_name = request.GET.__getitem__('s3_object_name')
    mime_type = request.GET.__getitem__('s3_object_type')

    expires = int(time.time() + 1000)
    amz_headers = "x-amz-acl:public-read"

    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, hashlib.sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

    print "returning json"
    data = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (
            url, AWS_ACCESS_KEY, expires, signature),
        'url': url
    })

    return HttpResponse(data, mimetype='application/json')


def toggle_select_gallery_image(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            image_pk = request.POST.get('image_pk')
            image = GalleryImage.objects.get(pk=image_pk)

            image.is_selected = not image.is_selected
            image.save()

            return HttpResponse(content=image.is_selected, content_type=None, status=200)

        except GalleryImage.DoesNotExist:

            return HttpResponse(content="Could find image.", content_type=None, status=400)


def client_access(request):
    if request.method == 'POST':
        form = ClientAccessForm(request.POST or None)
        
        if form.is_valid():
            passcode = form.cleaned_data['passcode']

            try:
                gallery = Gallery.objects.get(passcode=passcode)
                return redirect('/gallery/%s/%s' % (gallery.pk, passcode))

            except Gallery.DoesNotExist:
                return render(request, 'client_access.html', {
                    'gallery_does_not_exist': True,
                    'passcode': passcode
                })

    return render(request, 'client_access.html', locals())
