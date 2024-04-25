from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from pprint import pformat


class AstProcessor:

    def __init__(self, logging, listener, parser, lexer):
        self.logging = logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.listener = listener
        self.parser = parser
        self.lexer = lexer

    def execute(self, input_source):
        parser = self.parser(CommonTokenStream(self.lexer(FileStream(input_source, encoding="utf-8"))))
        walker = ParseTreeWalker()
        walker.walk(self.listener, parser.compilationUnit())
        self.logger.debug('Display all data extracted by AST. \n' + pformat(self.listener.ast_info, width=160))
        return self.listener.ast_info
