# Clearing a Local Port That's in Use

How to find and kill an old process running on a particular port.

## Why This Matters

This is useful when you need to run something on a port and discover it's already in use. For example, if you're starting Uvicorn from a Jupyter notebook and get this error, and you don't want to just pick another port:

```sh
ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): [errno 48] address already in use
```

## Identify What's Running on the Port

Find the PID of whatever process is running on port 8000:


```python
% lsof -i :8000
COMMAND   PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  53995  arg   73u  IPv4 0xfd5e93838a5d5d03      0t0  TCP *:irdmi (LISTEN)
```

## Kill It and Recheck

Kill that process:


```python
% kill -9 53995
```

Now when you run lsof again, the process is gone:


```python
% lsof -i :8000
```
