import markdown

def read_markdown(template):
    md = markdown.Markdown(output_format="html5")
    with open(template.filename) as markdownfile:
        markdown_content = markdownfile.read()
        return {"html": md.convert(markdown_content)}
