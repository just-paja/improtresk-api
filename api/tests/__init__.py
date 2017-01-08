from model_mommy import mommy


def gen_func():
    return '###Markdown text'


mommy.generators.add('django_markdown.models.MarkdownField', gen_func)
