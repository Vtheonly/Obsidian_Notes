---
tags: [structure-aware, architecture, grammar]
---

# Grammar-Guided Decoders

> **Definition.** A *grammar-guided decoder* restricts token generation at each step so that the output is always a valid string of a given grammar.

## Mechanism

At each step:

1. Run a parser on the partial output to get its set of possible parser states.
2. For each state, compute the set of valid next tokens.
3. Mask out invalid tokens in the model's logits (set them to $-\infty$).

## Example: JSON

If the partial output is `{"name": "`, the parser is in state `inside-string`. Valid next tokens are characters; `}` is invalid until the string is closed. The mask enforces this.

## Example: LaTeX

The parser tracks the brace stack. If the partial output is `\frac{a`, the next token must close the brace (`}`) or continue the numerator. A bare `\frac` with no following `{` is invalid.

## Strength

Hard guarantee on **syntactic** validity. The output is always parseable.

## Limitations

- Only guarantees syntax, not semantics. (`{"name": 5}` is syntactically valid JSON but maybe semantically wrong if `name` should be a string.)
- Grammar can be expensive to compile into a mask.
- Some grammars are ambiguous, requiring parser state sets rather than single states.

See [[Grammar Constrained Generation]], [[Constrained Decoding]].

## Related Concepts

- [[Grammar Constrained Generation]]
- [[Constrained Decoding]]
- [[Structural Constraints]]
