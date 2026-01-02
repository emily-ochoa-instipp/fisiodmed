from django import template

register = template.Library()

@register.filter
def has_group(user, group_names):
    """
    Uso:
    {% if request.user|has_group:"Secretaria,Presidenta,'Administrador' %}
    """
    if not user.is_authenticated:
        return False

    groups = group_names.split(',')
    return user.groups.filter(name__in=groups).exists()
