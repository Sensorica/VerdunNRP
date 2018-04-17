from django import template

register = template.Library()

@register.inclusion_tag("valueaccounting/_form_dialog.html")
def form_dialog(
    dialog_id,
    action,
    form,
    title,
    confirm_text='Save',
    method='POST',
    formset=None,
    label_id=None,
    form_id=None
):

    if not label_id:
        label_id = 'label-for-%s' % (dialog_id,)
    if not form_id:
        form_id = 'form-for-%s' % (dialog_id,)

    return {
        'dialog_id': dialog_id,
        'action': action,
        'form': form,
        'title': title,
        'confirm_text': confirm_text,
        'method': method,
        'formset': formset,
        'label_id': label_id,
        'form_id': form_id
    }
