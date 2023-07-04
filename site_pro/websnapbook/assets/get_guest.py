from ..models import Guest


def get_event_guests(event):
    guests = Guest.objects.filter(events__in=[event])
    return guests
