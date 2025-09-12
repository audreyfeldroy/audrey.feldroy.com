# Delegates Decorator

My study of the `@delegates` decorator and `GetAttr` from `fastcore`.

I follow https://www.fast.ai/posts/2019-08-06-delegation.html


```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade
```


```python
student = Student("Alice", 12, 'A')
print(student.name, student.age, student.grade)
```

    Alice 12 A



```python
kid = Student("Uma", 5.5, 'Good Kid!')
print(kid.name, kid.age, kid.grade)
```

    Uma 5.5 Good Kid!



```python
%pip install fastcore
```


```python
from fastcore.meta import delegates
```


```python
class Person:
    def __init__(self, name, age, **kwargs):
        self.name = name
        self.age = age

@delegates()
class Student(Person):
    def __init__(self, name, age, grade, **kwargs):
        super().__init__(name, age, **kwargs)
        self.grade = grade
```


```python
child = Student("Amira", 6, grade='A', school='XYZ')
child.__dict__
```




    {'name': 'Amira', 'age': 6, 'grade': 'A'}




```python
from fastcore.basics import GetAttr
```


```python
class Strawberry(GetAttr):
    def __init__(self, color, variety):
        self.color, self.variety = color, variety
        self.default = color
```


```python
s = Strawberry('red', 'Pegasus')
s.color, s.variety, s.default
```




    ('red', 'Pegasus', 'red')




```python
[s for s in dir(s) if not s.startswith('_')]
```




    ['capitalize',
     'casefold',
     'center',
     'color',
     'count',
     'default',
     'encode',
     'endswith',
     'expandtabs',
     'find',
     'format',
     'format_map',
     'index',
     'isalnum',
     'isalpha',
     'isascii',
     'isdecimal',
     'isdigit',
     'isidentifier',
     'islower',
     'isnumeric',
     'isprintable',
     'isspace',
     'istitle',
     'isupper',
     'join',
     'ljust',
     'lower',
     'lstrip',
     'maketrans',
     'partition',
     'removeprefix',
     'removesuffix',
     'replace',
     'rfind',
     'rindex',
     'rjust',
     'rpartition',
     'rsplit',
     'rstrip',
     'split',
     'splitlines',
     'startswith',
     'strip',
     'swapcase',
     'title',
     'translate',
     'upper',
     'variety',
     'zfill']




```python
def play(game, player='Daddy', num_players=2):
    print(f'{player} is playing {game}')

play('chess', 'Mehdiya')
```

    Mehdiya is playing chess



```python
@delegates(play)
def play_chess(player, speed='blitz', **kwargs):
    play('chess', player)

play_chess('Uma')
```

    Uma is playing chess



```python
print(play_chess.__signature__)
```

    (player, speed='blitz', *, num_players=2)



```python
import inspect
print(inspect.signature(play_chess))
```

    (player, speed='blitz', *, num_players=2)



```python
print(inspect.signature(play))
```

    (game, player='Daddy', num_players=2)

