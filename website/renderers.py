
def render_markdown(env, template, **kwargs):
    content_template = env.get_template("_content.html")
    output_path = "%s/%s" % (env.outpath, template.name.replace(".md", ".html"))
    content_template.stream(**kwargs).dump(output_path)
