### Turing Complete Language Parser and Interpreter

#### How to Run Interpreter:

From terminal and in root directory(/simple)

``` python3 source/simple.txt ```

or

``` python3 source/simple.txt example.txt```

##### Syntax:
1. keywords must all be capitalised e.g:
- PRINT
- IF
- ELSE
- WHILE
- TRUE
- FALSE
- INPUT
- AND
- OR

2. Variables can be named whatever without underscores or special characters.

3. Supported expressions:
- +, -, *, /
- AND, OR, !(unary negation)
- ==, !=, <, >, <=, >=
- ()

Example:
```
isRunning = TRUE
shoppingList = ""

WHILE (isRunning == TRUE) {
    item = INPUT("Add an item: ")
    IF (item == "") {
        isRunning = FALSE
    } ELSE {
        shoppingList = shoppingList + ", " + item
    }
}

PRINT shoppingList

```

#### Stage 1: Basic Calculator (0-20%):
The interpreter supports arithmetic expressions using:
- Real numbers(integers and decimals)
- Unary negation ('-')
- Parentheses for grouping e.g (5 + 3) * 2
- Binary operators: '+', '-', '*', '/'

Example File: calculator.txt

#### Stage 2: Boolean Logic (20-40%):
The interpreter supports boolean values (true and false) and operations:
- Comparison: '==', '!=', '<', '<=', '>', '>='
- Logical: 'AND', 'OR', '!'

Example File: boolean.txt

#### Stage 3: Text Values (40-50%):
String literals are enclosed in double quotes ("string"). The language supports:
- String concatenation with +
- String equality and inequality

Example File: string.txt

#### Stage 4: Global Data (50-60%):
Global variables can be created, read, updated and printed. variables types can include:
- Numbers
- Booleans
- Strings

Example File: variables.txt

#### Stage 5: Control Flow(60-80%):
The language supports:
- IF statements (with or without ELSE)
- WHILE loops
- INPUT("prompt") for user input
- Nested If statements

Example File: shopping.txt

