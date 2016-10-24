grammar Build;

programme: (statement)*;

statement
 : route BREAK+
 | declaration BREAK+
 ;

declaration
 : use_declaration
 | include_declaration
 ;

use_declaration
 : 'use' USE_KEYWORD ID
 ;

 include_declaration
  : 'include' (ID | PATH)
  ;

route
  : (PATH | PSEUDO_DEST | ERROR_NAME) ('<-' (PATH | REGEX))+ ('^' condition (BOOL_OP condition)*)?
  | (PATH | STRING) '<-' (ERROR_CODE | ERROR_NAME)
  ;

condition: '!'? (STRING | ID | PATH) (STRING | REGEX | PATH | METHOD);

METHOD
 : '.' (
 | 'isfile'
 | 'isdirectory'
 | 'hastext'
 )
 ;


PATH: ([aArRiI] [uUeE]? | [uUeE] [aArRiI]?)? '<' (~[<\r\n\\] | '\\' .)* '>';

STRING
 : '\'' (~['\r\n\\] | '\\' .)* '\''
 | '"' (~["\r\n\\] | '\\' .)* '"'
 ;

REGEX: '`' (~[`\r\n\\] | '\\' .)* '`';

ERROR_CODE: [0-9][0-9][0-9];

PSEUDO_DEST: 'protect';

ERROR_NAME: 'none' | 'forbid' | 'error';

USE_KEYWORD: 'template' | 'lang' | 'charset';

ID
 : [a-zA-Z][a-zA-Z0-9]* ('.' [a-zA-Z0-9]+)*
 | ':' [ a-zA-Z0-9]* ('.' [a-zA-Z0-9]+)* ':'
 ;
 /*('ip'
 | 'language'
 | 'server.name'
 | 'server.ip'
 | 'server.port'
 | 'time.stamp'
 | 'time.day'
 | 'time.dayofweek'
 | 'time.hour'
 | 'time.minute'
 | 'time.month'
 | 'time.second'
 | 'time.year'
 | 'method'
 | 'connection'
 | 'protocol'
 | 'location'
 | 'filepath'
   ) ':'?
 ;*/


BOOL_OP: '&' | '|';

INT: [0-9]+;

COMMENT
 : ('#' .*? '\n'+
 | '/*' .*? '*/') -> skip
 ;

WS: ([ \t\r]|'\n'+ ' '+)+? -> skip;

BREAK: [;\n]+;