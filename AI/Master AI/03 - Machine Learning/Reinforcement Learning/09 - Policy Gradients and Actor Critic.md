---
tags: [ml, reinforcement-learning, policy-gradient, actor-critic]
iteration: 2
created: 2026-08-07
aliases: [Policy Gradients and Actor Critic]
---

# 09 - Policy Gradients and Actor-Critic

> [!info] TL;DR
> Policy gradient methods directly optimize the policy $\pi_\theta$ via gradient ascent on expected return. Actor-critic methods combine a policy ("actor") with a value function ("critic") to reduce variance. **PPO, the algorithm behind RLHF, is an actor-critic method** — this note is the prerequisite.

## Why Policy-Based Methods?

Value-based methods (DQN) work for discrete actions but struggle with:
- Continuous action spaces (can't `max` over continuous sets).
- Stochastic policies (necessary for some games, e.g., rock-paper-scissors).
- Indirect policy learning (Q-learning learns Q, then derives $\pi$ — extra step).

Policy-based methods parameterize $\pi_\theta$ directly and optimize $\theta$ on the expected return.

## The Policy Gradient Theorem

The expected return under policy $\pi_\theta$:

$$
J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^{T} \gamma^t r_t \right]
$$

The policy gradient theorem (Sutton et al. 2000):

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t \mid s_t) \, G_t \right]
$$

where $G_t = \sum_{t'=t}^{T} \gamma^{t'-t} r_{t'}$ is the return from step $t$.

### Intuition

- $\nabla_\theta \log \pi_\theta(a_t \mid s_t)$ is the direction that increases the probability of taking action $a_t$ in state $s_t$.
- $G_t$ weights this by how good the outcome was.
- The gradient pushes up the probability of actions that led to high returns, down for low returns.

The $\log$ comes from the **score function estimator** — a trick for differentiating through an expectation. Equivalent to REINFORCE (Williams, 1992).

## REINFORCE (Vanilla Policy Gradient)

The simplest policy gradient algorithm:

1. Run policy $\pi_\theta$ in the environment to collect a trajectory $\tau = (s_0, a_0, r_0, s_1, \ldots)$.
2. Compute returns $G_t$.
3. Update: $\theta \leftarrow \theta + \alpha \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t) \, G_t$.

### Problems with REINFORCE
- **Huge variance**: $G_t$ is the sum of many noisy rewards. Gradient estimates are extremely noisy.
- **Sample inefficient**: throws away data after one update.
- **No credit assignment**: hard to tell which actions in a trajectory caused the eventual return.

## Reducing Variance: Baselines

Subtract a baseline $b(s_t)$ from the return:

$$
\nabla_\theta J(\theta) = \mathbb{E} \left[ \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t) (G_t - b(s_t)) \right]
$$

The baseline doesn't bias the gradient (a math identity) but can dramatically reduce variance. The most common baseline: $V^\pi(s_t)$ — the value of the state. This gives the **advantage** $A^\pi(s_t, a_t) = Q^\pi(s_t, a_t) - V^\pi(s_t)$.

## Advantage Function

$$
A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s)
$$

- $A > 0$: action $a$ is better than average in state $s$ → push probability up.
- $A < 0$: action $a$ is worse than average → push probability down.

Using $A$ instead of $G$ is the key variance reduction that makes policy gradients practical.

## Actor-Critic

Maintain **two** models:
- **Actor**: the policy $\pi_\theta$.
- **Critic**: a value estimator $V_\phi$ (or $Q_\phi$).

The critic provides the baseline for the actor's gradient. Both are trained simultaneously.

### A2C / A3C

**Advantage Actor-Critic**:
- Critic learns $V_\phi$ via TD learning.
- Actor updates with advantage estimate $\hat{A}_t = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$ (TD error as advantage).

**A3C** (Asynchronous Advantage Actor-Critic, Mnih et al. 2016): multiple workers train in parallel, asynchronously updating shared actor and critic. Was the first major actor-critic success.

**A2C**: synchronous version; often as good as A3C and simpler.

### GAE (Generalized Advantage Estimation)

A more sophisticated advantage estimate that interpolates between one-step TD and Monte Carlo returns:

