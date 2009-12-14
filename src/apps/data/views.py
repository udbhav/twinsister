from django.views.generic import list_detail
from django.shortcuts import get_object_or_404

from apps.data.models import Data
from apps.people.models import Person

def entries_by_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    return list_detail.object_list(
        request, 
        queryset = Data.objects.filter(published=True).filter(posted_by=person).order_by('-pub_date'),
        paginate_by = 15,
        template_name = 'data/person_data_list.html',
        extra_context = {'person': person},
        )

