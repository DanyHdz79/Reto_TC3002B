%{
#include <stdio.h>
#include <dirent.h> 
%}

digit           [0-9]
letter          [a-zA-Z]
loop            for|while|do
conditional     if|else|switch|case|default
keyword         alignas|alignof|auto|bool|break|const|constexpr|continue|double|enum|extern|false|goto|inline|long|nullptr|register|restrict|return|short|signed|sizeof|static|static_assert|struct|thread_local|true|typedef|typeof|typeof_unqual|union|unsigned|void|volatile|public|private|sleep|system|printf|fopen|fgets|NULL|perror
name            (({letter}+({digit}+|{letter}+|\_)*)|(\_+({digit}+|{letter}+)+({digit}+|{letter}+|\_)*))
function        (({keyword}[ ])*{name}\(\))
skip            (#.*)|(\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/)|(\/\/.*)|\n
int_number      [\-|\+]?{digit}+
float_number    [\-|\+]?{digit}*\.{digit}+
arithmetic      [\+\-\*\/\%\~]
arithmetic_operation ({int_number}|{float_number}|{name}){arithmetic}({int_number}|{float_number}|{name})

%%
int                                         {printf("int ");}
float                                       {printf("float ");}
char                                        {printf("char ");}
{loop}                                      {printf("loop ");}
{conditional}                               {printf("conditional ");}
{function}                                  {printf("function ");}
{arithmetic_operation}                      {printf("arithmetic_operation ");}
\t|\n                                       {printf(" ");}
{skip}\n                                    //do nothing
.                                                                      
%%



//lex ./../lexical_analyzer/lexer.l && gcc ./../lexical_analyzer/lex.yy.c -o lexer -ll
// func / loops / cond / int / float / char /  operaciones aritmeticas / 
