grammar lect;

// ----- Start symbols for the grammar.

// A single interactive statement, entered in REPL prompt.
// Note the extra line break to terminate.
single_input
  : LINE_BREAK | simple_stmt | compound_stmt LINE_BREAK
  ;

// A single file of code.
file_input
  : (LINE_BREAK | stmt)* ENDMARKER
  ;

// An expression passed to the eval() function.
eval_input
  : testlist LINE_BREAK* ENDMARKER
  ;

stmt
  : simple_stmt | compound_stmt
  ;

simple_stmt
  : small_stmt (';' small_stmt)* ';' LINE_BREAK
  ;

small_stmt
  : (expr_stmt | print_stmt | del_stmt | pass_stmt | flow_stmt | import_stmt | assert_stmt)
  ;

expr_stmt
  : testlist (augassign (yield_expr|testlist) | (ASSIGN (yield_expr|testlist))*)
  ;

augassign
  : ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' | '<<=' | '>>=' | '**=' | '//=')
  ;

// For normal assignments, additional restrictions enforced by the interpreter
print_stmt
  : 'print' ( ( test (',' test)* ',' )? | '>>' test ( (',' test)+ ','? )? )
  ;

assert_stmt
  : ASSERT test (',' test)?
  ;

del_stmt
  : DEL exprlist
  ;

pass_stmt
  : PASS
  ;

flow_stmt
  : break_stmt | continue_stmt | return_stmt | throw_stmt | yield_stmt
  ;

break_stmt
  : BREAK
  ;

continue_stmt
  : CONTINUE
  ;

return_stmt
  : RETURN testlist?
  ;

yield_stmt
  : yield_expr
  ;

throw_stmt
  : THROW (test (',' test (',' test))?)?
  ;

// URLs refer to directory structure within sandbox or component, or to
// a URL on the web from which a component can be downloaded.
url
  : protocol IDENTIFIER ('/' IDENTIFIER)*?
  ;

protocol
  : ('@component' | '@sandbox' | 'http' 's'?) '://'
  ;

import_stmt
  : IMPORT url (AS IDENTIFIER)?
  ;

compound_stmt
  : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef
  ;

if_stmt
  : IF test ':' suite (ELIF test ':' suite)* (ELSE ':' suite)?
  ;

while_stmt
  : WHILE test ':' suite
  ;

for_stmt
  : FOR exprlist IN testlist ':' suite
  ;

try_stmt
  : TRY ':' suite (except_clause ':' suite)+ (FINALLY ':' suite)?
  ;

with_stmt
  : WITH with_item (',' with_item)*  ':' suite
  ;

with_item
  : test (AS expr)
  ;

// NB compile.c makes sure that the default except clause is last
except_clause
  : CATCH (test ((AS | ',') test)?)?
  ;

suite
  : simple_stmt | LINE_BREAK INDENT stmt+ DEDENT
  ;

// A "test" is an expression that might or might not be wrapped in boolean
// logic. The boolean operator precedence is reflected in how the nesting
// is done here.

test
  : or_test (IF or_test ELSE test)? | lambdef
  ;

// OR is the lowest-priority boolean expr; AND is bound
// more tightly.
or_test
  : and_test (OR and_test)*
  ;

// AND has a higher priority than OR, but lower than NOT.
and_test
  : not_test (AND not_test)*
  ;

// NOT has a higher priority than AND.
not_test
  : NOT not_test | comparison
  ;

comparison
  : expr (comp_op expr)*
  ;

comp_op
  : '<'|'>'|'=='|'>='|'<='|'!='|IN|NOT IN|'is'|'is' 'not'
  ;

expr
  : xor_expr ('|' xor_expr)*
  ;

xor_expr
  : and_expr ('^' and_expr)*
  ;

and_expr
  : shift_expr ('&' shift_expr)*
  ;

shift_expr
  : arith_expr (('<<'|'>>') arith_expr)*
  ;

arith_expr
  : term (('+'|'-') term)*
  ;

term
  : factor (('*'|'/'|'%'|'//') factor)*
  ;

factor
  : ('+'|'-'|'~') factor | power
  ;

power
  : atom trailer* ('**' factor)?
  ;

atom
  : ('(' (yield_expr|testlist_comp)? ')' | '[' listmaker? ']' | '{' dictorsetmaker? '}' | '`' testlist1 '`' | IDENTIFIER | number | STR_LITERAL+)
  ;

listmaker
  : test ( list_for | (',' test)* ','? )
  ;

testlist_comp
  : test ( comp_for | (',' test)* ','? )
  ;

// A mark is something like:
//   +pure
//   +text(1, 50)
// Marks can appear between identifiers and their values.
mark
  : ('-' | '+') IDENTIFIER ('(' arglist ')')?
  ;

marks
  : mark+
  ;

funcdef
  : FUNC IDENTIFIER ':' LINE_BREAK suite
  ;

