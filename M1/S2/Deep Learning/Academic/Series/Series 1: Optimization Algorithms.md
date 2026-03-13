# Series 1: Optimization Algorithms

_This is a placeholder for practical exercises/series._

## Exercise 1: Manual Gradient Calculation

Given the function $f(x,y) = (x-2)^2 + 2(y-3)^2$.

**1. Find the partial derivatives.**

- $\frac{\partial f}{\partial x} = 2x - 4$
- $\frac{\partial f}{\partial y} = 4y - 12$

**2. Perform one step of Gradient Descent starting at $(x,y) = (30, 20)$ with $\alpha = 0.05$.**

- $\nabla f(30, 20) = [(2(30)-4), (4(20)-12)] = [56, 68]$
- $x_{new} = 30 - (0.05 \times 56) = 30 - 2.8 = 27.2$
- $y_{new} = 20 - (0.05 \times 68) = 20 - 3.4 = 16.6$

_(See Python implementation in the course slides for the automated loop)._
