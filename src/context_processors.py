def current_site(request):
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    return {'current_site': site}
