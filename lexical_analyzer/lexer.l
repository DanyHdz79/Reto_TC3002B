%{
#include <stdio.h>
%}

digit [0-9]
letter [a-zA-Z]
spaces \t|\b|\r\n|\'|\\|\"|\$|


keywords alignas|alignof|auto|bool|break|case|char|const|constexpr|continue|default|do|double|else|enum|extern|false|float|for|goto|if|inline|int|long|nullptr|register|restrict|return|short|signed|sizeof|static|static_assert|struct|switch|thread_local|true|typedef|typeof|typeof_unqual|union|unsigned|void|volatile|while 
/* |_Alignas|_Alignof|_Atomic|_BitInt|_Bool|_Complex|_Decimal128|_Decimal32|_Decimal64|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local */

operators &&|&=|&|\||~|!|!=|\|\||\|=|^|^=\|\(|\)|\{|\}|\[|\]|#|##|\+|\-|\/|\%|\<|\>\:|\;|\,|\.|\?|\*
name (({letter}+({digit}+|{letter}+|\_)*)|(\_+({digit}+|{letter}+)+({digit}+|{letter}+|\_)*))

%%
[\-|\+]?{digit}+                                                                                {printf("int");}
[\-|\+]?{digit}*\.{digit}+                                                                      {printf("float");}
{operators}                                                                                     {printf("operator");}
{keywords}                                                                                      {printf("keyword");}
\".*\"                                                                                          {printf("string");}
{name}                                                                                          {printf("variable");}
{name}\(\)                                                                                      {printf("function");}
%%