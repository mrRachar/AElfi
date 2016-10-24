# Generated from Build.g4 by ANTLR 4.5.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BuildParser import BuildParser
else:
    from BuildParser import BuildParser

# This class defines a complete listener for a parse tree produced by BuildParser.
class BuildListener(ParseTreeListener):

    # Enter a parse tree produced by BuildParser#programme.
    def enterProgramme(self, ctx:BuildParser.ProgrammeContext):
        pass

    # Exit a parse tree produced by BuildParser#programme.
    def exitProgramme(self, ctx:BuildParser.ProgrammeContext):
        pass


    # Enter a parse tree produced by BuildParser#statement.
    def enterStatement(self, ctx:BuildParser.StatementContext):
        pass

    # Exit a parse tree produced by BuildParser#statement.
    def exitStatement(self, ctx:BuildParser.StatementContext):
        pass


    # Enter a parse tree produced by BuildParser#declaration.
    def enterDeclaration(self, ctx:BuildParser.DeclarationContext):
        pass

    # Exit a parse tree produced by BuildParser#declaration.
    def exitDeclaration(self, ctx:BuildParser.DeclarationContext):
        pass


    # Enter a parse tree produced by BuildParser#use_declaration.
    def enterUse_declaration(self, ctx:BuildParser.Use_declarationContext):
        pass

    # Exit a parse tree produced by BuildParser#use_declaration.
    def exitUse_declaration(self, ctx:BuildParser.Use_declarationContext):
        pass


    # Enter a parse tree produced by BuildParser#include_declaration.
    def enterInclude_declaration(self, ctx:BuildParser.Include_declarationContext):
        pass

    # Exit a parse tree produced by BuildParser#include_declaration.
    def exitInclude_declaration(self, ctx:BuildParser.Include_declarationContext):
        pass


    # Enter a parse tree produced by BuildParser#route.
    def enterRoute(self, ctx:BuildParser.RouteContext):
        pass

    # Exit a parse tree produced by BuildParser#route.
    def exitRoute(self, ctx:BuildParser.RouteContext):
        pass


    # Enter a parse tree produced by BuildParser#condition.
    def enterCondition(self, ctx:BuildParser.ConditionContext):
        pass

    # Exit a parse tree produced by BuildParser#condition.
    def exitCondition(self, ctx:BuildParser.ConditionContext):
        pass


