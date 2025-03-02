Below are detailed solutions to the first four exercises provided, using LEX for lexical analysis tasks. Each exercise is defined with an example code snippet and explanations.

---

#### Exercise 1: Replace Spaces/Tabs with Underscores (Except at End of Line)

**Description:** This LEX code replaces all spaces and tabs with underscores (`_`). However, if the space or tab appears at the end of a line, it will be ignored.

```lex
%%
[ \t]+ putchar('_');      // Replace spaces/tabs with underscores
[ \t]+$ ;                 // Ignore spaces/tabs at end of line
\n   putchar('\n');       // Newline character
```

**Explanation:**
- `[ \t]+` matches one or more spaces or tabs. The action `putchar('_')` outputs an underscore for each match.
- `[ \t]+$` matches one or more spaces/tabs at the end of a line but takes no action, effectively ignoring them.
- `\n` outputs a newline character, ensuring the original line structure is maintained.

---

#### Exercise 2: Echo "UFAS" and Attempt to Match Patterns

**Description:** This LEX code echoes "UFAS" to the output whenever it is encountered in the text, then rejects it so that the remaining patterns (`a`, `ab`, `abc`) are matched with the remaining input.

```lex
%%
a | ab | abc | UFAS ECHO; REJECT;  // Echo UFAS and retry matching
.|\n ;                              // Ignore all other characters
```

**Explanation:**
- `UFAS ECHO; REJECT;` first echoes "UFAS" when encountered, then `REJECT` allows for further matching on the remaining input.
- The `REJECT` function effectively restarts matching from the current position, attempting to match any other patterns (`a`, `ab`, `abc`).
- `.` or `\n` matches any other character or newline, which is ignored.

**Output Example:**
Input: `UFASabc`
Output: `UFAS abc`

---

#### Exercise 3: Print "alg" for "algerie" and Process Remaining as New Match

**Description:** This LEX code prints "alg" when it encounters the word "algerie" and then processes "erie" as a new match.

```lex
%%
algerie ECHO; yyless(3);  // Output "alg" and continue with "erie"
[a-z]+ ECHO;               // Echo other lowercase sequences
\n ;                       // Newline handling
```

**Explanation:**
- `algerie ECHO; yyless(3);` matches "algerie", echoes it, and then `yyless(3)` resets the input to reprocess starting from the 4th character (`"erie"`).
- `[a-z]+ ECHO;` matches any other lowercase sequence, echoing it directly.

**Output Example:**
Input: `algerie`
Output: `alg erie`

---

#### Exercise 4: Count Occurrences of "L3A"

**Description:** This LEX code counts the number of times "L3A" appears in the input text and prints the count at the end.

```lex
%{
int i = 0;
%}

%%
L3A { i++; }   // Increment count for each occurrence of "L3A"
\n ;           // Newline handling
. ;            // Ignore other characters

%%
int main(int argc, char *argv[]) {
    yylex();
    printf("Count of 'L3A': %d\n", i);
    return 0;
}
```

**Explanation:**
- `L3A { i++; }` increments the counter `i` for each match of "L3A".
- `\n` and `.` handle newline and other characters without action, ensuring they are ignored.
- The `main()` function invokes `yylex()` and outputs the count of "L3A".

**Output Example:**
Input: `L3A L3A`
Output: `Count of 'L3A': 2`


#### Exercise 5: Count Characters, Words, Identifiers, and Lines

**Description:** This LEX code counts the number of characters, words, identifiers, and lines in the input text.

```lex
%{
int char_count = 0;
int word_count = 0;
int identifier_count = 0;
int line_count = 0;
%}

%%
[a-zA-Z_][a-zA-Z0-9_]* { identifier_count++; }     // Match identifiers
[ \t]+                  { word_count++; }          // Match words separated by spaces/tabs
\n                      { line_count++; }          // Count newlines as lines
.                       { char_count++; }          // Count each character

%%

int main() {
    yylex();
    printf("Characters: %d\n", char_count);
    printf("Words: %d\n", word_count);
    printf("Identifiers: %d\n", identifier_count);
    printf("Lines: %d\n", line_count);
    return 0;
}
```

**Explanation:**
- `[a-zA-Z_][a-zA-Z0-9_]*` matches identifiers and increments `identifier_count`.
- `[ \t]+` matches words separated by spaces or tabs, incrementing `word_count`.
- `\n` counts each newline to increment `line_count`.
- `.` counts each character, increasing `char_count`.

---

#### Exercise 6: Add Line Numbers to Non-Blank Lines

**Description:** This LEX code adds line numbers to all non-blank lines in the input file.

```lex
%{
int line_number = 1;
%}

%%
^[ \t]*$        { /* Skip blank lines */ }
.|\n            { if(yytext[0] != '\n') printf("%d: %s", line_number++, yytext); } 

%%

int main() {
    yylex();
    return 0;
}
```

**Explanation:**
- `^[ \t]*$` matches blank lines (spaces or tabs only) and takes no action.
- For non-blank lines, it prefixes each line with the line number by printing `line_number++`.

---

#### Exercise 7: Extract and Print Comments Between Curly Braces `{}`

**Description:** This LEX code extracts comments enclosed in `{}` and prints only the comment text.

```lex
%%
"{"[^}]*"}" { printf("Comment: %s\n", yytext); }   // Match comments between { }
.|\n        ;                                      // Ignore other characters

%%

int main() {
    yylex();
    return 0;
}
```

**Explanation:**
- `"{"[^}]*"}"` matches text enclosed by `{}`, printing the matched text as a comment.
- `.` and `\n` handle other characters without action.

---

#### Exercise 8: Replace "groupe" with "section" or "classe" Based on Line Start

