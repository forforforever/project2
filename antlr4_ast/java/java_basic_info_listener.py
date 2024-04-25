from antlr4_ast.java.JavaParserListener import JavaParserListener
from antlr4_ast.java.JavaParser import JavaParser


class JavaBasicInfoListener(JavaParserListener):

    def __init__(self):
        self.call_methods = []
        self.ast_info = {
            'packageName': '',
            'classes': [],
            'imports': [],
            'fields': [],
            'methods': []
        }

    # Enter a parse tree produced by JavaParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        self.ast_info['packageName'] = ctx.qualifiedName().getText()

    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        import_class = ctx.qualifiedName().getText()
        self.ast_info['imports'].append(import_class)

    # Enter a parse tree produced by JavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        # print("Start line: {0} | End line: {1} | Method name: {2}".format(ctx.start.line, ctx.methodBody(
        # ).stop.line, ctx.getChild(1).getText()))
        self.call_methods = []

    # Exit a parse tree produced by JavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        c1 = ctx.getChild(0).getText()  # ---> return type
        c2 = ctx.getChild(1).getText()  # ---> method name
        params = self.parse_method_params_block(ctx.getChild(2))

        method_info = {
            'startLine': ctx.start.line,
            'endLine': ctx.methodBody().stop.line if ctx.methodBody() else None,
            'returnType': c1,
            'methodName': c2,
            'params': params,
            'masterObject': {},
            'depth': ctx.depth(),
            'callMethods': self.call_methods
        }
        self.check_masterObject(ctx, method_info)
        self.ast_info['methods'].append(method_info)

    # Enter a parse tree produced by JavaParser#methodCall.
    def enterMethodCall(self, ctx: JavaParser.MethodCallContext):
        line_number = str(ctx.start.line)
        column_number = str(ctx.start.column)
        self.call_methods.append(line_number + ' ' + column_number + ' ' + ctx.parentCtx.getText())

    # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        class_info = {
            'startLine': ctx.start.line,
            'endLine': ctx.classBody().stop.line if ctx.classBody() else None,
            'className': '',
            'extends': '',
            'implements': '',
            'masterObject': {},
            'depth': ctx.depth(),
        }

        child_count = int(ctx.getChildCount())
        if child_count == 7:
            # class Foo extends Bar implements Hoge
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            # c3 = ctx.getChild(2)  # ---> extends
            c4 = ctx.getChild(3).getChild(0).getText()  # ---> extends class name
            # c5 = ctx.getChild(4)  # ---> implements
            # c7 = ctx.getChild(6)  # ---> method body

            class_info['className'] = c2
            class_info['extends'] = c4
            class_info['implements'] = self.parse_implements_block(ctx.getChild(5))
            self.check_masterObject(ctx, class_info)
            self.ast_info['classes'].append(class_info)
        elif child_count == 5:
            # class Foo extends Bar
            # or
            # class Foo implements Hoge
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            c3 = ctx.getChild(2).getText()  # ---> extends or implements
            # c5 = ctx.getChild(4)  # ---> method body

            class_info['className'] = c2
            if c3 == 'implements':
                class_info['implements'] = self.parse_implements_block(ctx.getChild(3))
            elif c3 == 'extends':
                c4 = ctx.getChild(3).getChild(0).getText()  # ---> extends class name or implements class name
                class_info['extends'] = c4
            self.check_masterObject(ctx, class_info)
            self.ast_info['classes'].append(class_info)
        elif child_count == 3:
            # class Foo
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            # c3 = ctx.getChild(2)  # ---> method body

            class_info['className'] = c2
            self.check_masterObject(ctx, class_info)
            self.ast_info['classes'].append(class_info)

    # Enter a parse tree produced by JavaParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        field = {
            'fieldType': ctx.getChild(0).getText(),
            'fieldDefinition': ctx.getChild(1).getText()
        }
        self.ast_info['fields'].append(field)

    def parse_implements_block(self, ctx):
        implements_child_count = int(ctx.getChildCount())
        result = []
        if implements_child_count == 1:
            impl_class = ctx.getChild(0).getText()
            result.append(impl_class)
        elif implements_child_count > 1:
            for i in range(implements_child_count):
                if i % 2 == 0:
                    impl_class = ctx.getChild(i).getText()
                    result.append(impl_class)
        return result

    def parse_method_params_block(self, ctx):
        params_exist_check = int(ctx.getChildCount())
        result = []
        # () ---> 2
        # (Foo foo) ---> 3
        # (Foo foo, Bar bar) ---> 3
        # (Foo foo, Bar bar, int count) ---> 3
        if params_exist_check == 3:
            params_child_count = int(ctx.getChild(1).getChildCount())
            if params_child_count == 1:
                param_type = ctx.getChild(1).getChild(0).getChild(0).getText()
                param_name = ctx.getChild(1).getChild(0).getChild(1).getText()
                param_info = {
                    'paramType': param_type,
                    'paramName': param_name
                }
                result.append(param_info)
            elif params_child_count > 1:
                for i in range(params_child_count):
                    if i % 2 == 0:
                        param_type = ctx.getChild(1).getChild(i).getChild(0).getText()
                        param_name = ctx.getChild(1).getChild(i).getChild(1).getText()
                        param_info = {
                            'paramType': param_type,
                            'paramName': param_name
                        }
                        result.append(param_info)
        return result

    def check_masterObject(self, ctx, object_info):
        parentCtx = ctx.parentCtx
        if isinstance(parentCtx, JavaParser.MemberDeclarationContext):
            masterCtx = parentCtx.parentCtx.parentCtx.parentCtx
            object_info['masterObject']['objectName'] = masterCtx.getChild(1).getText()
            object_info['masterObject']['startLine'] = masterCtx.start.line
