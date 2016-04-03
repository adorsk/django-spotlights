from django import template

register = template.Library()

@register.inclusion_tag('spotlights/render_slide.html')
def render_slide(request=None, slide=None):
    print("r: ", request, "s: ", slide)
    return {
        'request': request,
        'slide': slide,
    }
