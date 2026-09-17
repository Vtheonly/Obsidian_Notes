---
tags: [implementation, tree-decoder]
---

# Tree Decoder Reference Implementation

A simple reference for a tree decoder. This is illustrative; production code is more complex.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class TreeDecoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, max_children):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTMCell(embed_dim, hidden_dim)
        self.child_predictor = nn.Linear(hidden_dim, max_children + 1)  # +1 for stop
        self.node_predictor = nn.Linear(hidden_dim, vocab_size)

    def forward(self, root_state, max_depth=10):
        # root_state: (hidden_dim,) initial state
        tree = []
        h, c = root_state, torch.zeros_like(root_state)
        agenda = [(h, c, None)]  # (hidden, cell, parent_id)
        node_id = 0

        while agenda and node_id < 100:
            h, c, parent_id = agenda.pop(0)
            x = self.embed(torch.tensor([0]))  # could condition on parent
            h, c = self.lstm(x, (h, c))
            num_children = self.child_predictor(h).argmax().item()
            node_type = self.node_predictor(h).argmax().item()
            tree.append({"id": node_id, "type": node_type, "parent": parent_id})

            for _ in range(num_children):
                agenda.append((h, c, node_id))
            node_id += 1

        return tree
```

## Notes

- Real decoders use attention over the partial tree.
- Constraints are applied as masks on the predictions.
- Beam search can be added.

See [[Tree Decoding]], [[Tree Generation]].

## Related Concepts

- [[Tree Decoding]]
- [[Tree Generation]]
- [[Constrained Decoding]]
