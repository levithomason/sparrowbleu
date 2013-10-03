from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.galleries.models import Gallery, GalleryImage
from apps.galleries.forms import GalleryForm, GalleryImageForm


def galleries(request):
    if not request.user.is_authenticated():
        return redirect('/')
    
    galleries = []
    for gallery in Gallery.objects.all():
        preview_image = GalleryImage.objects.filter(gallery=gallery.pk, is_preview_image=True)

        galleries.append([gallery, preview_image])
    
    return render(request, 'galleries.html', {
      'galleries': galleries,
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

def gallery_detail(request, pk):
    try:
        this_gallery = Gallery.objects.get(pk=pk)
        gallery_images = GalleryImage.objects.filter(gallery=pk)
                
        return render(request, 'gallery_detail.html', {
          'gallery': this_gallery,
          'gallery_images': gallery_images,
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
            is_first_gallery_image = (gallery.galleryimage_set.count() == 0)
            counter = 0

            for image_file in request.FILES.getlist('images'):
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
    
    
    