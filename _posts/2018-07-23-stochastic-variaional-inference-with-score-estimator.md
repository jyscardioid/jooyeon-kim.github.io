---
title: 'Stochastic Variaional Inference with Score Estimator'
date: 2018-07-23
permalink: /blogs/stochastic-variaional-inference-with-score-estimator/
tags:
  - Machine Learning
summary: ""
---

For the following optimization problem, minimizing KL divergence from $q_{\theta}(x)$ to $p(x\|y_0)$,

$ argmin_{\theta} \text{KL} \left[ q_{\theta}(x) \|\| p(x\|y_0)  \right] $,

How can we use stochastic gradient descent with the following gradient, which is the score estimator (a.k.a. REINFORCE):

$ \nabla_{\theta} \text{KL} [ q_{\theta}(x) \|\| p(x\|y_0) ]$.

## 1. Basis

This problem is the same as $E_{x \sim q_{\theta}(x)} \left[\left(
  \nabla_{\theta} \log(q_{\theta}(x))
  \right) \cdot
  \log \frac{q_{\theta}(x)}{p(x,y_0)}
\right]$.

$\nabla_{\theta} \text{KL} [ q_{\theta}(x) \|\| p(x\|y_0) ]$

$ = \nabla_{\theta} \left(
        \sum_{x} q_{\theta}(x) \log \frac{q_{\theta}(x)}{p(x,y_0)}
        + \sum_{x} q_{\theta}(x) \log p(y_0)
      \right)$

$ = \nabla_{\theta} \left(
        \sum_{x} q_{\theta}(x) \log \frac{q_{\theta}(x)}{p(x,y_0)}
      \right)
      + \nabla_{\theta} \left( \sum_{x} q_{\theta}(x) \log p(y_0) \right)$

$ = \nabla_{\theta} \left(
        \sum_{x} q_{\theta}(x) \log \frac{q_{\theta}(x)}{p(x,y_0)}
      \right)
    \because \text{Lemma 1}$

$ = \sum_{x} \nabla_{\theta} \left( q_{\theta}(x) \right) \log \frac{q_{\theta}(x)}{p(x,y_0)} + 
      \sum_{x} q_{\theta}(x) \nabla_{\theta} \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)$

$ = \sum_{x} \nabla_{\theta} \left( q_{\theta}(x) \right) \log \frac{q_{\theta}(x)}{p(x,y_0)}
    \because \text{Lemma 2}$

$ = \sum_{x} q_{\theta}(x) \cdot
      \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right) \cdot
      \log \frac{q_{\theta}(x)}{p(x,y_0)}
    \because \text{Lemma 3}$

$ = E_{x \sim q_{\theta}(x)} \left[
          \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right)
          \cdot \log \frac{q_{\theta}(x)}{p(x,y_0)}
        \right]$


### Lemma 1

$\nabla_{\theta} \left( \sum_{x} q_{\theta}(x) \log p(y_0) \right)$

$= \log p(y_0) \nabla_{\theta} \left( \sum_{x} q_{\theta}(x) \right)$

$= \log p(y_0) \nabla_{\theta} (1)$

$= 0$

### Lemma 2

$\sum_{x} q_{\theta}(x) \nabla_{\theta} \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)$

$= \sum_{x} q_{\theta}(x) \nabla_{\theta} \left( \log q_{\theta}(x) \right)$

$= \sum_{x} q_{\theta}(x) \frac{\nabla_{\theta}q_{\theta}(x)}{q_{\theta}(x)} \because \text{Lemma 3}$

$= \sum_{x} \nabla_{\theta} q_{\theta}(x)$

$= \nabla_{\theta} \sum_{x} q_{\theta}(x)$

$= \nabla_{\theta}(1) = 0$

### Lemma 3

$\nabla_{\theta} \left( \log q_{\theta}(x) \right) = \frac{\nabla_{\theta}q_{\theta}(x)}{q_{\theta}(x)}$

Here, Lemma 3 was called the log trick. In my humble opinion, this is quite similar to the differentiation of multi-variate log function.

## 2. Reduce Variance (Control Variate)

The sampling algorithm to estimate this is:

For $x_1, ... x_N$ drew from $q_{\theta}(x)$

$\frac{1}{N} \sum_{i=1}^{N}
      \left( \nabla_{\theta}  \log(q_{\theta}(x_i)) \right)
      \cdot \left( \log \frac{q_{\theta}(x_i)}{p(x_i,y_0)} \right)$

If we just use this algorithm, there will be high variance of results. So, to reduce the variance, we use a control variate $B$ in the below estimator.

$\frac{1}{N} \sum_{i=1}^{N}
      \left( \nabla_{\theta}  \log(q_{\theta}(x_i)) \right)
      \cdot \left( \log \frac{q_{\theta}(x_i)}{p(x_i,y_0)} -B \right)$

The reason that this is the same as $ \nabla_{\theta} \text{KL} [ q_{\theta}(x) \vert \vert p(x \vert y_0) ] $ is,

$E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right)
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} - B \right)
      \right] \label{q3_b_equation}$

$ = E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right)
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
      \right] -
      E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right) \cdot B
      \right]$

$ = E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right)
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
      \right] -
      B \cdot E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right)
      \right]$

$ = E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right)
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
      \right] -
      B \cdot \sum_{x} q_{\theta}(x) \nabla_{\theta} \left( \log q_{\theta}(x) \right)$

$ = E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta}  \log(q_{\theta}(x)) \right)
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
      \right]
      \because \text{Lemma 2}$

$ = \nabla_{\theta} \text{KL} [ q_{\theta}(x) \|\| p(x\|y_0) ]
    \because \text{(1)}$


## 3. Optimize Control Variate

We can compute the control variate $B$ that minimizes the variance of the equation in 2.

$B^{*} = \frac
        {E_{x \sim q_{\theta}(x)} \left[
          \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
          \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
        \right]}
        {E_{x \sim q_{\theta}(x)} \left[
          \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
        \right]}$

The proof is as follows.

For the simplicity, let $C$ be $ \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} - B \right)$.

In this problem, we have to find $B$ that minimizes the variance of the estimate for $N=1$, which is $\text{Variance}(C) = E_{x \sim q_{\theta(x)}}[C^2] - \left( \nabla_{\theta} \text{KL} [ q_{\theta}(x) \vert \vert p(x \vert y_0 ) ] \right)^2$.

Because $\left( \nabla_{\theta} \text{KL} [ q_{\theta}(x) \vert \vert p(x \vert y_0) ] \right)^2$ is just a constant, we can conclude that $argmin_{B} [ \text{Variance}(C) ] = argmin_{B} [ E_{x \sim q_{\theta}(x)}[C^2] ]$.

$E_{x \sim q_{\theta}(x)}[C^2] =$

$E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right) ^2
      \right]$

$\quad - 2B \cdot E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
      \right]$

$\quad + B^2 \cdot E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
      \right]$

Its derivative with respect to $B$ is,

$\frac{d}{dB} E_{x \sim q_{\theta}(x)}[C^2] = $

$\quad - 2 \cdot E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
        \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
      \right]$

$\quad + 2B \cdot E_{x \sim q_{\theta}(x)} \left[
        \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
      \right]$

$B^{*}$ that makes the derivative zero will be,

$B^{*} = \frac
        {E_{x \sim q_{\theta}(x)} \left[
          \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
          \cdot \left( \log \frac{q_{\theta}(x)}{p(x,y_0)} \right)
        \right]}
        {E_{x \sim q_{\theta}(x)} \left[
          \left( \nabla_{\theta} \log(q_{\theta}(x)) \right) ^2
        \right]}$
