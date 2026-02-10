# Solving UnicodeDecodeErrors Due to Opening Binary Files

[![](https://audreyfeldroy.github.io/arg-static/img/python-tip-600x314.png)](https://audreyfeldroy.github.io/arg-static/img/python-tip-600x314.png)

  
  

## Common Scenario: Walking Directory Tree and Opening Files

A common thing to do in Python is to go through a directory tree, opening each file and doing something with the file's text.  
  

```
for path in paths:
    for line in open(path, 'r'):
        # Do something with each line of the file here.
        # Go ahead, right inside the for loop.
        # It's a text file, so imagine the possibilities.
```

  
Here, we iterate over all the paths in the directory tree. For each path, we open the file for reading. Then we go through each line of the file and do something with it.  
  

## The Problem

This works well enough for many situations, but at some point you end up running into a UnicodeDecodeError when you try to open a particular file. Usually, it's because that file isn't a text file: for example, it might be a JPEG or a font file.  
  
Those errors are scary! They look like this:   
  

```
for line in open(path, 'r'):
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <encodings.utf_8.IncrementalDecoder object at 0x10349a320>
input = b"\x00\x00\x01\x00\x02\x00  \x00\x00\x01\x00 \x00(\x10\x00\x00&\x00\x00\x00\x10\x10\x00\x00\x01\x00 \x00(\x04\x00\x00N...00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
final = False

def decode(self, input, final=False):
    # decode input (taking the buffer into account)
    data = self.buffer + input
>       (result, consumed) = self._buffer_decode(data, self.errors, final)
E       UnicodeDecodeError: 'utf-8' codec can't decode byte 0xad in position 89: invalid start byte
```

  
Before you go into a UnicodeDecodePanic trying out all the variants of open, io.open, unicode\_open, etc., think about whether the file you're trying to open is even a text file.  
  

## The Solution

To solve the problem of accidentally opening non-text files, you can use [BinaryOrNot](https://github.com/audreyr/binaryornot)'s is\_binary function. Just check to make sure the file isn't a binary before attempting to open it, like this:   
  

```
from binaryornot.check import is_binary

for path in paths:
    if not is_binary(path):
        for line in open(path, 'r'):
            # Do something with each line of the file here.
            # Go ahead, right inside the for loop.
            # It's a text file, so imagine the possibilities.
```

  
This is a real-life code example. In fact, it comes from a fix to cookiecutter-django's tests that I just [committed this weekend](https://github.com/pydanny/cookiecutter-django/commit/7e8f58d6ec472f6e5effc291f00471d32d64c686), which comes from [Cookiecutter core code](https://github.com/audreyr/cookiecutter/blob/5b997e8e2f5d4773eff62f95afe7426c23bbfeed/cookiecutter/generate.py#L156-L159).  
  
BinaryOrNot is a package that guesses whether a file is binary or text. I put it together a couple of years ago in order to use it in Cookiecutter. Since then, I've found uses for it over and over in various projects.  
  

## More Info

BinaryOrNot on GitHub: <https://github.com/audreyr/binaryornot>  
Project documentation: <http://binaryornot.readthedocs.org/>