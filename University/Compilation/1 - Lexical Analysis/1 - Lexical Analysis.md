
## Chapter 2: Lexical Analysis

### 1. Introduction

Lexical analysis involves reading a source file character by character to form **tokens** (words) and verifying that they belong to the language using a regular grammar. A token belonging to the language is coded and possibly inserted into the symbol table. The result of this analysis is a sequence of tuples of tokens and possibly a list of lexical errors. Each tuple includes the token, its code, and its lexical unit (its nature).

### 2. Definitions

* **Lexeme or Token:** A sequence of characters. For example, "77", "c1", etc.
* **Lexical Unit:** The nature of the lexeme (useful for syntax). For example, "integer constant", "identifier", etc.
* **Attribute:** Information useful for semantics. For example, value "77", pointer to the symbol table, etc.

### 3. Functionalities of a Lexical Analyzer

A lexical analyzer (lexical scanner, lexer) commonly called a lexer forms tokens at the request of the parser. To achieve this, it requires several functions:

* **Perform pre-processing of the source program:** Before forming tokens, the analyzer may need to perform certain tasks, not necessarily all of them, for example:
    * Processing macros, includes, and defines in C, etc.
    * Handling whitespace
    * Numbering lines
    * Removing comments (paying attention to line management)

* **Form the tokens:** Before forming tokens, it is necessary to:
    * **Define the tokens (by lexical unit) and their separators:**
        * **Keywords:** These must be listed (if, for, int, etc.)
        * **Identifier:** Define the structure (a sequence of digits and letters starting with a letter)
        * **Integer constant:** A sequence of digits
        * **Real constant:** A sequence of digits containing at least one decimal point; scientific notation can also be integrated
        * **String constant:** A sequence of characters enclosed in double quotes
        * **Operator:** These must be listed (<, >, not, etc.)
        * **Punctuation symbol:** , ; ( ) [ } etc.
        * **Etc.**

    * **Separators:**
        * **Keywords:** As with an identifier, any character that is not alphanumeric
        * **Integer or real constant:** Any character that is not a digit or a decimal point
        * **Etc.**

* **Encode the tokens**

* **Insert the tokens into the symbol table.**

* **Locate and report lexical errors**

### 4. Complexity of Lexical Analysis

Some factors complicate the construction of lexical analyzers. For example, certain languages have non-reserved keywords, and/or whitespace is not significant, while in others, the placement within the line is crucial.

One solution to the problem of non-reserved words is to find the character that can determine the lexical unit and thus the token. To achieve this, it is sufficient to use two buffers and a pair of pointers to manage the lookahead character problem.

### 5. Construction of a Lexical Analyzer

Lexical analysis should be based on extended regular expressions and finite state automata. There are several methods to implement an analyzer, with a deterministic method being preferred. Here are the steps to follow:

1. **List all tokens (or token families) and their separators.**
2. **Write a regular expression for each listed entity.**
3. **Construct a finite state automaton for each regular expression.**
4. **Unite all the automata found in step 3.**
5. **Make the union automaton deterministic.**
6. **Minimize the deterministic automaton.**
7. **Implement the analyzer:**
   - Find the appropriate data structure for storing the automaton.
   - Write procedures for all listed functionalities and for each state of the minimized automaton, specify the procedures to execute.
   - Write the main program.

### 6. Lexical Analyzer Generators

To facilitate the implementation of a lexer, several generators exist. Examples include JLex for Java, Lex, and Flex for C. Lex and Flex practically implement the method described in section 5, specifically steps 3, 4, 5, 6, and partially 7.


**Introduction:**

- **Lexical Analysis** is the first phase of compilation. Its main task is to break down the source code text into a set of units called "tokens" (more accurately termed "lexemes"). These tokens represent fundamental building blocks in the program.

- The term "lexeme" signifies a lexical unit that the syntax analyzer (parser) will use. This interaction is typically implemented by making the lexical analyzer a subprogram (or part) of the syntax analyzer. When the syntax analyzer requests the "next lexical unit," the lexical analyzer reads the input characters until it can identify the next lexeme.

- In this process, the lexical analyzer reads and identifies tokens (lexemes), which are then passed to the syntax analyzer for further processing.

- A "lexical unit" refers to a unit of code in the program source that the lexical analyzer recognizes as a token or lexeme.

- The main purpose of lexical analysis is to prepare the source code for the subsequent phases of compilation, such as syntax analysis and semantic analysis. It involves identifying and categorizing different language elements, like keywords, identifiers, literals, and operators, so that the compiler can work with them effectively.

- The **"Symbol Table"** is a data structure that stores information about identifiers (variables, functions, etc.) declared in the program. This information is crucial for type checking, scope resolution, and code generation in later phases of compilation.

