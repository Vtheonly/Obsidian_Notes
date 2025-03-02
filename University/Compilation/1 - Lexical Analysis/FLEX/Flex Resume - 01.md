# Flex (Fast Lexer)

## Overview
Flex is a lexical analyzer generator that takes a source file (`.lex` or `.flex`) containing a lexical analyzer description and generates a C file named `lex.yy.c`. This file, when compiled with gcc, produces the executable lexical analyzer.

## How Flex Works
1. Takes description file containing regular expressions and actions
2. Generates a combined NFDA (union of all NFDAs from regular expressions)
3. Converts NFDA to DFA
4. Minimizes the DFA
5. Generates C code to simulate the minimal automaton

## The yylex Function
- Located in `lex.yy.c`
- Performs lexical analysis of lexemes
- No arguments, returns an integer (code of recognized lexical unit)
- By default:
  - Reads from standard input (stdin)
  - Writes to standard output (stdout)

## Program Structure
A Flex program consists of three sections:

```
%{
/* Inclusions and Declarations */
%}
/* Regular Expression Definitions */
%%
/* Rules */
%%
/* Auxiliary C Code */
```

### 1. Definitions Section
- File inclusions
- Global C declarations (variables, types, functions)
- Regular expression definitions

### 2. Rules Section
- Contains regular expressions for recognizing lexemes
- Specifies actions to execute
- Format:
```
regex_1 action_1
regex_2 action_2
...
regex_n action_n
```

### 3. Auxiliary Code Section
- Contains necessary C routines
- Implementation of required functionality

## Predefined Variables and Functions
- `yytext`: (char*) Current recognized lexeme
- `yyleng`: (int) Length of yytext
- `yylineno`: (int) Current line number
- `yyin`: (File*) Input file pointer (defaults to stdin)
- `yyout`: (File*) Output file pointer (defaults to stdout)
- `unputc(char)`: Returns character to input stream
- `main()`: Default contains only yylex call

## Flex Routines

### Action Rules
1. Empty action or `;` - lexeme is ignored
2. Unrecognized strings are copied to output by default
3. `|` means "same as next rule's action"

### Special Directives
- `ECHO`: Copies yytext to output file
- `REJECT`: Forces analyzer to use second-best applicable rule
- `yymore()`: Concatenates current lexeme instead of replacing
- `yyless(n)`: Returns all but first n characters to input stream
- `yyterminate()`: Ends analyzer execution

## Automaton Handling

### Stop Conditions
When multiple regular expressions can analyze the input string:
1. Rule recognizing longest match is chosen first
2. If equal length, first rule is chosen
3. If no final state reached, default action triggers

## Compilation Options
- `-d`: Debug mode
- `-s`: Suppresses Flex default rule
- `-t`: Writes generated code to stdout
- `-T`: Shows DFA information
- `-V`: Shows Flex version

## Example Usage

### Sample Lexical Analyzer
```c
%{
#include <stdlib.h>
%}
%%
alors |
finsi |
si |
sinon printf("%s : KEYWORD\n", yytext);
[a-zA-Z_][a-zA-Z_0-9]* printf("%s : IDENT\n", yytext);
[0-9]+ printf("%d : NBENT\n", atoi(yytext));
[ \t\n] ;
```

### Compilation Process
1. Write Flex code in `.lex` file
2. Compile with Flex compiler
3. Compile generated C file with gcc
4. Link with Flex library

### Running the Analyzer
- Input file can be redirected to the analyzer
- Output shows recognized lexemes and their types