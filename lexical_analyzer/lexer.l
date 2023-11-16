%{
#include <stdio.h>
#include <dirent.h> 
%}

digit           [0-9]
letter          [a-zA-Z]
keyword         alignas|alignof|auto|bool|break|char|const|constexpr|continue|double|enum|extern|false|float|goto|inline|int|long|nullptr|register|restrict|return|short|signed|sizeof|static|static_assert|struct|thread_local|true|typedef|typeof|typeof_unqual|union|unsigned|void|volatile|public|private|sleep|system|printf|fopen|fgets|NULL|perror|scanf

loop            (for|while|do)([ ]*\(.*\))?
conditional     (if|else|switch|case|default)([ ]*\(.*\))?
name            (({letter}+({digit}+|{letter}+|\_)*)|(\_+({digit}+|{letter}+)+({digit}+|{letter}+|\_)*))
function        ((({keyword}|{pointer})[ ])*{name}\(.*\))|{keyword}\(.*\)              
skip            (#.*)|(\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/)|(\/\/.*)|return[ ]*.*\;
int_number      [\-|\+]?{digit}+
float_number    [\-|\+]?{digit}*\.{digit}+
arithmetic      [\+\-\*\/\%\~]
pointer         (int|float|char|FILE)[ ]*\*[ ]*{name}?
arithmetic_operation ({int_number}|{float_number}|{name})[ ]*{arithmetic}

%%
;                                           {printf("semicolon ");}
{loop}                                      {printf("loop ");}
{conditional}                               {printf("conditional ");}
{function}                                  {printf("function ");}
\"[^\"]*\"                                  {printf("string ");}
{pointer}                                   {printf("pointer ");}
{arithmetic_operation}                      {printf("arithmetic_operation ");}
int[ ]{name}                                {printf("int_variable ");}
float[ ]{name}                              {printf("float_variable ");}
char[ ]{name}                               {printf("char_variable ");}
\t|\n                                       {printf(" ");}
{skip}\n                                    //do nothing
{keyword}                                   {printf("keyword ");}
{name}                                      {printf("variable ");}
.                                                                      
%%


//lex ./../lexical_analyzer/lexer.l && gcc ./../lexical_analyzer/lex.yy.c -o lexer -ll
// func / loops / cond / int / float / char /  operaciones aritmeticas / 



