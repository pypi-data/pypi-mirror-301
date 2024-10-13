from markdown import Extension

from osbot_markdown.markdown.md__pre_processors.Pre_Processor__IFrame import Pre_Processor__IFrame
from osbot_markdown.markdown.md__pre_processors.Pre_Processor__QUnit import Pre_Processor__QUnit


class Extension__QUnit(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(Pre_Processor__QUnit(md), 'qunit', 175)