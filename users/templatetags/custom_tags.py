from django import template
from django.utils import timezone
import datetime

register = template.Library()

@register.filter
def is_online(last_activity):
    if not last_activity:
        return False
    now = timezone.now()
    diff = now - last_activity
    # Consideramos online si hubo actividad en los últimos 5 minutos
    return diff < datetime.timedelta(minutes=5)

@register.filter(name='split')
def split(value, key):
    """
        Devuelve el valor spliteado por la key
    """
    return value.split(key)
