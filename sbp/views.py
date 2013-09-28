from django.shortcuts import render_to_response
from django.shortcuts import render

def home(request):
    return render_to_response('home.html', locals())

def client_access(request):
    return render_to_response('client_access.html', locals())

def new_gallery(request):
    if request.method == 'POST': # If the form has been submitted...
        form = GalleryForm(request.POST) # A form bound to the POST data
    
        if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
            return HttpResponseRedirect('/') # Redirect after POST
        else:
            form = ContactForm() # An unbound form

    return render(request, 'new_gallery.html', {
        'form': form,
    })