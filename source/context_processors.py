def current_site(request):
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    return {'current_site': site}

def paypal_submit_url(request):
    from django.conf import settings
    if settings.DEBUG:
        url = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
    else:
        url = 'https://www.paypal.com/cgi-bin/webscr'
    return {'paypal_submit_url': url}
