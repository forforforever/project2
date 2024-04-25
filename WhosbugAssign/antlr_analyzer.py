import logging.config
import os
from antlr4_ast.ast_processor import AstProcessor
from antlr4_ast.java.java_basic_info_listener import JavaBasicInfoListener
from antlr4_ast.java.JavaLexer import JavaLexer
from antlr4_ast.java.JavaParser import JavaParser



def log_init():
    file_conf_path = 'WhosbugAssign/analyzeLog/utiltools_log.conf'
    if os.path.exists(file_conf_path):
        logging.config.fileConfig(file_conf_path)
    else:
        print('Logging config file path not exist, path: {}'.format(file_conf_path))


def analyze_java(target_file_path):
    AST_ANALYZER = AstProcessor(logging, JavaBasicInfoListener(), JavaParser, JavaLexer)
    return AST_ANALYZER.execute(target_file_path)


if __name__ == '__main__':
    res = analyze_java('../antlr4_ast/testfiles/java/AllInOne7.java')
    print(res)
