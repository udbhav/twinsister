from django.core.exceptions import ObjectDoesNotExist

def delete_subclasses(sender, instance, *args, **kwargs):
    # If one of the subclasses is deleted, clean up after ourselves and delete the instance of the parent class as well

    try: 
        data = instance.data_ptr
    except (AttributeError, ObjectDoesNotExist):
        pass
    else:
        try:
            data.delete()
        except AssertionError:
            pass
