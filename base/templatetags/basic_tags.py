from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def limit(value, arg):
    """Limit the number of items in a list. This is needed because
    the Django slice templatetag doesn't allow us to pass in a value
    dynamically."""
    try:
        return value[:arg]
    except TypeError:
        return value


@register.filter
def has_h2_block(body):
    """Check if a StreamField body contains an h2 block."""
    for block in body:
        if block.block_type == 'h2':
            return True
    return False


@register.simple_tag(takes_context=True)
def render_nested_pages(context, page, max_depth=1, current_depth=1):
    """Recursive template tag for displaying a sitemap for a section
    of the site."""
    if current_depth > max_depth:
        return ''

    output = []
    for child in page.get_children().specific():
        if child.live and child.show_in_menus:
            output.append(f'<li class="nav-item"><a class="nav-link" href="{child.url}">{child.title}</a>')
            if child.get_children().filter(live=True, show_in_menus=True).exists():
                output.append('<ul class="nav flex-column">')
                output.append(
                    render_nested_pages(context, child, max_depth, current_depth + 1)
                )
                output.append('</ul>')
            output.append('</li>')

    return mark_safe('\n'.join(output))
