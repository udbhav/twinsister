from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from apps.images.models import Image, Gallery

def image(request, gallery_id, image_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    image = get_object_or_404(Image, pk=image_id)
    return render_to_response('images/image.html', {
            'gallery': gallery,
            'image': image,
            }, context_instance=RequestContext(request))
    
