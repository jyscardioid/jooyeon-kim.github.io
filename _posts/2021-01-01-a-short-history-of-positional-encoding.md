---
title: 'A Short History of Positional Encoding'
date: 2021-01-30
permalink: /blogs/a-short-history-of-positoinal-encoding/
tags:
  - CS
  - Machine Learning
---

Since I first saw the 'Attention Is All You Need' paper, I had a strong curiosity about the principle and theory of positional encoding.
It is well understood that the Transformer did not have inductive biases for RNN architectures and thus introduced positional encoding.
However, I have still not convinced how and why this works.
The authors mentioned that they chose this design because of the special nature of sinusoid about the relative position, but it was not enough for me.
> ... we hypothesized it would allow the model to easily learn to attend by relative positions, since for any fixed offset $k$, $PE_{pos+k}$ can be represented as a linear function of $PE_{pos}$. (Section 3.5 in [Vaswani et al., 2017](https://arxiv.org/abs/1706.03762))

While searching related literature, I was able to read the papers to develop more advanced positional encoding.
In particular, I found that positional encoding in Transformer can be beautifully extended to represent the time (generalization to the continuous space) and positions in a graph (generalization to the irregular structure).
In this post, I review the work related to positional encoding and describe what theories are based on the generalization to time and graph.

## Positional Representation

### Learned Positional Embedding

[Gehring et al., 2017 (ConvS2S)](https://arxiv.org/abs/1705.03122)

### Positional Encoding with Sinusoids 

[Vaswani et al., 2017 (Transformer)](https://arxiv.org/abs/1706.03762)

### Relative Positional Encoding

[Shaw et al., 2018](https://arxiv.org/abs/1803.02155),
[Dai et al., 2019 (Transformer-XL)](https://arxiv.org/abs/1901.02860)

### Word Order Encoding

[Wang et al., 2020](https://openreview.net/forum?id=Hke-WTVtwr)

### Rethinking Positional Encoding

[Ke et al., 2021](https://openreview.net/forum?id=09-528y2Fgf)

## Generalization Beyond Position

### Time Representation

[Xu et al., 2019 (Bochner/Mercer Time Embedding)](https://arxiv.org/abs/1911.12864),
[Kazemi et al., 2019 (time2vec)](https://arxiv.org/abs/1907.05321),
[Xu et al., 2021 (Temporal Kernel)](https://openreview.net/forum?id=whE31dn74cL),
[Shukla and Marlin, 2021 (Multi-time attention)](https://openreview.net/forum?id=mXbhcalKnYM)

### Tree Positional Encoding

[Shiv and Quirk, 2019](https://papers.nips.cc/paper/2019/hash/6e0917469214d8fbd8c517dcdc6b8dcf-Abstract.html)

### Graph Positional Encodings with Laplacian Eigenvectors

[Qiu et al., 2020 (GCC)](https://arxiv.org/abs/2006.09963),
[Dwivedi et al., 2020 (Benchmarking GNNs)](https://arxiv.org/abs/2003.00982v3)
