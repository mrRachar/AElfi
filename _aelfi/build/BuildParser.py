# Generated from Build.g4 by ANTLR 4.5.2
# encoding: utf-8
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\25")
        buf.write("M\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\7\2\22\n\2\f\2\16\2\25\13\2\3\3\3\3\6\3\31\n")
        buf.write("\3\r\3\16\3\32\3\3\3\3\6\3\37\n\3\r\3\16\3 \5\3#\n\3\3")
        buf.write("\4\3\4\5\4\'\n\4\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3")
        buf.write("\7\6\7\63\n\7\r\7\16\7\64\3\7\3\7\3\7\3\7\7\7;\n\7\f\7")
        buf.write("\16\7>\13\7\5\7@\n\7\3\7\3\7\3\7\5\7E\n\7\3\b\5\bH\n\b")
        buf.write("\3\b\3\b\3\b\3\b\2\2\t\2\4\6\b\n\f\16\2\t\4\2\t\t\20\20")
        buf.write("\4\2\t\t\r\16\4\2\t\t\13\13\3\2\t\n\4\2\f\f\16\16\4\2")
        buf.write("\t\n\20\20\3\2\b\13O\2\23\3\2\2\2\4\"\3\2\2\2\6&\3\2\2")
        buf.write("\2\b(\3\2\2\2\n,\3\2\2\2\fD\3\2\2\2\16G\3\2\2\2\20\22")
        buf.write("\5\4\3\2\21\20\3\2\2\2\22\25\3\2\2\2\23\21\3\2\2\2\23")
        buf.write("\24\3\2\2\2\24\3\3\2\2\2\25\23\3\2\2\2\26\30\5\f\7\2\27")
        buf.write("\31\7\25\2\2\30\27\3\2\2\2\31\32\3\2\2\2\32\30\3\2\2\2")
        buf.write("\32\33\3\2\2\2\33#\3\2\2\2\34\36\5\6\4\2\35\37\7\25\2")
        buf.write("\2\36\35\3\2\2\2\37 \3\2\2\2 \36\3\2\2\2 !\3\2\2\2!#\3")
        buf.write("\2\2\2\"\26\3\2\2\2\"\34\3\2\2\2#\5\3\2\2\2$\'\5\b\5\2")
        buf.write("%\'\5\n\6\2&$\3\2\2\2&%\3\2\2\2\'\7\3\2\2\2()\7\3\2\2")
        buf.write(")*\7\17\2\2*+\7\20\2\2+\t\3\2\2\2,-\7\4\2\2-.\t\2\2\2")
        buf.write(".\13\3\2\2\2/\62\t\3\2\2\60\61\7\5\2\2\61\63\t\4\2\2\62")
        buf.write("\60\3\2\2\2\63\64\3\2\2\2\64\62\3\2\2\2\64\65\3\2\2\2")
        buf.write("\65?\3\2\2\2\66\67\7\6\2\2\67<\5\16\b\289\7\21\2\29;\5")
        buf.write("\16\b\2:8\3\2\2\2;>\3\2\2\2<:\3\2\2\2<=\3\2\2\2=@\3\2")
        buf.write("\2\2><\3\2\2\2?\66\3\2\2\2?@\3\2\2\2@E\3\2\2\2AB\t\5\2")
        buf.write("\2BC\7\5\2\2CE\t\6\2\2D/\3\2\2\2DA\3\2\2\2E\r\3\2\2\2")
        buf.write("FH\7\7\2\2GF\3\2\2\2GH\3\2\2\2HI\3\2\2\2IJ\t\7\2\2JK\t")
        buf.write("\b\2\2K\17\3\2\2\2\f\23\32 \"&\64<?DG")
        return buf.getvalue()


