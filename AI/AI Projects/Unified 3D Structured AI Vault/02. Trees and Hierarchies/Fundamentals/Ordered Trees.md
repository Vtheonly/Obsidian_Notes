---
tags: [trees, ordered]
---

# Ordered Trees

> An **ordered tree** is a tree in which the order of children of each node matters.

## Why Order Matters

For two trees to be equal as ordered trees, they must have the same nodes, same parent-child relations, **and** the same left-to-right ordering of children at every node.

| Tree A        | Tree B        | Equal as unordered? | Equal as ordered? |
| ------------- | ------------- | ------------------- | ----------------- |
| `(A (B C))`   | `(A (B C))`   | yes                 | yes               |
| `(A (B C))`   | `(A (C B))`   | yes                 | no                |
| `(A (B C D))` | `(A (D B C))` | no                  | no                |

## Where Ordered Trees Arise

- **Parse trees**: token order matters; `[1, 2, 3]` is not `[3, 2, 1]`.
- **HTML / XML**: child order matters; `<p>Hello <b>world</b></p>` is not `<p><b>world</b> Hello</p>`.
- **Code ASTs**: statement order matters; `x = 1; y = 2;` is not `y = 2; x = 1;`.
- **Building floor plans** (sometimes): room order along a corridor may matter for indexing.

## Where Unordered Trees Suffice

- BIM containment hierarchy: a wall contains its windows; the order of windows in the wall usually does not matter.
- File systems (mostly): directory contents are typically unordered.

## Implication for Generation

If your tree is ordered, your decoder must decide *both* the structure *and* the order. If unordered, you can canonicalize (e.g. sort children by some key) and only decide the structure.

See [[Tree Generation]], [[Tree Decoding]].

## Related Concepts

- [[Tree Terminology]]
- [[N-ary Trees]]
- [[Parse Trees]]
- [[Tree Generation]]
