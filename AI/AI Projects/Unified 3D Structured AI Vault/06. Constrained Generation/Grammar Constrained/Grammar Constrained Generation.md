---
tags: [constrained-generation, grammar]
---

# Grammar-Constrained Generation

> **Definition.** *Grammar-constrained generation* restricts token generation so the output is always a valid string of a given formal grammar.

## How It Works

1. Compile the grammar into a parser (LR, LL, or Earley).
2. At each decoding step, run the parser on the partial output to get its set of possible states.
3. For each state, compute the set of valid next tokens.
4. Mask out invalid tokens in the model's logits.

## Example: JSON

Grammar:

```
value  -> object | array | string | number | true | false | null
object -> "{" (string ":" value ("," string ":" value)*)? "}"
array  -> "[" (value ("," value)*)? "]"
string -> """ char* """
```

If the partial output is `{"name":`, valid next tokens start a value: `"`, `[`, `{`, digit, `t`, `f`, `n`. Anything else is masked out.

## Strengths

- Hard guarantee on syntactic validity.
- Compatible with any autoregressive model.
- Cheap at inference (mask is computed incrementally).

## Limitations

- Only syntactic validity is guaranteed. Semantics still need separate checking.
- Compiling the grammar into a mask can be expensive for some grammars.
- Ambiguous grammars require tracking a set of states.

## Implementations

- **Outlines**: Python library for grammar-constrained generation.
- **llguidance / guidance**: similar idea, supports regex and CFG.
- **Custom**: integrate a parser into the model's decoding loop.

## Related Concepts

- [[Constrained Decoding]]
- [[Grammar Guided Decoders]]
- [[Schema Constrained Generation]]
