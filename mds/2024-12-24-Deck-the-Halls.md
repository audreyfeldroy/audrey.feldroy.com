# Deck the Halls


```python
from fastcore.all import *
```


```python
x = "Deck the halls with boughs of holly"
x
```


```python
L("la")*8
```


```python
def sing(): return L("Fa", *L("la")*8)
```


```python
sing()
```


```python
print("Tis the season to be jolly")
```


```python
" ".join(sing())
```


```python
repr("Don we now our gay apparel")
```


```python
s = sing()
s
```


```python
"".join(s[0:3])
```


```python
for i in range(0,3): print("".join(s[i:i+3]))
```


```python
"Troll the ancient yuletide carol"
```


```python
L(zip(s[0:5], s[1:5])) + 'la'
```
