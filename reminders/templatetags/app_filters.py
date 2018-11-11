from django import template

register = template.Library()

@register.filter(name="remainder")
def remainder(value,loop_counter):

    return (value-loop_counter)%5