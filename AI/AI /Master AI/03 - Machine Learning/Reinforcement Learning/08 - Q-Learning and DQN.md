---
tags: [ml, reinforcement-learning, q-learning, dqn]
iteration: 8
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Q-Learning and DQN]
---

# 08 - Q-Learning and DQN

> [!info] TL;DR
> Q-learning learns the optimal action-value function $Q^*(s, a)$ directly from experience. Deep Q-Networks (DQN, DeepMind 2015) use a neural network to approximate $Q$ for high-dimensional states (e.g., Atari pixels). DQN was the first major deep RL success.

## Q-Learning

Q-learning is **model-free** (no need to know $P$ or $R$) and **off-policy** (can learn from any experience, not just the current policy). It directly estimates $Q^*$ via the Bellman optimality equation.

### The Update Rule

Given a transition $(s, a, r, s')$:

$$
Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]
$$

The term in brackets is the **TD error** — the difference between the current estimate and the bootstrapped target $r + \gamma \max_{a'} Q(s', a')$.

### Why it converges (under conditions)

With sufficient exploration and a small enough learning rate $\alpha$, Q-learning converges to $Q^*$ in finite MDPs (tabular case). The proof relies on the Bellman operator being a contraction.

### Exploration: $\epsilon$-greedy

To ensure exploration, take a random action with probability $\epsilon$, greedy otherwise:

$$
a_t = \begin{cases} \text{random} & \text{with prob } \epsilon \\ \arg\max_a Q(s_t, a) & \text{with prob } 1 - \epsilon \end{cases}
$$

Typical schedule: start with $\epsilon = 1.0$, decay to $\epsilon = 0.05$ over training.

## DQN (Deep Q-Network)

The breakthrough: approximate $Q(s, a)$ with a neural network $Q_\theta(s, a)$, allowing RL on high-dimensional states (Atari pixels, robot sensors).

### Key challenges and solutions

#### 1. Correlated samples
Consecutive transitions are highly correlated, breaking the i.i.d. assumption of SGD. Solution: **experience replay** — store transitions in a buffer, sample random minibatches.

#### 2. Non-stationary target
The target $r + \gamma \max_{a'} Q_\theta(s', a')$ uses the same network we're updating. As $\theta$ changes, the target shifts, causing instability. Solution: **target network** — a separate network $Q_{\theta^-}$ whose weights are copied from $\theta$ every $N$ steps.

### The DQN Loss

$$
L(\theta) = \mathbb{E}_{(s, a, r, s') \sim \text{replay}} \left[ \left( r + \gamma \max_{a'} Q_{\theta^-}(s', a') - Q_\theta(s, a) \right)^2 \right]
$$

### Algorithm sketch

```python
Q = QNetwork(state_dim, n_actions)
Q_target = copy.deepcopy(Q)
replay_buffer = ReplayBuffer(capacity=100_000)

for episode in range(num_episodes):
    s = env.reset()
    for t in range(max_steps):
        # epsilon-greedy
        if random.random() < epsilon:
            a = random_action()
        else:
            a = Q(s).argmax()
        
        s_next, r, done = env.step(a)
        replay_buffer.add(s, a, r, s_next, done)
        s = s_next
        
        # Training step
        if len(replay_buffer) > batch_size:
            batch = replay_buffer.sample(batch_size)
            states, actions, rewards, next_states, dones = batch
            
            # Target: r + gamma * max_a' Q_target(s', a') (0 if done)
            with torch.no_grad():
                target = rewards + gamma * (1 - dones) * Q_target(next_states).max(dim=1)[0]
            
            # Prediction: Q(s, a)
            preds = Q(states).gather(1, actions.unsqueeze(1)).squeeze(1)
            
            loss = F.mse_loss(preds, target)
            opt.zero_grad()
            loss.backward()
            opt.step()
    
    # Update target network periodically
    if episode % target_update_freq == 0:
        Q_target.load_state_dict(Q.state_dict())
```

### DQN Improvements

- **Double DQN** (van Hasselt et al. 2016): use the online network to choose the action, the target network to evaluate it. Reduces overestimation bias.
- **Dueling DQN** (Wang et al. 2016): decompose $Q(s,a) = V(s) + A(s, a) - \text{mean}(A(s, \cdot))$. Helps when action choice doesn't matter in many states.
- **Prioritized experience replay** (Schaul et al. 2016): sample transitions proportional to TD error — focus on the surprising ones.
- **Rainbow** (Hessel et al. 2018): combines all DQN improvements; SOTA on Atari.

## Limitations of Q-Learning / DQN

- **Discrete actions only** — `max_a` requires enumerable actions. For continuous actions, use DDPG, SAC, or PPO with a continuous policy.
- **Overestimation bias** — `max` tends to overestimate Q. Double DQN mitigates.
- **Sample inefficiency** — DQN needs millions of environment interactions on Atari.
- **Hyperparameter sensitivity** — replay buffer size, target update frequency, $\epsilon$ schedule all matter.

## Why This Matters for AI

- DQN was the **first deep RL breakthrough** (2015, Atari). Demonstrated that neural networks could learn complex control from raw pixels.
- The replay buffer + target network pattern is reused in many RL algorithms, including some RLHF variants.
- For **LLM alignment**, Q-learning isn't directly used (PPO is preferred), but the conceptual framework (off-policy, value-based) influenced alignment research.

## Production Implications

- DQN and variants are used in **game AI** (Atari, StarCraft, Go via AlphaZero).
- For real-world control (robotics, autonomous vehicles), **safety constraints** matter — DQN alone is dangerous because it explores randomly. Use safe RL or model-predictive control.
- For **recommendation systems**, contextual bandits (simpler than full RL) often suffice.
- For LLMs, see [[10 - PPO Deep Treatment]] and [[12 - Fine-Tuning/RLHF/RLHF with PPO|RLHF]].

## Common Pitfalls

- **No replay buffer** — training is unstable without it.
- **Updating target network too often** — defeats the purpose (stability).
- **Wrong $\epsilon$ schedule** — too high = no learning; too low = no exploration.
- **Reward scaling** — large rewards cause divergence; scale to ~[-1, 1].
- **Forgetting `done` mask** — terminal states have no future value; the target should be just `r`, not `r + γ V(s')`.

## Further Reading

- Mnih et al. (2015), *Human-level control through deep reinforcement learning* (DQN).
- van Hasselt et al. (2016), *Deep Reinforcement Learning with Double Q-Learning*.
- Sutton & Barto, *Reinforcement Learning*, Chapter 6 (Q-learning).

## Convergence Proof Sketch (Tabular Q-Learning)

The convergence of tabular Q-learning under standard conditions (Watkins & Dayan 1992) is one of the few convergence results in RL. The key ingredients:

1. **Bellman operator is a contraction.** Define $T^* Q(s, a) = \mathbb{E}_{s' \sim P}[r + \gamma \max_{a'} Q(s', a')]$. Then $\|T^* Q_1 - T^* Q_2\|_\infty \le \gamma \|Q_1 - Q_2\|_\infty$, by the contraction property of $\max$ and the discount $\gamma < 1$. By the Banach fixed-point theorem, $T^*$ has a unique fixed point $Q^*$.

