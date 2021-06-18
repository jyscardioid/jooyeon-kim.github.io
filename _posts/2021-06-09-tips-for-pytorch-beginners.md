---
title: 'Three Basic Tips for PyTorch Beginners'
date: 2021-06-09
permalink: /blogs/three-basic-tips-for-pytorch-beginners/
tags:
  - Machine Learning Engineering
summary: ""
---

While grading students' codes this semester (Fall 2021), I found some suboptimal patterns that students often use.
This article organizes them and introduces a more efficient use of PyTorch.

## Avoid to use your own loops, use PyTorch's functions

Let's try to find the maximum of the tensor corresponding to the first dimension.

```python
import torch

x = torch.Tensor([[0, 1, 2, 3],
                  [7, 6, 5, 4]])
answer = torch.Tensor([3., 7.])
```

Iteration over a tensor through primitive loops (`for` or `while`) in python is very slow.

```python
# Don't
max_x = torch.empty((2,))
idx = torch.argmax(x, dim=1)
for i in range(x.size(0)):
    max_x[i] = x[i, idx[i]]
```

Instead, use methods implemented in PyTorch.

```python
# Do
max_x, _ = torch.max(x, dim=1)
```

It is nearly impossible to remember all functions in PyTorch.
We may not know which functions are implemented or which functions to use.
Thus, it is important to search the document first.

## Use `:` in slicing tensors

We probably need to select the entire sub-tensor for some dimension.
For this case, I have seen using `torch.arange` with the corresponding size.
```python
# H: Tensor, the shape of which is [B, N, F].
# Don't
H = H[torch.arange(H.shape[0]), idx]
```

This can easily be replaced with a colon (`:`) .

```python
# Do
H = H[:, idx]
```

If we put colons in the entire dimension of the Tensor, we can easily recognize its shape.
This improves the readability of the code and makes it easier to maintain it.

```python
# Even better
H = H[:, idx, :]
```

## Avoid to call unnecessary `.detach()`

Detaching a tensor from a computational graph (by `.detach()`) is usually not a good idea.
This prevents propagating the gradient to the graph before that computational node.

In the code below, let's detach `hidden`, the output of `layer_1`.
```python
import torch
torch.random.manual_seed(42)
layer_1, layer_2 = torch.nn.Linear(16, 16), torch.nn.Linear(16, 16)
data, labels = torch.rand(3, 16), torch.rand(1, 16)

hidden = layer_1(data)
# Don't
hidden = hidden.detach()
output = layer_2(hidden)

(output - labels).sum().backward()  # MSE loss
optim = torch.optim.SGD(list(layer_1.parameters()) + list(layer_2.parameters()), lr=1e-1)

print(layer_1.weight.mean())
optim.step()
print(layer_1.weight.mean())
```
Then, the parameter of `layer_1` does not change even after `.step()`.
In most cases, this is not the result we want.
```
tensor(-0.0136, grad_fn=<MeanBackward0>)
tensor(-0.0136, grad_fn=<MeanBackward0>)
```
If we remove the `.detach()` part, we can see that the `layer_1` has been updated.
```
tensor(-0.0136, grad_fn=<MeanBackward0>`
tensor(0.0113, grad_fn=<MeanBackward0>)
```

Of course, there is also an [advanced way](https://pytorch.org/docs/stable/nn.functional.html#gumbel-softmax) of using `.detach()` on purpose.

## Related materials

- [7 Tips To Maximize PyTorch Performance](https://towardsdatascience.com/7-tips-for-squeezing-maximum-performance-from-pytorch-ca4a40951259)
- [Efficient PyTorch — Eliminating Bottlenecks](https://towardsdatascience.com/efficient-pytorch-part-1-fe40ed5db76c)