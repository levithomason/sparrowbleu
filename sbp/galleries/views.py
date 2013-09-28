from django.shortcuts import render, redirect
from django.views.generic import ListView

from sbp.galleries.models import Gallery
from sbp.galleries.forms import GalleryForm


def new_gallery(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST or None)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            passcode = form.cleaned_data['passcode']
            number_of_images = form.cleaned_data['number_of_images']
            
            gallery = Gallery(name=name, passcode=passcode, number_of_images=number_of_images)
            gallery.save()
            
            return redirect('gallery_posted')
        
    else:
        
        form = GalleryForm()
        
    return render(request, 'new_gallery.html', {
        'form': form
    })
    
    
def gallery_posted(request):
    return render(request, 'gallery_posted.html')


class galleries(ListView):
    model = Gallery
    context_object_name = 'Galleries'
    template_name = 'galleries.html'