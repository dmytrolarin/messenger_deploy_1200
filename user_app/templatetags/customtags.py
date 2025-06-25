from django import template

register = template.Library()

@register.inclusion_tag("user_app/inclusion_tags/custom_form.html")
def render_custom_form(form):
    '''
        Цей тег потрібен для генерації кастомної форми за певним, заготовленим нами шаблоном. 
        Він приймає django форму, та на її основі будує html форму.
    '''
    return {"form": form}