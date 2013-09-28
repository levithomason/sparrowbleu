from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from sbp.galleries.forms import GalleryForm

def new_gallery(request):
    form = GalleryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            gallery = form.save()
            gallery.save()
            return redirect(gallery_posted)
        
    return render_to_response('new_gallery.html', {'form': form}, context_instance=RequestContext(request))


def contact_add(request):
    # sticks in a POST or renders empty form
    form = ContactForm(request.POST or None)
    if form.is_valid():
        cmodel = form.save()
        #This is where you might chooose to do stuff.
        #cmodel.name = 'test1'
        cmodel.save()
        return redirect(contacts)

    return render_to_response('phonebook/contact_add.html',
                              {'contact_form': form},
                              context_instance=RequestContext(request))