- In addition to its primary task of tokenizing the source code, the lexical analyzer can perform several secondary tasks:

  1. **Comment and Whitespace Removal:**
     The lexical analyzer can eliminate comments and whitespace from the source code. Comments are text in the code that are meant for human readability and are typically ignored by the compiler. Whitespace includes spaces, tabs, and newline characters. Removing comments and whitespace makes the source code more compact and easier for subsequent phases of compilation to process.

  2. **Error Message Linking:**
     The lexical analyzer can link error messages generated by the compiler back to the source code. For example, if there's a lexical error, the lexical analyzer can associate the error message with the line number in the source code where the error occurred. This makes it easier for programmers to identify and fix issues in their code, as error messages can be directly related to the relevant part of the source code.

  3. **Preprocessing of the Source Code:**
     Before forming tokens, the lexical analyzer may need to perform various preprocessing tasks, including handling macros, includes, and defines (common in the C programming language), handling whitespace characters, managing line numbering, and removing comments while ensuring proper line management.

  4. **Token Formation:** 
     To form tokens, the lexical analyzer performs the following steps:
     
     - **Defining Tokens:** This involves specifying the keywords used in the programming language (e.g., "if," "for," "int," etc.) and categorizing the source code into these predefined tokens.
     - **Token Categorization:** The source code is categorized into these predefined tokens.
     - **Attribute Determination:** Attributes associated with each token are determined. For instance, when identifying an integer constant, the attribute would be the actual integer value.

**Grammar of Type 2 (Context-Free Grammar):**
   - Lexical analysis operates based on a grammar, and this grammar falls into the category of Type 2 in the Chomsky hierarchy.
   - Type 2 grammars, also known as context-free grammars, describe a set of rules for generating strings in a language. These rules define the syntax of the language without considering the context in which symbols appear.
   - In the context of lexical analysis, a context-free grammar is employed to define the structure and rules of the programming language.

**Generation of Intermediate Code:**
   - Lexical analysis is a phase in the compilation process where the source code is broken down into tokens, which are the smallest units in a programming language (e.g., keywords, identifiers, operators).
   - The tokens are then used to generate intermediate code. Intermediate code is an abstraction that sits between the high-level source code and the low-level machine code. It is a representation that makes it easier to perform subsequent optimizations and transformations.

**Syntax Tree Spanning Options - Infix, Postfix, or Abstract:**
   - After generating intermediate code, the next step involves creating a syntax tree to represent the structure of the program.
   - The syntax tree can be spanned in different ways, and this choice can impact how the code is further processed:
      - **Infix Notation:** The syntax tree follows the typical mathematical notation with operators between operands (e.g., `2 + 3`).
      - **Postfix (or Reverse Polish) Notation:** The operators come after their operands (e.g., `2 3 +`).
      - **Abstract Syntax Tree (AST):** An abstract representation that captures the essential structure and semantics of the code without necessarily preserving the exact syntax. ASTs are often used for optimization and code generation.

**Conclusion:**
The lexical analysis phase is responsible for tokenizing the source code and providing a stream of lexemes (lexical units) to the syntax analyzer, facilitating the parsing and understanding of the program's structure. Using context-free grammar, the lexical analyzer breaks down the source code into tokens, generates intermediate code, and constructs a syntax tree. This phase also performs additional tasks such as removing comments and whitespace, linking error messages to the source code, and preprocessing the source code, all of which contribute to a more efficient and developer-friendly compilation process.


**Introduction:**

- **Lexical Analysis** is the first phase of compilation. Its main task is to break down the source code text into a set of units called "tokens" (more accurately termed "lexemes"). These tokens represent fundamental building blocks in the program.

- The term "lexeme" signifies a lexical unit that the syntax analyzer (parser) will use. This interaction is typically implemented by making the lexical analyzer a subprogram (or part) of the syntax analyzer. When the syntax analyzer requests the "next lexical unit," the lexical analyzer reads the input characters until it can identify the next lexeme.

- In this process, the lexical analyzer reads and identifies tokens (lexemes), which are then passed to the syntax analyzer for further processing.

- A "lexical unit" refers to a unit of code in the program source that the lexical analyzer recognizes as a token or lexeme.

The main purpose of lexical analysis is to prepare the source code for the subsequent phases of compilation, such as syntax analysis and semantic analysis. It involves identifying and categorizing different language elements, like keywords, identifiers, literals, and operators, so that the compiler can work with them effectively.

The "Symbol Table" is also mentioned, which is a data structure that stores information about identifiers (variables, functions, etc.) declared in the program. This information is crucial for type checking, scope resolution, and code generation in later phases of compilation.

In summary, the lexical analysis phase is responsible for tokenizing the source code and providing a stream of lexemes (lexical units) to the syntax analyzer, facilitating the parsing and understanding of the program's structure.

