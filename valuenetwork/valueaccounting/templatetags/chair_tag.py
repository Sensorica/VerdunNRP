from django import template

register = template.Library()

@register.inclusion_tag('chair.html')
def chair(desc, field):
    return {'desc': desc, 'field': field, 'linebreaks': ('\n' in field or '<br' in field)}
