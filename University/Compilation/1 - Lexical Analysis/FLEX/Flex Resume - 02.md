
# Flex (Lexical Analyzer Generator)

## Basic Structure
A Flex program (`.l` file) consists of three main sections:
```
declarations
%%
translation rules
%%
auxiliary procedures
```

### 1. Declarations Section
- Contains:
  - Variable declarations
  - Manifest constants
  - Regular definitions
  - Note: Manifest constants are identifiers representing constants (e.g., `#define PIE 3.14`)

### 2. Translation Rules Section
Format:
```
p1 {action 1}
p2 {action 2}
p3 {action 3}
```
- Each `p` represents a regular expression
- Each `action` is a C program fragment
- Actions define analyzer behavior when pattern matches lexeme

### 3. Auxiliary Procedures Section
- Contains needed procedures for actions
- Can be alternatively compiled separately and loaded with analyzer

## Regular Expressions in Flex

### Basic Operators
| Operator | Description |
|----------|-------------|
| x or "x" | Single character |
| r1r2 | Concatenation of regex r1 and r2 |
| r* | Kleene star (zero or more) |
| r+ | Positive closure (one or more) |
| r? | Optional (equivalent to (r\|ε)) |

### Character Sets
| Expression | Description |
|------------|-------------|
| [xyz] | One character among x, y, or z |
| [c-f] | One character in range c to f |
| . | Any character except newline |
| [^] | Any character except those in brackets |

### Quantifiers
| Expression | Description |
|------------|-------------|
| r{n,m} | n to m occurrences of r |
| r{n,} | n or more occurrences of r |
| r{n} | Exactly n occurrences of r |

### Special Operators
| Expression | Description |
|------------|-------------|
| r1\|r2 | Union of r1 and r2 |
| r1/r2 | r1 when followed by r2 |
| ^r | r at line start |
| $r | r at line end |

### Special Characters
- `\t` or "\t": Tab character
- `\n` or "\n": Newline character
- `{}`: Definition reference operator
- `()`: Grouping operator

### Important Notes
1. **Escape Characters**:
   - Use `\` and "..." to designate Flex operators as literal characters
   - `\`, `^`, and `$` cannot appear in parentheses or regular definitions

2. **Inside Square Brackets**:
   - `\` maintains its meaning
   - `-` acts as range operator when in middle position
   - `-` is literal at start or end


---



