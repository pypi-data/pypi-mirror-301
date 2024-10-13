from osbot_markdown.markdown.md__extensions.Extension__Chat_Bot         import Extension__Chat_Bot
from osbot_markdown.markdown.md__extensions.Extension__IFrame           import Extension__IFrame
from osbot_markdown.markdown.md__extensions.Extension__Mermaid          import Extension__Mermaid
from osbot_markdown.markdown.md__extensions.Extension__QUnit            import Extension__QUnit
#from osbot_markdown.markdown.md__extensions.Extension__Render_Template  import Extension__Render_Template
from osbot_markdown.markdown.md__extensions.Extension__Video            import Extension__Video

from markdown                                           import Markdown
from osbot_utils.base_classes.Type_Safe                 import Type_Safe
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self


class Markdown_Parser(Type_Safe):


    def markdown(self):
        return Markdown(extensions=self.extensions())

    @cache_on_self
    def extensions(self):

        from markdown.extensions.attr_list   import AttrListExtension
        from markdown.extensions.def_list    import DefListExtension
        from markdown.extensions.footnotes   import FootnoteExtension
        from markdown.extensions.md_in_html  import MarkdownInHtmlExtension
        from markdown.extensions.meta        import MetaExtension
        from markdown.extensions.tables      import TableExtension
        from markdown.extensions.fenced_code import FencedCodeExtension

        markdown_default_extensions = [ AttrListExtension           (),
                                        DefListExtension            (),
                                        FootnoteExtension           (),
                                        MarkdownInHtmlExtension     (),
                                        MetaExtension               (),
                                        TableExtension              (),
                                        FencedCodeExtension         ()
                                        ]

        custom_extensions           = [ Extension__Chat_Bot         (),
                                        Extension__IFrame           (),
                                        Extension__Mermaid          (),
                                        Extension__QUnit            (),
                                        #Extension__Render_Template  (),
                                        Extension__Video            ()]

        return custom_extensions + markdown_default_extensions

    def markdown_to_html(self, markdown_text):
        return self.parse(markdown_text).get('html')

    def markdown_to_html_and_metadata(self, markdown_text):
        data = self.parse(markdown_text)
        return { 'html' : data.get('html'), 'metadata' : data.get('meta')}

    def content_to_html(self, content):
        return self.parse(content).get('html')


    def parse(self, markdown_text):
        if markdown_text:
            markdown = self.markdown()
            html     = markdown.convert(markdown_text)
            meta     = self.extract_metadata_from_markdown(markdown)
        else:
            html = ''
            meta = {'error': 'markdown file not found'}
        return dict(markdown_text=markdown_text, html=html, meta=meta)

    def extract_metadata_from_markdown(self, markdown):
        metadata = {}
        for key,value in markdown.Meta.items():  # this is from the MetaExtension
            metadata[key] = ' '.join(value)      # change
        return metadata

markdown_parser = Markdown_Parser()