from django import template

register = template.Library()

@register.inclusion_tag('spotlights/render_slide.html')
def render_slide(request=None, slide=None):
    return {
        'request': request,
        'slide': slide,
        'slide_class': type(slide).__name__,
    }

