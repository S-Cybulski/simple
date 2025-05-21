### 1.0 Defining the Language

statement -> expression | keyword expression | identifier equality expression

expression -> literal | grouping | unary | binary

literal -> NUMBER | STRING | "TRUE" | "FALSE" | NULL

grouping -> "(" expression ")"

unary -> ("-" | "!") expression

binary -> expression operator expression


operator -> "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/" | "AND" | "OR" 

Arithmetic operations:

Binary add (+) 
Binary subtract (-) 
Binary multiply (*) 
Binary division (/) 
Unary negation (-)

Binary and (AND) 
Binary or (OR) 
Unary negation (!)

Global variables (any alphanumeric key starting with an alpha, that is not a keyword)

IF expression THEN
    Path 1
ELSE
    Path 2
ENDIF



WHILE expression THEN
    Loop body
ENDWHILE

