---
tags: [implementation, graph-decoder]
---

# Graph Decoder Reference Implementation

A simple reference for a graph decoder.

```python
import torch
import torch.nn as nn

class GraphDecoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, max_nodes):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.node_lstm = nn.LSTMCell(embed_dim, hidden_dim)
        self.edge_predictor = nn.Linear(hidden_dim * 2, 1)
        self.node_predictor = nn.Linear(hidden_dim, vocab_size)

    def forward(self, init_state, max_nodes=50):
        nodes = []
        edges = []
        h, c = init_state, torch.zeros_like(init_state)

        for i in range(max_nodes):
            x = self.embed(torch.tensor([0]))
            h, c = self.node_lstm(x, (h, c))
            node_type = self.node_predictor(h).argmax().item()
            nodes.append({"id": i, "type": node_type})

            # Predict edges to existing nodes
            for j in range(i):
                # Pair features
                pair = torch.cat([h, nodes[j]["hidden"]])
                edge_prob = self.edge_predictor(pair).sigmoid()
                if edge_prob > 0.5:
                    edges.append({"src": i, "dst": j, "type": "adjacent"})

        return nodes, edges
```

See [[Scene Graph Generation]], [[Graph Neural Networks]].

## Related Concepts

- [[Scene Graph Generation]]
- [[Graph Neural Networks]]