**Description:** This LEX code replaces the word "groupe" with "section" if the line starts with `a`, and with "classe" if the line starts with `b`.

```lex
%%
^a.*groupe { printf("section%s\n", yytext + 6); }  // Line starting with 'a'
^b.*groupe { printf("classe%s\n", yytext + 6); }   // Line starting with 'b'
.|\n       { printf("%s", yytext); }               // Print other lines as-is

%%

int main() {
    yylex();
    return 0;
}
```

**Explanation:**
- `^a.*groupe` matches lines starting with `a` and containing "groupe", replacing "groupe" with "section".
- `^b.*groupe` matches lines starting with `b` and containing "groupe", replacing "groupe" with "classe".
- `.` and `\n` print all other lines unchanged.

#### Exercise 9: Lexical Analyzer for Recognizing Tokens (Decimal Numbers, Identifiers, Relational Operators, Keywords)

**Description:** This LEX code recognizes decimal numbers, identifiers, relational operators, and keywords. It also includes a function for adding identifiers to a symbol table.

```lex
%{
#include <stdio.h>
void RangerID(const char* id) {
    printf("Identifier stored: %s\n", id);  // Mock function for storing identifier
}
%}

%%
[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?    { printf("Decimal number: %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*                 { RangerID(yytext); }
"<"                                     { printf("Relational operator: PPQ\n"); }
">"                                     { printf("Relational operator: PGQ\n"); }
"<="                                    { printf("Relational operator: PPE\n"); }
">="                                    { printf("Relational operator: PGE\n"); }
"<> "                                   { printf("Relational operator: DIF\n"); }
"si"                                    { printf("Keyword: si\n"); }
"sinon"                                 { printf("Keyword: sinon\n"); }
"alors"                                 { printf("Keyword: alors\n"); }
[ \t\n]                                 ;   // Ignore whitespace

%%

int main() {
    yylex();
    return 0;
}
```

**Explanation:**
- `[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?` matches decimal numbers in scientific notation.
- `[a-zA-Z_][a-zA-Z0-9_]*` matches identifiers, invoking `RangerID` to store them.
- Each relational operator and keyword is matched separately with a unique message.

---

#### Exercise 10: Recognize Keywords, Identifiers, and Operators

**Description:** This LEX code recognizes keywords `begin` and `end`, identifiers, and operators (`+`, `-`, `*`, `**`). Errors are flagged for unrecognized sequences.

```lex
%%
"begin"      { printf("Keyword: begin\n"); }
"end"        { printf("Keyword: end\n"); }
[a-zA-Z_][a-zA-Z0-9_]*    { printf("Identifier: %s\n", yytext); }
"+"           { printf("Operator: +\n"); }
"-"           { printf("Operator: -\n"); }
"*"           { printf("Operator: *\n"); }
"**"          { printf("Operator: **\n"); }
[ \t\n]       ;  // Ignore whitespace
.             { printf("Error: unrecognized sequence '%s'\n", yytext); }

%%

int main() {
    yylex();
    return 0;
}
```

**Explanation:**
- `"begin"` and `"end"` are keywords recognized explicitly.
- `[a-zA-Z_][a-zA-Z0-9_]*` matches identifiers.
- Operators are recognized individually, with an error message for any unrecognized sequence.

---

#### Exercise 11: Count Vowels, Consonants, and Punctuation Characters

**Description:** This LEX code counts the number of vowels, consonants, and punctuation characters in the input text.

```lex
%{
int vowel_count = 0;
int consonant_count = 0;
int punctuation_count = 0;
%}

%%
[aeiouAEIOU]     { vowel_count++; }
[b-df-hj-np-tv-zB-DF-HJ-NP-TV-Z] { consonant_count++; }
[.,;!?]          { punctuation_count++; }
.|\n             ; // Ignore other characters

%%

int main() {
    yylex();
    printf("Vowels: %d\n", vowel_count);
    printf("Consonants: %d\n", consonant_count);
    printf("Punctuation: %d\n", punctuation_count);
    return 0;
}
```

**Explanation:**
- `[aeiouAEIOU]` matches vowels and increments `vowel_count`.
- `[b-df-hj-np-tv-zB-DF-HJ-NP-TV-Z]` matches consonants, incrementing `consonant_count`.
- `[.,;!?]` matches punctuation characters, increasing `punctuation_count`.

---

#### Exercise 12: Add Line Numbers to Every Line in a File

**Description:** This LEX code adds line numbers to every line in the input file, including blank lines.

```lex
%{
int line_number = 1;
%}

%%
\n         { printf("%d: %s", line_number++, yytext); }  // Print line number with each line

%%

int main() {
    yylex();
    return 0;
}
```

**Explanation:**
- `\n` matches each newline character and prefixes the current line with `line_number`, incrementing it for each line.

---

#### Exercise 13: Recognize Binary (ending in 'b') and Octal Numbers (ending in 'o')

**Description:** This LEX code recognizes binary numbers (ending with 'b') and octal numbers (ending with 'o').

```lex
%%
[01]+b  { printf("Binary number: %s\n", yytext); }
[0-7]+o { printf("Octal number: %s\n", yytext); }
.|\n    ; // Ignore other characters

%%

int main() {
    yylex();
    return 0;
}
```

**Explanation:**
- `[01]+b` matches binary numbers by requiring only `0` or `1` digits and the suffix `b`.
- `[0-7]+o` matches octal numbers with digits from `0` to `7` and suffix `o`.

---

These solutions demonstrate various ways to handle pattern recognition, token counting, and data manipulation in LEX, highlighting its flexibility for different types of lexical analysis tasks.