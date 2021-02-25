---
title: 'Handing Struct Error when Using Python Multi-processing Pool'
date: 2020-09-12
permalink: /blogs/struct-error-python-multiprocessing/
tags:
  - CS
summary: ""
---

When using Python `multiprocessing.Pool` to process large data, I met this strange error.
```
struct.error: 'i' format requires -2147483648 <= number <= 2147483647
```

Looking at the internal structure, it seems that arguments are pickled before they are sent to child processes from the parent process.
When the size of arguments is too large for pickling (maybe more than 2147483647), this kind of struct error occurs.
```python
from multiprocessing import Pool

def f(data_id, large_data):
    pass

if __name__ == '__main__':
    big_data = Data()
    pool = Pool()
    pool.starmap(f, [(i, big_data) for i in range(100)])
```

I don't know whether there is an elegant solution, but it can be solved by declaring this data globally.
```python
from multiprocessing import Pool

def f(data_id):
    global big_data
    large_data = big_data

if __name__ == '__main__':
    big_data = Data()
    pool = Pool()
    pool.starmap(f, [(i,) for i in range(100)])
```