2. **Q-learning is stochastic approximation of $T^*$.** Each update $Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha_t [r_t + \gamma \max_{a'} Q(s_t', a') - Q(s_t, a_t)]$ is a noisy sample of the Bellman operator applied at the current $(s_t, a_t)$.

3. **Robbins-Monro conditions.** If $\sum_t \alpha_t = \infty$ and $\sum_t \alpha_t^2 < \infty$, and every $(s, a)$ pair is visited infinitely often (sufficient exploration), then $Q_t \to Q^*$ almost surely.

The deep RL case (DQN) **does not have a general convergence proof** because:
- The Bellman operator applied through a neural network function approximator is no longer a contraction (the network introduces non-monotonicity).
- The "regression to the mean" of SGD interacts poorly with the non-stationary target.
- Experience replay decorrelates samples but doesn't eliminate the moving-target problem (this is what the target network addresses, heuristically).

This is why DQN training is notoriously unstable, why hyperparameter tuning matters, and why deterministic-convergence claims for deep RL should be treated with skepticism. DQN works empirically; it does not converge provably.

## Detailed DQN Implementation (Production-Style)

A more complete sketch with all the engineering details:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import deque
import random

class QNetwork(nn.Module):
    def __init__(self, obs_dim, n_actions, hidden=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, n_actions),
        )
    def forward(self, x):
        return self.net(x)  # returns Q(s, *) for all actions

class ReplayBuffer:
    def __init__(self, capacity=100_000):
        self.buf = deque(maxlen=capacity)
    def add(self, s, a, r, s_next, done):
        self.buf.append((s, a, r, s_next, done))
    def sample(self, batch_size):
        batch = random.sample(self.buf, batch_size)
        s, a, r, s_next, done = zip(*batch)
        return (np.array(s), np.array(a, dtype=np.int64),
                np.array(r, dtype=np.float32),
                np.array(s_next), np.array(done, dtype=np.float32))
    def __len__(self): return len(self.buf)

class DQNAgent:
    def __init__(self, obs_dim, n_actions, lr=1e-4, gamma=0.99,
                 epsilon_start=1.0, epsilon_end=0.05, epsilon_decay=1e5,
                 target_update=1000, batch_size=64, device="cuda"):
        self.q = QNetwork(obs_dim, n_actions).to(device)
        self.q_target = QNetwork(obs_dim, n_actions).to(device)
        self.q_target.load_state_dict(self.q.state_dict())
        self.opt = torch.optim.Adam(self.q.parameters(), lr=lr)
        self.buf = ReplayBuffer(100_000)
        self.gamma, self.batch_size = gamma, batch_size
        self.target_update = target_update
        self.step = 0
        self.eps_start, self.eps_end, self.eps_decay = epsilon_start, epsilon_end, epsilon_decay
        self.n_actions, self.device = n_actions, device

    def epsilon(self):
        return self.eps_end + (self.eps_start - self.eps_end) * \
               np.exp(-self.step / self.eps_decay)

    def act(self, obs):
        self.step += 1
        if random.random() < self.epsilon():
            return random.randint(0, self.n_actions - 1)
        with torch.no_grad():
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            return int(self.q(obs_t).argmax(dim=1).item())

    def learn(self):
        if len(self.buf) < self.batch_size:
            return None
        s, a, r, s_next, done = self.buf.sample(self.batch_size)
        s = torch.as_tensor(s, dtype=torch.float32, device=self.device)
        a = torch.as_tensor(a, device=self.device).unsqueeze(1)
        r = torch.as_tensor(r, device=self.device)
        s_next = torch.as_tensor(s_next, dtype=torch.float32, device=self.device)
        done = torch.as_tensor(done, device=self.device)

        # Current Q(s, a)
        q_sa = self.q(s).gather(1, a).squeeze(1)

        # Target: r + gamma * max_a' Q_target(s', a') * (1 - done)
        with torch.no_grad():
            q_next = self.q_target(s_next).max(dim=1)[0]
            target = r + self.gamma * (1 - done) * q_next

        loss = F.smooth_l1_loss(q_sa, target)  # Huber loss — more stable than MSE
        self.opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.q.parameters(), 10.0)  # gradient clipping
        self.opt.step()

        # Periodic target network sync
        if self.step % self.target_update == 0:
            self.q_target.load_state_dict(self.q.state_dict())
        return loss.item()