$$
\hat{A}_t^{(1)} = \delta_t
$$
$$
\hat{A}_t^{(2)} = \delta_t + \gamma \lambda \delta_{t+1}
$$
$$
\hat{A}_t^{(\infty)} = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}
$$

where $\delta_t = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$ is the TD error. The hyperparameter $\lambda \in [0, 1]$ trades off bias (low $\lambda$) and variance (high $\lambda$). $\lambda = 0.95$ is a common default.

GAE is standard in modern actor-critic methods, including PPO.

## On-Policy vs Off-Policy

- **On-policy**: train on data collected by the current policy. Must discard old data after each update. PPO is on-policy.
- **Off-policy**: train on data from any policy (e.g., replay buffer). More sample-efficient but harder to stabilize. DQN, SAC are off-policy.

On-policy methods are simpler and more stable but sample-inefficient. The RLHF use case is on-policy because we want to improve the current LLM, not old versions.

## Worked Example (REINFORCE with baseline)

```python
class Policy(nn.Module):
    def __init__(self, state_dim, n_actions):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 64), nn.ReLU(),
            nn.Linear(64, n_actions),
        )
    def forward(self, s):
        return F.softmax(self.net(s), dim=-1)

class Value(nn.Module):
    def __init__(self, state_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 64), nn.ReLU(),
            nn.Linear(64, 1),
        )
    def forward(self, s):
        return self.net(s).squeeze(-1)

policy = Policy(state_dim, n_actions)
value = Value(state_dim)
opt_pi = torch.optim.Adam(policy.parameters(), lr=1e-3)
opt_v = torch.optim.Adam(value.parameters(), lr=1e-3)

def update(states, actions, returns):
    # Advantage
    v = value(states)
    advantages = returns - v.detach()
    
    # Policy gradient
    log_probs = torch.log(policy(states).gather(1, actions.unsqueeze(1)).squeeze(1))
    pi_loss = -(log_probs * advantages).mean()
    opt_pi.zero_grad(); pi_loss.backward(); opt_pi.step()
    
    # Value update
    v_loss = F.mse_loss(v, returns)
    opt_v.zero_grad(); v_loss.backward(); opt_v.step()
```

## Why This Matters for AI

- **PPO is an actor-critic method.** Without understanding policy gradients and advantage, you can't understand PPO, and without PPO, you can't understand RLHF.
- The **advantage function** is a central concept that recurs in modern alignment (e.g., DPO uses log-ratio advantages).
- The on-policy setting is what makes LLM alignment tractable — we can collect fresh trajectories from the current model and improve it.

## Production Implications

- Pure policy gradient methods (REINFORCE) are too high-variance for production. Always use actor-critic with GAE.
- For LLMs, see [[10 - PPO Deep Treatment]] and [[12 - Fine-Tuning/RLHF/RLHF with PPO|RLHF]].
- For game-playing and robotics, more advanced methods (PPO, SAC, MuZero) are standard.

## Common Pitfalls

- **No baseline** — REINFORCE without a baseline is too noisy to be useful.
- **Wrong advantage sign** — flipping sign makes the model worse instead of better.
- **Off-policy data with on-policy algorithm** — PPO can use a small amount of stale data (via importance sampling), but going too far off-policy breaks it.
- **Critic learning too fast or too slow** — the critic must be reasonably accurate for the actor's gradients to be meaningful. Tune critic LR separately.

## Further Reading

- Sutton et al. (2000), *Policy Gradient Methods for Reinforcement Learning with Function Approximation*.
- Williams (1992), *Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning* (REINFORCE).
- Schulman et al. (2016), *High-Dimensional Continuous Control Using Generalized Advantage Estimation* (GAE).
- Mnih et al. (2016), *Asynchronous Methods for Deep Reinforcement Learning* (A3C).

## See Also

- [[07 - MDPs and Bellman Equations]]
- [[08 - Q-Learning and DQN]]
- [[10 - PPO Deep Treatment]]
- [[03 - Machine Learning/MOC|ML MOC]]
- [[12 - Fine-Tuning/RLHF/RLHF with PPO|RLHF]] (planned)
