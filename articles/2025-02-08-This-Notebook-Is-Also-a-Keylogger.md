# This Notebook Is Also a Keylogger

Here I play with using Pynput as a system level keylogger, from within my Jupyter notebook version of this.


```python
from pynput import keyboard 
```

## Print Key Presses and Releases


```python
def on_press(key):
    try: print(key.char, end='', flush=True)
    except AttributeError: print(key, end='', flush=True)
```


```python
def on_release(key):
    print(f"↑{key.char if hasattr(key, 'char') else key}", end='', flush=True)
    if key == keyboard.Key.esc: return False  # Stop listener
```

Yeah, I implemented them differently for variety, since this is all just for fun. The second feels nicer. 

## Listen (Non-Blocking)


```python
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
```

    ↑Key.enter↑Key.shifta↑aa↑aKey.enter↑Key.entera↑aaaaa↑aa↑as↑sKey.shift↑Key.shiftKey.shift_r↑Key.shift_rd↑dd↑dddddddddd↑dKey.esc↑Key.esc

Tags: jupyter, python, security
