from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """
    Ajoute des classes CSS Tailwind aux champs du formulaire.
    Usage dans le template: {{ form.username|add_class:"border p-2 rounded w-full" }}
    """
    return field.as_widget(attrs={"class": css})
