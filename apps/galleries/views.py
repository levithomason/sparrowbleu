from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.galleries.models import Gallery, GalleryImage
from apps.galleries.forms import GalleryForm, GalleryImageForm

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
            
            return redirect('galleries')
        
    else:
        
        form = GalleryForm()
        
    return render(request, 'new_gallery.html', {
        'form': form
    })

    
def gallery_posted(request):
    if not request.user.is_authenticated():
        return redirect('/')

    return render(request, 'gallery_posted.html')


def galleries(request):
    if not request.user.is_authenticated():
        return redirect('/')
    
    galleries = Gallery.objects.all()
    
    return render(request, 'galleries.html', {
      'galleries': galleries,
    })
    
def gallery_detail(request, pk):
    this_gallery = Gallery.objects.get(pk=pk)
    gallery_images = GalleryImage.objects.filter(gallery=pk)
    
    return render(request, 'gallery_detail.html', {
      'gallery': this_gallery,
      'gallery_images': gallery_images,
    })
    
def new_gallery_image(request):

    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = Gallery.objects.get(pk=request.POST['gallery'])
            
            for image_file in request.FILES.getlist('image'):
                new_image = GalleryImage.objects.create(gallery=gallery)
                new_image.image.save(image_file.name, image_file)
            
            return redirect('/gallery/' + str(gallery.pk))

        else:
            form = GalleryImageForm()
    else:
        form = GalleryImageForm()

    return render(request, 'uploaded_image.html', {'form': form})



###############################################################
# Debug stuff
###############################################################

def images(request):
    images = GalleryImage.objects.all()
    
    return render(request, 'images.html', {'images': images})

def upload_test(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        return render(request, 'upload_test.html', {'form': form})
    else:
        form = GalleryImageForm()
        return render(request, 'upload_test.html', {'form': form})