// We recognize function invocations by the presence of args at the end
// of an identifier.
args
  : '(' arglist? ')'
  ;

arglist
  : arg (',' arg)*
  ;

// An arg is something passed to a called function. Do not confuse with a
// param, which is the definition of what might be passed.
arg
  : (IDENTIFIER ASSIGN)? test
  ;

lambdef
  : 'lambda' 'FIXME' ':' test
  ;

trailer
  : '(' arglist? ')' | '[' subscriptlist ']' | '.' IDENTIFIER
  ;

subscriptlist
  : subscript (',' subscript)* ','?
  ;

subscript
  : '.' '.' '.' | test | test? ':' test? sliceop?
  ;

sliceop
  : ':' test?
  ;

exprlist
  : expr (',' expr)* ','?
  ;

testlist
  : test (',' test)* ','?
  ;

dictorsetmaker
  : ( (test ':' test (comp_for | (',' test ':' test)* ','?)) | (test (comp_for | (',' test)* ','?)) )
  ;

classdef
  : CLASS IDENTIFIER ':' suite
  ;

// The reason that keywords are test nodes instead of IDENTIFIER is that using IDENTIFIER
// results in an ambiguity. ast.c makes sure it's a IDENTIFIER.
argument
  : test comp_for? | test ASSIGN test
  ;

list_iter
  : list_for | list_if
  ;

list_for
  : FOR exprlist IN testlist list_iter?
  ;

list_if
  : IF test list_iter?
  ;

comp_iter
  : comp_for | comp_if
  ;

comp_for
  : FOR exprlist IN or_test comp_iter?
  ;

comp_if
  : IF test comp_iter?
  ;

testlist1
  : test (',' test)*
  ;

yield_expr
  : YIELD testlist?
  ;

number
  : INTEGER_LITERAL | FLOAT_LITERAL
  ;

INTEGER_LITERAL
  : DECIMAL_INTEGER_LITERAL | HEX_INTEGER_LITERAL | OCT_INTEGER_LITERAL | BINARY_INTEGER_LITERAL
  ;

fragment
DECIMAL_INTEGER_LITERAL
  : DECIMAL_NUMERAL INTEGER_TYPE_SUFFIX?
  ;

fragment
HEX_INTEGER_LITERAL
  : HEX_NUMERAL INTEGER_TYPE_SUFFIX?
  ;

fragment
OCT_INTEGER_LITERAL
  : OCT_NUMERAL INTEGER_TYPE_SUFFIX?
  ;

fragment
BINARY_INTEGER_LITERAL
  : BIN_NUMERAL INTEGER_TYPE_SUFFIX?
  ;

// Allow all integer literals to have "L" at the end
// to force 64-bit.
fragment
INTEGER_TYPE_SUFFIX
  : [lL]
  ;

fragment
DECIMAL_NUMERAL
  : '0' | NON_ZERO_DIGIT (DIGITS? | UNDERSCORES DIGITS)
  ;

fragment
DIGITS
  : DIGIT (DIGITS_AND_UNDERSCORES? DIGIT)?
  ;

fragment
DIGIT
  : '0' | NON_ZERO_DIGIT
  ;

fragment
NON_ZERO_DIGIT
  : [1-9]
  ;

fragment
DIGITS_AND_UNDERSCORES
  : DIGIT_OR_UNDERSCORE+
  ;

fragment
DIGIT_OR_UNDERSCORE
  : DIGIT | '_'
  ;

// Like java, allow _ as a separator or grouping char between digits
// for those who'd like improved readability of numeric literals.
fragment
UNDERSCORES
  : '_'+
  ;

fragment
HEX_NUMERAL
  : '0' [xX] HEX_DIGITS
  ;

fragment
HEX_DIGITS
  : HEX_DIGIT (HEX_DIGITS_AND_UNDERSCORES? HEX_DIGIT)?
  ;

fragment
HEX_DIGIT
  : [0-9a-fA-F]
  ;

fragment
HEX_DIGITS_AND_UNDERSCORES
  : HEX_DIGIT_OR_UNDERSCORE+
  ;

fragment
HEX_DIGIT_OR_UNDERSCORE
  : HEX_DIGIT | '_'
  ;

fragment
OCT_NUMERAL
  : '0' UNDERSCORES? OCT_DIGITS
  ;

fragment
OCT_DIGITS
  : OCT_DIGIT (OCT_DIGITS_AND_UNDERSCORES? OCT_DIGIT)?
  ;

fragment
OCT_DIGIT
  : [0-7]
  ;

fragment
OCT_DIGITS_AND_UNDERSCORES
  : OCT_DIGIT_OR_UNDERSCORE+
  ;

fragment
OCT_DIGIT_OR_UNDERSCORE
  : OCT_DIGIT | '_'
  ;

fragment
BIN_NUMERAL
  : '0' [bB] BIN_DIGITS
  ;

fragment
BIN_DIGITS
  : BIN_DIGIT (BIN_DIGIT_AND_UNDERSCORES? BIN_DIGIT)?
  ;

