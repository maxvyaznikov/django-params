from django import template
from ..models import Param

register = template.Library()

@register.filter(is_safe=True)
def param(name):
    return Param.get(name)
