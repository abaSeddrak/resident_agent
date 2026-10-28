from markdownify import markdownify

def html_to_text(html: str):
    return markdownify(html, escape_asterisks=False, heading_style="ATX").strip()