fragment
BIN_DIGIT
  : [01]
  ;

fragment
BIN_DIGIT_AND_UNDERSCORES
  : BIN_DIGIT_OR_UNDERSCORE+
  ;

fragment
BIN_DIGIT_OR_UNDERSCORE
  : BIN_DIGIT | '_'
  ;

// ¤3.10.2 Floating-Point Literals

FLOAT_LITERAL
  : DECIMAL_FLOAT_LITERAL | HEX_FLOAT_LITERAL
  ;

fragment
DECIMAL_FLOAT_LITERAL
  : DIGITS '.' DIGITS? EXPONENT_PART? FLOAT_TYPE_SUFFIX?
  | '.' DIGITS EXPONENT_PART? FLOAT_TYPE_SUFFIX?
  | DIGITS EXPONENT_PART FLOAT_TYPE_SUFFIX?
  | DIGITS FLOAT_TYPE_SUFFIX
  ;

fragment
EXPONENT_PART
  : EXPONENT_INDICATOR SIGNED_INTEGER
  ;

fragment
EXPONENT_INDICATOR
  : [eE]
  ;

fragment
SIGNED_INTEGER
  : SIGN? DIGITS
  ;

fragment
SIGN
  : [+-]
  ;

fragment
FLOAT_TYPE_SUFFIX
  : [fFdD]
  ;

fragment
HEX_FLOAT_LITERAL
  : HEX_SIGNIFICAND BINARY_EXPONENT FLOAT_TYPE_SUFFIX?
  ;

fragment
HEX_SIGNIFICAND
  : HEX_NUMERAL '.'?
  | '0' [xX] HEX_DIGITS? '.' HEX_DIGITS
  ;

fragment
BINARY_EXPONENT
  : BINARY_EXPONENT_INDICATOR SIGNED_INTEGER
  ;

fragment
BINARY_EXPONENT_INDICATOR
  : [pP]
  ;

IDENTIFIER
  : [a-z_][a-z_0-9]*
  ;

FOR: 'for';
IF: 'if';
CLASS: 'class';

CHAR_LITERAL
  : '\'' ONE_CHAR '\''
  | '\'' ESCAPE_SEQ '\''
  ;

fragment
ONE_CHAR
  : ~['\\]
  ;

// String Literals

STR_LITERAL
  : '"' STR_CHARS? '"'
  ;

fragment
STR_CHARS
  : STR_CHAR+
  ;

fragment
STR_CHAR
  : ~["\\] | ESCAPE_SEQ
  ;

// ¤3.10.6 Escape Sequences for Character and String Literals

fragment
ESCAPE_SEQ
  : '\\' [btnfr"'\\]
  | UNI_ESCAPE
  ;

fragment
UNI_ESCAPE
  : '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
  ;

fragment
ZERO_TO_3
  : [0-3]
  ;

// Separators

LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
LBRACK : '[';
RBRACK : ']';
SEMI : ';';
COMMA : ',';
DOT : '.';

// Operators

ASSIGN : '=';
GT : '>';
LT : '<';
BANG : '!';
TILDE : '~';
QUESTION : '?';
COLON : ':';
EQUAL : '==';
LE : '<=';
GE : '>=';
NOTEQUAL : '!=';
INC : '++';
DEC : '--';
ADD : '+';
SUB : '-';
MUL : '*';
DIV : '/';
BITAND : '&';
BITOR : '|';
CARET : '^';
MOD : '%';

ADD_ASSIGN : '+=';
SUB_ASSIGN : '-=';
MUL_ASSIGN : '*=';
DIV_ASSIGN : '/=';
AND_ASSIGN : '&=';
OR_ASSIGN : '|=';
XOR_ASSIGN : '^=';
MOD_ASSIGN : '%=';
LSHIFT_ASSIGN : '<<=';
RSHIFT_ASSIGN : '>>=';
URSHIFT_ASSIGN : '>>>=';
    
WS  // only within a statement
  : [ \t]+ -> skip
  ;

LINE_BREAK // statement separator in most cases
  : [\r\n\u000C]
  ;

COMMENT
  : '##' .*? '##' -> skip
  ;

LINE_COMMENT
  : '#' ~[\r\n]* -> skip
  ;

// Keywords
BREAK: 'break';
RETURN: 'return';
IMPORT: 'import';
WHILE: 'while';
ELSE: 'else';
IN: 'in';
TRY: 'try';
ELIF: 'elif';
FINALLY: 'finally';
WITH: 'with';
AS: 'as';
CATCH: 'catch';
YIELD: 'yield';
TRUE: 'true';
FALSE: 'false';
NULL: 'null';
AND: 'and';
OR: 'or';
NOT: 'not';
ASSERT: 'assert';
DEL: 'del';
PASS: 'pass';
CONTINUE: 'continue';
THROW: 'throw';
FUNC: 'func';