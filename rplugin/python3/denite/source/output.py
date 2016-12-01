# ============================================================================
# FILE: output.py
# AUTHOR: momotaro <momotaro.n@gmail.com>
# License: MIT license
# ============================================================================

from .base import Base
import os
import re

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'output'
        self.kind = 'word'
        self.syntax_name = 'deniteSource_output'

    def on_init(self, context):
        command = ' '.join(context['args'])
        if not command:
            command = self.vim.call('input',
                    'Please input Vim command: ', context['input'])
        context['__command'] = command

    def gather_candidates(self, context):
        message = self.vim.call('denite#util#redir', context['__command'])
        message = re.sub('^(\r\n|\n)', '', message)
        return list(map(lambda x: { 'word': x, 'action__text': x },
            re.split('\r\n|\n', message)))

    def highlight_syntax(self):
        self.vim.command('syntax include @Vim syntax/vim.vim')
        self.vim.command('syntax region ' + self.syntax_name + 'Vim'
                ' start=// end=/$/ contains=@Vim containedin=' + self.syntax_name)
