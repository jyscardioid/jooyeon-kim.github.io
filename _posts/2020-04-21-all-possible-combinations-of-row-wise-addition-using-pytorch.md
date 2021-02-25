---
title: 'All Possible Combinations of Row-wise Addition Using PyTorch'
date: 2020-04-21
permalink: /blogs/all-possible-combinations-of-row-wise-addition-using-pytorch/
tags:
  - CS
  - Machine Learning
summary: ""
---

How to get all possible combinations of row-wise addition (or substraction) using PyTorch?
For example, if we have `x = [x0, x1, x2]` and `y = [y0, y1]`, our goal is computing `[x0 + y0, x0 + y1, x1 + y0, x1 + y1, x2 + y0, x2 + y1]`.

Using PyTorch, the answer is:
```python
x = torch.Tensor([0, 1, 2])
y = torch.Tensor([10, 20])

"""
tensor([10., 20., 11., 21., 12., 22.])
"""
ans = (x.unsqueeze(1) + y.unsqueeze(0)).view(-1)
```

Similary, for the multi-dimensional vectors,
```python
x = torch.Tensor([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
y = torch.Tensor([[10, 20, 30], [40, 50, 60]])

"""
tensor([[10., 21., 32.],
        [40., 51., 62.],
        [13., 24., 35.],
        [43., 54., 65.],
        [16., 27., 38.],
        [46., 57., 68.]])
"""
ans = (x.unsqueeze(1) + y.unsqueeze(0)).view(-1, 3)
```