class BuildParser ( Parser ):

    grammarFileName = "Build.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'use'", "'include'", "'<-'", "'^'", "'!'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'protect'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "METHOD", "PATH", "STRING", 
                      "REGEX", "ERROR_CODE", "PSEUDO_DEST", "ERROR_NAME", 
                      "USE_KEYWORD", "ID", "BOOL_OP", "INT", "COMMENT", 
                      "WS", "BREAK" ]

    RULE_programme = 0
    RULE_statement = 1
    RULE_declaration = 2
    RULE_use_declaration = 3
    RULE_include_declaration = 4
    RULE_route = 5
    RULE_condition = 6

    ruleNames =  [ "programme", "statement", "declaration", "use_declaration", 
                   "include_declaration", "route", "condition" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    METHOD=6
    PATH=7
    STRING=8
    REGEX=9
    ERROR_CODE=10
    PSEUDO_DEST=11
    ERROR_NAME=12
    USE_KEYWORD=13
    ID=14
    BOOL_OP=15
    INT=16
    COMMENT=17
    WS=18
    BREAK=19

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.5.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgrammeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BuildParser.StatementContext)
            else:
                return self.getTypedRuleContext(BuildParser.StatementContext,i)


        def getRuleIndex(self):
            return BuildParser.RULE_programme

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgramme" ):
                listener.enterProgramme(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgramme" ):
                listener.exitProgramme(self)




    def programme(self):

        localctx = BuildParser.ProgrammeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_programme)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BuildParser.T__0) | (1 << BuildParser.T__1) | (1 << BuildParser.PATH) | (1 << BuildParser.STRING) | (1 << BuildParser.PSEUDO_DEST) | (1 << BuildParser.ERROR_NAME))) != 0):
                self.state = 14
                self.statement()
                self.state = 19
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def route(self):
            return self.getTypedRuleContext(BuildParser.RouteContext,0)


        def BREAK(self, i:int=None):
            if i is None:
                return self.getTokens(BuildParser.BREAK)
            else:
                return self.getToken(BuildParser.BREAK, i)

        def declaration(self):
            return self.getTypedRuleContext(BuildParser.DeclarationContext,0)


        def getRuleIndex(self):
            return BuildParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = BuildParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.state = 32
            token = self._input.LA(1)
            if token in [BuildParser.PATH, BuildParser.STRING, BuildParser.PSEUDO_DEST, BuildParser.ERROR_NAME]:
                self.enterOuterAlt(localctx, 1)
                self.state = 20
                self.route()
                self.state = 22 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 21
                    self.match(BuildParser.BREAK)
                    self.state = 24 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==BuildParser.BREAK):
                        break


            elif token in [BuildParser.T__0, BuildParser.T__1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 26
                self.declaration()
                self.state = 28 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 27
                    self.match(BuildParser.BREAK)
                    self.state = 30 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==BuildParser.BREAK):
                        break


            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DeclarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def use_declaration(self):
            return self.getTypedRuleContext(BuildParser.Use_declarationContext,0)


        def include_declaration(self):
            return self.getTypedRuleContext(BuildParser.Include_declarationContext,0)


        def getRuleIndex(self):
            return BuildParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)




    def declaration(self):

        localctx = BuildParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_declaration)
        try:
            self.state = 36
            token = self._input.LA(1)
            if token in [BuildParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 34
                self.use_declaration()

            elif token in [BuildParser.T__1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 35
                self.include_declaration()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Use_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def USE_KEYWORD(self):
            return self.getToken(BuildParser.USE_KEYWORD, 0)

        def ID(self):
            return self.getToken(BuildParser.ID, 0)

        def getRuleIndex(self):
            return BuildParser.RULE_use_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUse_declaration" ):
                listener.enterUse_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUse_declaration" ):
                listener.exitUse_declaration(self)




    def use_declaration(self):

        localctx = BuildParser.Use_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_use_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(BuildParser.T__0)
            self.state = 39
            self.match(BuildParser.USE_KEYWORD)
            self.state = 40
            self.match(BuildParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Include_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(BuildParser.ID, 0)

        def PATH(self):
            return self.getToken(BuildParser.PATH, 0)

        def getRuleIndex(self):
            return BuildParser.RULE_include_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInclude_declaration" ):
                listener.enterInclude_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInclude_declaration" ):
                listener.exitInclude_declaration(self)




    def include_declaration(self):

        localctx = BuildParser.Include_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_include_declaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(BuildParser.T__1)
            self.state = 43
            _la = self._input.LA(1)
            if not(_la==BuildParser.PATH or _la==BuildParser.ID):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RouteContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PATH(self, i:int=None):
            if i is None:
                return self.getTokens(BuildParser.PATH)
            else:
                return self.getToken(BuildParser.PATH, i)

        def PSEUDO_DEST(self):
            return self.getToken(BuildParser.PSEUDO_DEST, 0)

        def ERROR_NAME(self):
            return self.getToken(BuildParser.ERROR_NAME, 0)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BuildParser.ConditionContext)
            else:
                return self.getTypedRuleContext(BuildParser.ConditionContext,i)


        def REGEX(self, i:int=None):
            if i is None:
                return self.getTokens(BuildParser.REGEX)
            else:
                return self.getToken(BuildParser.REGEX, i)

        def BOOL_OP(self, i:int=None):
            if i is None:
                return self.getTokens(BuildParser.BOOL_OP)
            else:
                return self.getToken(BuildParser.BOOL_OP, i)

        def STRING(self):
            return self.getToken(BuildParser.STRING, 0)

        def ERROR_CODE(self):
            return self.getToken(BuildParser.ERROR_CODE, 0)

        def getRuleIndex(self):
            return BuildParser.RULE_route

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoute" ):
                listener.enterRoute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoute" ):
                listener.exitRoute(self)




    def route(self):

        localctx = BuildParser.RouteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_route)
        self._la = 0 # Token type
        try:
            self.state = 66
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 45
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BuildParser.PATH) | (1 << BuildParser.PSEUDO_DEST) | (1 << BuildParser.ERROR_NAME))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 48 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 46
                    self.match(BuildParser.T__2)
                    self.state = 47
                    _la = self._input.LA(1)
                    if not(_la==BuildParser.PATH or _la==BuildParser.REGEX):
                        self._errHandler.recoverInline(self)
                    else:
                        self.consume()
                    self.state = 50 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==BuildParser.T__2):
                        break

                self.state = 61
                _la = self._input.LA(1)
                if _la==BuildParser.T__3:
                    self.state = 52
                    self.match(BuildParser.T__3)
                    self.state = 53
                    self.condition()
                    self.state = 58
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==BuildParser.BOOL_OP:
                        self.state = 54
                        self.match(BuildParser.BOOL_OP)
                        self.state = 55
                        self.condition()
                        self.state = 60
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                _la = self._input.LA(1)
                if not(_la==BuildParser.PATH or _la==BuildParser.STRING):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 64
                self.match(BuildParser.T__2)
                self.state = 65
                _la = self._input.LA(1)
                if not(_la==BuildParser.ERROR_CODE or _la==BuildParser.ERROR_NAME):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConditionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self, i:int=None):
            if i is None:
                return self.getTokens(BuildParser.STRING)
            else:
                return self.getToken(BuildParser.STRING, i)

        def ID(self):
            return self.getToken(BuildParser.ID, 0)

        def PATH(self, i:int=None):
            if i is None:
                return self.getTokens(BuildParser.PATH)
            else:
                return self.getToken(BuildParser.PATH, i)

        def REGEX(self):
            return self.getToken(BuildParser.REGEX, 0)

        def METHOD(self):
            return self.getToken(BuildParser.METHOD, 0)

        def getRuleIndex(self):
            return BuildParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)




    def condition(self):

        localctx = BuildParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_condition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            _la = self._input.LA(1)
            if _la==BuildParser.T__4:
                self.state = 68
                self.match(BuildParser.T__4)


            self.state = 71
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BuildParser.PATH) | (1 << BuildParser.STRING) | (1 << BuildParser.ID))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
            self.state = 72
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BuildParser.METHOD) | (1 << BuildParser.PATH) | (1 << BuildParser.STRING) | (1 << BuildParser.REGEX))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





