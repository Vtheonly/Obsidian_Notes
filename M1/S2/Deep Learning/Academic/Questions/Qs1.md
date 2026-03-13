# Conceptual Questions

**Q: Why can't we use Mean Squared Error (MSE) for Logistic Regression?**
A: Logistic Regression passes the linear combination $z$ through a Sigmoid activation function. If you insert a Sigmoid function inside the MSE equation, the resulting mathematical landscape becomes non-convex. It will have multiple local minima, meaning Gradient Descent is highly likely to get stuck and fail to find the optimal solution. We use Log Loss (Binary Cross-Entropy) because it guarantees a convex landscape.

**Q: What is the purpose of the bias term ($b$)?**
A: While weights ($w$) determine the slope or importance of an input, the bias ($b$) shifts the activation function left or right. Without a bias, the activation function must always cross the origin $(0,0)$, which severely limits the patterns the network can learn.
