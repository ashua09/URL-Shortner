import string
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Shortner
from .forms import ShortenerForm

# Create your views here.

def index(request):
    form=ShortenerForm()
    context= {'form':form}
    return render(request, 'app/home.html', context)


def home_view(request):
    
    
    if request.method == 'POST':

        used_form = ShortenerForm(request.POST)

        if used_form.is_valid():
            
            shortened_object = used_form.save()
            long_url = shortened_object.long_url
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
              
            context= {'new_url': new_url,
                      'long_url': long_url}
             
            return render(request, 'app/home.html', context)
        else:
            context['errors']= used_form.errors
            return render(request, 'app/home.html', context)
    else:
        form=ShortenerForm()
        context= {'form':form}
        return render(request, 'app/home.html', context)
    

def redirect_url_view(request, shortened_part):

    try:
        shortener = Shortner.objects.get(short_url=shortened_part)

        shortener.times_followed += 1        

        shortener.save()
        
        return HttpResponseRedirect(shortener.long_url)
        
    except:
        raise Http404('Sorry this link is broken :(')