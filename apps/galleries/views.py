from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.files.uploadedfile import SimpleUploadedFile
from settings import CLIENT_ACCESS_KEY

from sorl.thumbnail import get_thumbnail

from apps.galleries.models import Gallery, GalleryImage
from apps.galleries.forms import GalleryForm, GalleryImageForm, ClientAccessForm


def galleries(request):
    if not request.user.is_authenticated():
        return redirect('/')
    
    galleries = []
    preview_image = None
    
    for gallery in Gallery.objects.all():
        preview_image = GalleryImage.objects.get(gallery=gallery, is_preview_image=True)
        preview_image_thumbnail = get_thumbnail(preview_image.image, '500x500', crop='center', quality=99)
        
        galleries.append([gallery, preview_image_thumbnail.url])
    
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
        
    else:
        
        form = GalleryForm()
        
    return render(request, 'new_gallery.html', {
        'form': form
    })

def gallery_detail(request, pk=None, passcode=None):
    if (pk == None or passcode == None):
        return redirect('/galleries/')
    else:
        try:
            gallery = Gallery.objects.get(pk=pk)
            gallery_images_qs = GalleryImage.objects.filter(gallery=pk)
            gallery_images_and_thumbnails = []
            thumbnail_scale = 0.20

            for gallery_image_object in gallery_images_qs:

                gallery_image = GalleryImage.objects.get(pk=gallery_image_object.pk).image

                thumbnail_width = str(int(gallery_image.width * thumbnail_scale))
                thumbnail_height = str(int(gallery_image.height * thumbnail_scale))
                
                thumbnail = get_thumbnail(gallery_image, thumbnail_width + 'x' + thumbnail_height, quality=99)
                
                gallery_images_and_thumbnails.append([gallery_image.url, thumbnail.url])
                
            return render(request, 'gallery_detail.html', {
              'gallery': gallery,
              'gallery_images_and_thumbnails': gallery_images_and_thumbnails,
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
                    new_image.is_preview_image=True
                    
                new_image.image.save(image_file.name, image_file)
                counter += 1

            return redirect('/gallery/' + str(gallery.pk))
            
        else:
            debug.append('form is invalid')
            return render(request, 'gallery_image_failed.html', {'form': form, 'gallery': gallery, 'debug': debug})
    
    form = GalleryImageForm()
    return render(request, 'gallery_detail.html', {'form': form, 'gallery': gallery, 'debug': debug})

def client_access(request):
    if request.method == 'POST':
        form = ClientAccessForm(request.POST or None)
        
        if form.is_valid():
            passcode = form.cleaned_data['passcode']
            gallery = Gallery.objects.get(passcode=passcode)
            
            return redirect('/gallery/' + str(gallery.pk) + "/" + passcode)

    return render(request, 'client_access.html', locals())    
    
    