```

Notable engineering choices:
- **Huber loss** (`smooth_l1_loss`) instead of MSE: less sensitive to large TD errors, which are common early in training. This is a small but consistent improvement.
- **Gradient clipping** to norm 10: prevents the occasional catastrophic update from destabilizing training.
- **Linear epsilon decay** by step (not episode): smoother exploration schedule.
- **Hard target update** every 1000 steps. An alternative is Polyak averaging (`q_target = 0.995 * q_target + 0.005 * q`), which often works better.

## Double DQN: Why and How

Standard DQN suffers from **overestimation bias**: $\mathbb{E}[\max_a Q(s', a')] \ge \max_a \mathbb{E}[Q(s', a)]$ by Jensen's inequality (max is convex). With noisy Q estimates, this systematically overestimates target values, leading to over-optimistic value functions and unstable training.

Double DQN (van Hasselt et al. 2016) splits the max into two operations:
- Use the **online network** to *select* the best next action: $a^* = \arg\max_a Q_\theta(s', a)$.
- Use the **target network** to *evaluate* that action: $Q_{\theta^-}(s', a^*)$.

```python
# Double DQN target
with torch.no_grad():
    next_actions = self.q(s_next).argmax(dim=1, keepdim=True)  # online selects
    q_next = self.q_target(s_next).gather(1, next_actions).squeeze(1)  # target evaluates
    target = r + self.gamma * (1 - done) * q_next
