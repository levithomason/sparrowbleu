from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.files.uploadedfile import SimpleUploadedFile

from sorl.thumbnail import get_thumbnail

from apps.galleries.models import Gallery, GalleryImage
from apps.galleries.forms import GalleryForm, GalleryImageForm, ClientAccessForm
from apps.sparrow_bleu.views import get_form_errors


def galleries(request):
    if not request.user.is_authenticated():
        return redirect('/')
    
    galleries = []
    preview_image = None

    for gallery in Gallery.objects.all():
        try:
            preview_image = GalleryImage.objects.get(gallery=gallery, is_preview_image=True)
            preview_image_thumbnail = get_thumbnail(preview_image.image, '500x500', crop='center', quality=99).url
        except GalleryImage.DoesNotExist:
            preview_image_thumbnail = None
        
        galleries.append([gallery, preview_image_thumbnail])
    
    gallery_empty = True
    for (gallery, image) in galleries:
        gallery_empty = image == None
    
    return render(request, 'galleries.html', {
      'galleries': galleries,
      'gallery_empty': gallery_empty,
    })


def new_gallery(request):
    if not request.user.is_authenticated():
        return redirect('/')
    
    if request.method == 'POST':
        form = GalleryForm(request.POST or None)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            passcode = form.cleaned_data['passcode']
            number_of_images = form.cleaned_data['number_of_images']
            
            gallery = Gallery(name=name, passcode=passcode, number_of_images=number_of_images)
            gallery.save()
            
            return redirect('/gallery/' + str(gallery.pk))
        
        errors = get_form_errors(form)
        return render(request, 'new_gallery.html', {'form': form, 'errors': errors})
    
    form = GalleryForm()
    return render(request, 'new_gallery.html', {'form': form})


def gallery_detail(request, pk=None, passcode=None):
    if pk is None or passcode is None:
        return redirect('/galleries/')
    else:
        try:
            gallery = Gallery.objects.get(pk=pk)
            gallery_images_qs = GalleryImage.objects.filter(gallery=pk)
            gallery_images = []

            for image_object in gallery_images_qs:

                image = GalleryImage.objects.get(pk=image_object.pk).image

                # landscape/portrait thumbs
                if image.width > image.height:
                    thumb_large = get_thumbnail(image, "960x480", quality=99)
                    thumb_small = get_thumbnail(image, "320x240", quality=99)
                else:
                    thumb_large = get_thumbnail(image, "480x960", quality=99)
                    thumb_small = get_thumbnail(image, "240x320", quality=99)

                gallery_image = {
                    "pk": image_object.pk,
                    "is_selected": image_object.is_selected,
                    "thumb_large": thumb_large.url,
                    "thumb_small": thumb_small.url
                }
                gallery_images.append(gallery_image)

            return render(request, 'gallery_detail.html', {
                'gallery': gallery,
                'gallery_images': gallery_images
            })

        except Gallery.DoesNotExist:
            return redirect('/galleries/')


def new_gallery_image(request):
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

            return redirect('/gallery/' + str(gallery.pk))
            
        else:
            debug.append('form is invalid')
            return render(request, 'gallery_image_failed.html', {'form': form, 'gallery': gallery, 'debug': debug})
    
    form = GalleryImageForm()
    return render(request, 'gallery_detail.html', {'form': form, 'debug': debug})


def select_gallery_image(request, gallery_pk=None, passcode=None, image_pk=None):
    if gallery_pk is None or passcode is None or image_pk is None:
        return redirect('/galleries/')
    else:
        if request.method == 'POST':
            GalleryImage.objects.get(pk=image_pk).is_selected = True

            image.save()

            return render(request, 'gallery_detail.html')


def client_access(request):
    if request.method == 'POST':
        form = ClientAccessForm(request.POST or None)
        
        if form.is_valid():
            passcode = form.cleaned_data['passcode']

            try:
                gallery = Gallery.objects.get(passcode=passcode)
                return redirect('/gallery/' + str(gallery.pk) + "/" + passcode)

            except Gallery.DoesNotExist:
                return render(request, 'client_access.html', {
                    'gallery_does_not_exist': True,
                    'passcode': passcode
                })

    return render(request, 'client_access.html', locals())
