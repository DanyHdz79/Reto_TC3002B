%{
#include <stdio.h>
#include <dirent.h> 
%}

digit           [0-9]
letter          [a-zA-Z]
spaces          \t|\b|\r\n|\'|\\|\"|\$|
keyword         alignas|alignof|auto|bool|break|char|const|constexpr|continue|double|enum|extern|false|float|goto|inline|int|long|nullptr|register|restrict|return|short|signed|sizeof|static|static_assert|struct|thread_local|true|typedef|typeof|typeof_unqual|union|unsigned|void|volatile|public|private|sleep|system|printf|fopen|fgets|NULL|perror
                /* |_Alignas|_Alignof|_Atomic|_BitInt|_Bool|_Complex|_Decimal128|_Decimal32|_Decimal64|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local */
loop            for|while|do
conditional     if|else|switch|case|default 
operator        &&|&=|&|\||\~|!|!=|\|\||\|\^|\^\=|\[|\]|#|##|\+|\-|\/|\%|\<|\>\:|\;|\,|\.|\?|\*
name            (({letter}+({digit}+|{letter}+|\_)*)|(\_+({digit}+|{letter}+)+({digit}+|{letter}+|\_)*))
function        (({keyword}[ ])*{name}\(\))
skip            (#.*)|(\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/)|(\/\/.*)|\n

%%
[\-|\+]?{digit}+                                                                                {printf("int ");}
[\-|\+]?{digit}*\.{digit}+                                                                      {printf("float ");}
[\+\-\*\/\%\~]                                                                                  {printf("arithmetic ");}
\=                                                                                              {printf("assign ");}
\(|\)|\{|\}                                                                                     {printf("delimit ");}
\=\=|\!\=|\<|\>|\<\=|\>\=                                                                       {printf("comparison ");}
\!|\&\&|\|\|                                                                                    {printf("logical ");} 
;                                                                                               {printf("semicolon ");}
{operator}                                                                                      {printf("operator ");}
'[^\'\n\r]?'                                                                                    {printf("char ");}
\"[^\"]*\"                                                                                      {printf("string ");}
{function}                                                                                      {printf("function ");}
{keyword}                                                                                       {printf("keyword ");}
{loop}                                                                                          {printf("loop ");}
{conditional}                                                                                   {printf("conditional ");}
{name}                                                                                          {printf("variable ");}
\t                                                                                              {printf(" ");}
{skip}\n                                                                                         //do nothing
%%



//lex ./../lexical_analyzer/lexer.l && gcc ./../lexical_analyzer/lex.yy.c -o lexer -ll