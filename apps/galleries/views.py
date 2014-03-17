import base64
import hmac
import json
import hashlib
import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
from apps.galleries.models import Gallery, GalleryImage
from apps.galleries.forms import GalleryForm, GalleryImageForm, ClientAccessForm
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, boto_bucket, boto_key
# sorl settings import required for sorl default to work properly
from sorl.thumbnail.conf import settings
from sorl.thumbnail import default, get_thumbnail


def galleries(request):
    if not request.user.is_authenticated():
        return redirect('/client-access')

    galleries = []

    for gallery in Gallery.objects.all().order_by('name'):
        has_images = GalleryImage.objects.all().filter(gallery=gallery).count() > 0
        if has_images:
            preview_image = GalleryImage.objects.all().filter(gallery=gallery)[0]
            thumb = get_thumbnail(preview_image.full_size_url, '250x250', quality=90, crop='center')
            preview_image_url = thumb.url
        else:
            preview_image_url = None

        selected_images = gallery.selected_images()

        if selected_images > gallery.number_of_images:
            total_cost = (selected_images - gallery.number_of_images) * gallery.cost_per_extra_image
        else:
            total_cost = 0

        galleries.append([gallery, preview_image_url, selected_images, total_cost])

    return render(request, 'galleries.html', {'galleries': galleries})


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
        gallery_pk = request.POST.get('gallery_pk')

        try:
            gallery = Gallery.objects.get(pk=gallery_pk)

            try:
                for key in boto_bucket.list(prefix=gallery.get_s3_directory_name()):
                    boto_key.key = key
                    key.delete()

                try:
                    gallery.delete()
                    default.kvstore.cleanup()

                    return HttpResponse(content="Gallery deleted successfully", content_type=None, status=200)

                except:
                    return HttpResponse(content="Couldn't delete gallery images", content_type=None, status=400)

            except:
                return HttpResponse(content="Could not delete S3 bucket for the gallery", content_type=None, status=400)

        except Gallery.DoesNotExist:
            return HttpResponse(content="Sorry, this gallery doesn't exist anymore.", content_type=None, status=400)


def gallery_detail(request, pk=None, passcode=None):
    if pk is None or passcode is None:
        return redirect('/galleries/')
    else:
        try:
            gallery = Gallery.objects.get(pk=pk)
            gallery_images = GalleryImage.objects.order_by('name').filter(gallery=pk)

            return render(request, 'gallery_detail.html', {
                'gallery': gallery,
                'gallery_images': gallery_images,
            })

        except Gallery.DoesNotExist:
            return redirect('/galleries/')


def create_gallery_image(request):
    if request.method == "POST":
        form = GalleryImageForm(request.POST)
        gallery = Gallery.objects.get(pk=request.POST['gallery'])
        full_size_url = request.POST['full_size_url']
        name = request.POST['name']

        if form.is_valid():
            new_image = GalleryImage.objects.create(full_size_url=full_size_url, gallery=gallery, name=name)
            new_image.save()

            return HttpResponse(content=new_image.pk, content_type=None, status=200)

        else:
            return HttpResponse(content="The request form is invalid:\n\n" + str(form.errors), content_type=None, status=400)


def s3_sign_upload(request):
    object_name = request.GET.get('s3_object_name')
    mime_type = request.GET.get('s3_object_type')

    expires = int(time.time() + 3600)
    amz_headers = "x-amz-acl:public-read"

    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, AWS_STORAGE_BUCKET_NAME, object_name)

    signature = base64.encodestring(hmac.new(AWS_SECRET_ACCESS_KEY, put_request, hashlib.sha1).digest())
    signature = signature.replace(' ', '%20').replace('+', '%2B')

    url = 'https://%s.s3.amazonaws.com/%s' % (AWS_STORAGE_BUCKET_NAME, object_name)

    data = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (
            url, AWS_ACCESS_KEY_ID, expires, signature),
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
