from django.template.defaulttags import register


@register.filter
def get_value(dictionary, key="QF"):
    return dictionary.get(key)
