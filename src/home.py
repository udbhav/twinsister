from django.shortcuts import render_to_response, redirect 
from django.template import RequestContext
from django.conf import settings
from apps.music.models import Release

def home(request):
    if request.session.get('repeat_visitor', False):
        return redirect('entries_by_page', page=1)
    else:
        request.session['repeat_visitor'] = True
        return redirect('splash')


def splash(request):
    object_list = Release.objects.filter(official=True).order_by('-pub_date')[:1]
    return render_to_response('home.html', {
            'object_list': object_list,
            }, context_instance=RequestContext(request))