```

This decouples selection from evaluation, eliminating most of the overestimation bias. The cost is one extra forward pass per training step (cheap).

Empirically, Double DQN is one of the most reliable DQN improvements — almost always helps, almost never hurts. **Always use Double DQN, not vanilla DQN.**

## Variants Comparison Table

| Variant            | Year | Key Idea                                                | Cost vs DQN  | Typical Benefit            |
|--------------------|------|---------------------------------------------------------|--------------|----------------------------|
| Vanilla DQN        | 2015 | NN + replay + target net                                | 1×           | Baseline                   |
| Double DQN         | 2016 | Decouple selection and evaluation                       | ~1.05×       | Eliminates overestimation  |
| Dueling DQN        | 2016 | Decompose Q = V + A                                     | 1×           | Better when actions are similar |
| PER (Prioritized)  | 2016 | Sample by TD error                                      | ~1.5–2×      | 2× sample efficiency       |
| Noisy DQN          | 2017 | Replace epsilon-greedy with noisy nets                  | 1×           | Better exploration         |
| C51 (Distributional)|2017 | Predict Q-value distribution, not expectation           | ~1.5×        | Better credit assignment   |
| QR-DQN             | 2017 | Quantile regression for distributional Q                | ~1.3×        | Faster than C51            |
| Rainbow            | 2018 | Combine 6 DQN improvements                              | ~2×          | SOTA on Atari              |
| R2D2               | 2019 | Recurrent DQN + burn-in + stored hidden state           | ~3×          | Partial observability      |
| Agent57            | 2020 | Adaptive exploration + Rainbow                          | ~5×          | First to beat humans on all 57 Atari games |

For LLM/RLHF work, none of these are directly used (PPO and GRPO dominate), but the conceptual lessons transfer:
- Off-policy + replay (used in DQN) ≈ the "old rollouts" buffer in some RLHF variants.
- Distributional Q (C51) influenced distributional reward modeling.
- The overestimation bias in DQN is a real concern in RLHF reward models — Double-Q-style ideas appear in RLHF variance reduction.

## Continuous Action Spaces: Why Q-Learning Fails

The Q-learning update requires $\max_{a'} Q(s', a')$ — an optimization over the action space. For discrete actions (Atari's 18 joystick directions), this is $O(|A|)$ and trivial. For continuous actions (robotics), the max has no closed form, and gradient-based maximization inside the Bellman backup is unstable.

This is why **actor-critic methods** (DDPG, SAC, PPO) dominate continuous control:
- DDPG/TD3/SAC: learn both $Q(s, a)$ (critic) and a policy $\pi(s)$ (actor). The actor directly outputs the action maximizing $Q$, eliminating the inner max.
- PPO: learn a stochastic policy directly, using a critic only to reduce variance of policy gradients.

See [[09 - Policy Gradients and Actor Critic]] and [[10 - PPO Deep Treatment]].

## Connection to RLHF and LLM Alignment

Q-learning is rarely used directly in LLM alignment, but the conceptual framework matters:

- **Why not Q-learning for LLMs?** The action space is the vocabulary (~50K tokens), and the state is the entire context. $\max_a Q(s, a)$ over 50K actions per token is feasible, but the bootstrapping target (Q estimating Q estimating Q...) is unstable for the autoregressive LLM structure. PPO and GRPO instead use **Monte Carlo or short-horizon returns** from rollouts, avoiding the bootstrapping instability.

- **What DQN ideas do appear in RLHF?**
  - **Experience replay**: PPOrollout buffers store old trajectories; the KL penalty stabilizes training (similar role to target networks).
  - **Reward overestimation**: just as DQN overestimates Q, RLHF reward models are vulnerable to **reward hacking** — the policy exploits imperfections in the learned reward. The KL penalty to the reference model is the analog of clipping and conservative Q-learning.
  - **Distributional rewards**: GRPO (DeepSeek-R1) samples multiple completions and uses their *relative* rewards (group baseline), reducing reward-model variance — conceptually similar to distributional Q-learning.

- **Best places to use Q-learning in modern AI**:
  - Discrete-decision systems (recommendation, ad selection) where reward is well-defined and the state space is moderate.
  - Tool-use agents where the action space is "which tool to call" (discrete, enumerable) and reward comes from environment feedback.
  - Game-playing AI (chess, Go via AlphaZero, StarCraft).

## Worked Example: Solving CartPole with DQN

A complete training loop on the classic CartPole-v1 environment:

```python
import gymnasium as gym

env = gym.make("CartPole-v1")
obs_dim = env.observation_space.shape[0]  # 4
n_actions = env.action_space.n            # 2
agent = DQNAgent(obs_dim, n_actions, device="cuda")