**Lexical Unit (Unité lexicale):**
- **Definition:** A lexical unit is a sequence of characters that has a collective meaning. In other words, it is a group of characters that, when considered together, represents a specific concept or entity in the source code.
- **Example:** In the context of programming languages, symbols like `<`, `>`, and `=` are relational operators, and the lexical unit for them could be named "OPREL" (short for "operator relational").

**Pattern (Modèle):**
- **Definition:** A pattern (or model) is a rule associated with a lexical unit that describes the set of strings in the program that can correspond to that lexical unit. It defines the structure or format that a valid lexeme should follow.
- **Example:** For an identifier (e.g., variable name) in the C programming language, the pattern might specify that it should consist of characters such as letters, digits, or certain symbols, and it must start with a letter. Valid lexemes for this lexical unit could be "a," "b," "montant," "tot1," and so on.

**Lexeme (Lexème):**
- **Definition:** A lexeme is any sequence of characters in the program's source code that matches the pattern of a lexical unit. It is essentially an instance of a lexical unit in the source code.
- **Example:** If the pattern for an identifier is as described earlier, then "a," "b," "montant," and "tot1" are examples of lexemes for the "IDENT" (identifier) lexical unit.

**Regular Expressions:** To describe the pattern (model) of a lexical unit, regular expressions are commonly used. Regular expressions are a powerful tool for specifying patterns in text, and they can define the structure and format of valid lexemes for various lexical units.

**Token:**
A token is a sequence of characters that can be treated as a unit in the grammar of programming languages. Tokens are the fundamental building blocks of code and are used for language parsing and analysis. They include various types of tokens, such as:
   - **Type tokens:** (e.g., identifiers, numbers, real numbers, etc.)
   - **Punctuation tokens:** (e.g., keywords like "if," "void," "return," etc.)
   - **Alphabetic tokens:** (keywords like "for," "while," "if," etc.)
   - **Identifiers:** (e.g., variable names, function names, etc.)
   - **Operators:** (e.g., '+', '++', '-')
   - **Separators:** (e.g., ',', ';')

Tokens are used to represent specific language constructs and are crucial for understanding the structure of code in programming languages.

**Non-Tokens:**
Non-tokens are characters or sequences of characters that are not treated as fundamental units by the language's grammar and are not part of the code's structure. Examples of non-tokens include:
   - **Comments**
   - **Preprocessor directives:** (used in languages like C and C++)
   - **Macros**
   - **Blanks (whitespace)**
   - **Tabs**
   - **Newlines**

Non-tokens do not play a direct role in the syntax or structure of the programming language and are often used for documentation, readability, or pre-processing tasks.

**Lexeme:**
A lexeme is the sequence of characters matched by a pattern to form the corresponding token or a sequence of input characters that comprises a single token. In other words, a lexeme is the actual sequence of characters that represents a specific language construct. For example, the lexemes in the provided examples are:
   - "float" (lexeme for a type token)
   - "abs_zero_Kelvin" (lexeme for an identifier)
   - "=" (lexeme for an operator)
   - "273" (lexeme for a number)
   - ";" (lexeme for a separator)

**Secondary Tasks of Lexical Analysis:**
1. **Comment and Whitespace Removal:** The lexical analyzer can eliminate comments and whitespace from the source code. Comments are text in the code that are meant for human readability and are typically ignored by the compiler. Whitespace includes spaces, tabs, and newline characters. Removing comments and whitespace makes the source code more compact and easier for subsequent phases of compilation to process.

2. **Error Message Linking:** The lexical analyzer can link error messages generated by the compiler back to the source code. For example, if there's a lexical error, the lexical analyzer can associate the error message with the line number in the source code where the error occurred. This makes it easier for programmers to identify and fix issues in their code, as error messages can be directly related to the relevant part of the source code.

3. **Preprocessing of the Source Code:** Before forming tokens, the lexical analyzer may need to perform various preprocessing tasks, including handling macros, includes, and defines (common in the C programming language), handling whitespace characters, managing line numbering, and removing comments while ensuring proper line management.

4. **Token Formation:** To form tokens, the lexical analyzer performs the following steps:
   - **Defining Tokens:** This involves specifying the keywords used in the programming language (e.g., "if," "for," "int," etc.) and categorizing the source code into these predefined tokens.
   - **Token Categorization:** The source code is categorized into these predefined tokens.
   - **Attribute Determination:** Attributes associated with each token are determined. For instance, when identifying an integer constant, the attribute would be the actual integer value.

These secondary tasks contribute to making the compilation process more efficient and developer-friendly. Comment and whitespace removal reduces the size of the code and simplifies its structure, while error message linking enhances the ability to debug and correct issues by providing context within the source code.
