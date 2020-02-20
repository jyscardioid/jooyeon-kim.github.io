---
title: 'Install PyTorch with CUDA 10.0'
date: 2020-02-20
permalink: /blogs/install-pytorch-with-cuda-10/
tags:
  - CS
---

To fix PyTorch CUDA version error like below:
```
RuntimeError: Detected that PyTorch and torch_sparse were compiled with different CUDA versions. PyTorch has CUDA version 10.1 and torch_sparse has CUDA version 10.0. Please reinstall the torch_sparse that matches your PyTorch install.
```

Install PyTorch with the right tag.
```bash
pip install torch==1.4.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
```

You can write cu92 or cu101 instead of cu100.

[PyTorch Geometric](https://github.com/rusty1s/pytorch_geometric#installation) is now using a similar form of pip indexing. 