episode_rewards = []
for episode in range(500):
    obs, _ = env.reset()
    ep_reward = 0
    for t in range(500):
        a = agent.act(obs)
        obs_next, r, terminated, truncated, _ = env.step(a)
        done = terminated or truncated
        agent.buf.add(obs, a, r, obs_next, float(done))
        loss = agent.learn()
        obs = obs_next
        ep_reward += r
        if done: break
    episode_rewards.append(ep_reward)
    if episode % 10 == 0:
        avg = np.mean(episode_rewards[-10:])
        print(f"Ep {episode:3d}  avg_reward(last 10)={avg:.1f}  eps={agent.epsilon():.3f}")
```

Expected progression: rewards climb from ~10 (random) to ~475 (solved threshold) over 200-400 episodes. Key failure modes you'll see:
- **Diverges after initial learning**: learning rate too high; reduce to 5e-5.
- **Plateaus at ~50**: insufficient exploration; slow epsilon decay.
- **Spiky rewards**: target update frequency too low; reduce to 500.
- **Memory explosion**: replay buffer too large for GPU; use CPU storage, GPU-only for sampling.

## Common Debugging Checklist

When your DQN isn't learning, check in this order:
1. **Is the buffer being filled before learning?** (Wait for at least `batch_size` samples.)
2. **Is `done` correctly propagated?** (A common bug — terminal states should NOT bootstrap.)
3. **Is epsilon decaying?** (Print it.)
4. **Is the target network being updated?** (Print step count modulo target_update.)
5. **Are rewards scaled?** (Atari rewards to [-1, 1]; large rewards cause divergence.)
6. **Are gradients clipped?** (Without clipping, occasional huge updates destroy training.)
7. **Is the loss decreasing?** (Plot it. If not, your learning rate is wrong.)
8. **Are you using Double DQN?** (Vanilla DQN can diverge where Double converges.)

## Interview Questions

1. **Q: Why does Q-learning use a target network?**
   A: To stabilize the moving-target problem. The TD target $r + \gamma \max_a Q(s', a')$ uses the same network being updated, creating a non-stationary optimization. The target network is a delayed copy (synced every N steps or Polyak-averaged), giving the online network a quasi-fixed target to regress toward.

2. **Q: Why is experience replay necessary for DQN?**
   A: Two reasons. (1) Consecutive transitions are highly correlated, violating SGD's i.i.d. assumption; random sampling from the buffer decorrelates them. (2) Each transition can be reused many times, dramatically improving sample efficiency. Without replay, DQN fails to learn on most Atari games.

3. **Q: What is the overestimation bias in DQN, and how does Double DQN fix it?**
   A: $\mathbb{E}[\max_a Q(s', a')] \ge \max_a \mathbb{E}[Q(s', a)]$ by Jensen (max is convex). With noisy Q, this systematically overestimates values. Double DQN decouples action selection (online network) from evaluation (target network), reducing the bias because the noise in selection is independent of the noise in evaluation.

4. **Q: Why isn't Q-learning used for LLM alignment?**
   A: Three reasons: (1) The action space (next token) is huge but discrete — technically tractable, but (2) bootstrapping Q-values for autoregressive LLMs is unstable because each token's "state" depends on the entire prefix, and (3) the reward signal is sparse and delayed (whole completion scored, not per-token). PPO/GRPO instead use Monte Carlo returns from rollouts, avoiding bootstrapping instability.

5. **Q: How does prioritized experience replay work, and what's its main tradeoff?**
   A: Sample transitions proportional to $|TD error|^\alpha$ (with importance-sampling weights to correct the bias). Trades compute (prioritization adds ~30-50% overhead) and introduces bias-variance tradeoffs (the IS weights reduce the bias but can increase variance if $\alpha$ is too high) for ~2× sample efficiency. Almost always worth it for expensive environments (robotics) and less clearly worth it for cheap ones (Atari).

6. **Q: Walk through the Q-learning update for a terminal transition.**
   A: At a terminal state, $s'$ is the absorbing state with $V(s') = 0$ by definition. The target becomes just $r$ (no bootstrap). Forgetting to mask the bootstrap with `(1 - done)` is the most common DQN bug — the model learns to predict nonzero future value at terminal states, which corrupts the value function.

## See Also

- [[07 - MDPs and Bellman Equations]]
- [[09 - Policy Gradients and Actor Critic]]
- [[10 - PPO Deep Treatment]]
- [[03 - Machine Learning/MOC|ML MOC]]
