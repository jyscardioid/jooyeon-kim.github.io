---
title: 'Run Tensorboard (or Jupyter) in a Remote Docker Container'
date: 2020-06-30
permalink: /blogs/tensorboard-in-a-docker-container/
tags:
  - Machine Learning Engineering
summary: ""
---

When creating a container, forward two ports 22 (for ssh) and 6006 (for Tensorboard).
```bash
docker run -ti --runtime=nvidia -p 8082:22 -p 8083:6006 nvidia/cuda:10.0-cudnn7-devel-ubuntu16.04 /bin/bash
```

We can access a container with ssh by,
```bash
ssh <user>@<host> -p 8082
```

## Access through localhost

In a remote container, run Tensorboard with 6006 (the default port).
```bash
tensorboard --logdir lightning_logs
```
```
TensorFlow installation not found - running with reduced feature set.
Serving TensorBoard on localhost; to expose to the network, use a proxy or pass --bind_all
TensorBoard 2.2.2 at http://localhost:6006/ (Press CTRL+C to quit)
```

In a local machine, bind local's 8083 port to remote's 6006 port.
```
ssh -L 8083:127.0.0.1:6006 <user>@<host> -p 8082
```

Now, we can access the Tensorboard web interface using the address `localhost:8083` in a local machine.

You can use Jupyter in the same way. Just change 6006 to 8888 (the default port in Jupyter).

## Access through IP address or domain name

If you want to access the Tensorboard through the IP address or domain name of the server, add `--host 0.0.0.0` to tensorboard command.

```bash
tensorboard --logdir lightning_logs --host 0.0.0.0
```

You can access the Tensorboard page with `http://<host>:8083` on any kind of machine connected to the internet.