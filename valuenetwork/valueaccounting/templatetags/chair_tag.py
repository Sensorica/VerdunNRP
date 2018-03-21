from django import template

regiser = template.Library()

@regiser.inclusion_tag('chair.html')
def chair(desc, field):
    return {'desc': desc, 'field': field, 'linebreaks': ('\n' in field or '<br' in field)}
