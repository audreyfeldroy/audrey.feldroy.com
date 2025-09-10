# Functional Programming with datetime, and Omni-Timezone Discord Timestamps

I define various useful datetime utilities with the help of fastcore's L and map, and functools' partial. Then I extend that to generate Discord timestamps, which localize Unix timestamps to the reader's timezone.


```python
from datetime import datetime
from fastcore.utils import *
from functools import partial
from zoneinfo import ZoneInfo
```

## Overview

I've been finding it helpful to use datetime with fastcore's L and map, and functools' partial. 

I shared some useful functions here to print my colleagues' current times, and generate Discord timestamps which localize Unix timestamps to the user's timezone.

## Converting the Current Time

We start off by doing things the classic way using Python stdlib datetime, which is actually quite good.


```python
datetime.now()
```




    datetime.datetime(2025, 2, 3, 10, 42, 15, 930074)



`now()` can take a timezone:


```python
dt = datetime.now(tz=ZoneInfo('Europe/London'))
dt
```




    datetime.datetime(2025, 2, 3, 10, 42, 16, 763220, tzinfo=zoneinfo.ZoneInfo(key='Europe/London'))




```python
nyc = dt.astimezone(ZoneInfo('America/New_York'))
nyc
```




    datetime.datetime(2025, 2, 3, 5, 42, 16, 763220, tzinfo=zoneinfo.ZoneInfo(key='America/New_York'))



Let's make a list of timezones:


```python
tzs = L('America/Los_Angeles', 'America/Chicago', 'America/New_York', 'Europe/London', 'Europe/Istanbul', 'Australia/Brisbane',)
tzs
```




    (#6) ['America/Los_Angeles','America/Chicago','America/New_York','Europe/London','Europe/Istanbul','Australia/Brisbane']



Now we map that timezone list to a "time in that timezone" function:


```python
def time_in_tz(tz:str, dt:datetime|None=None) -> str: 
    if dt is None: dt = datetime.now()
    dt = dt.astimezone(ZoneInfo(tz))
    return f"{tz:20} {dt:%H:%M}"
tzs.map(time_in_tz).map(print)
```

    America/Los_Angeles  02:42
    America/Chicago      04:42
    America/New_York     05:42
    Europe/London        10:42
    Europe/Istanbul      13:42
    Australia/Brisbane   20:42





    (#6) [None,None,None,None,None,None]



## Converting a Future Time With Timezone

To get a time in the future for a particular timezone:


```python
tomorrow_3pm_est = datetime.now(ZoneInfo('America/New_York')).replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=1)
```

This also works and is more readable:


```python
datetime.fromisoformat('2025-01-30 15:00').replace(tzinfo=ZoneInfo('America/New_York'))
```




    datetime.datetime(2025, 1, 30, 15, 0, tzinfo=zoneinfo.ZoneInfo(key='America/New_York'))




```python
current_times = partial(time_in_tz, dt=tomorrow_3pm_est)
tzs.map(current_times).map(print)
```

    America/Los_Angeles  12:00
    America/Chicago      14:00
    America/New_York     15:00
    Europe/London        20:00
    Europe/Istanbul      23:00
    Australia/Brisbane   06:00





    (#6) [None,None,None,None,None,None]



## Adding Discord Timestamp

A Discord timestamp looks like <t:1738094460:F> where:

* 1738094460 is a Unix timestamp
* F is long date/time like "Tuesday, January 28, 2025 2:20 PM"

When you put one of those into a Discord message, it automatically shows in each user's local timezone.


```python
f"<t:{int(dt.timestamp())}:f>"
```




    '<t:1738579336:f>'




```python
def print_discord_time(dt:datetime|None=None) -> None:
    if dt is None: dt = datetime.now()
    print(f"{"Discord":20} <t:{int(dt.timestamp())}:f>")
print_discord_time()
```

    Discord              <t:1738579349:f>



```python
print_discord_time(tomorrow_3pm_est)
```

    Discord              <t:1738699200:f>


## Printing It All


```python
def print_times(dt:datetime|None=None) -> None:
    if dt is None: dt = datetime.now()
    tzs = L('America/Los_Angeles', 'America/Chicago', 'America/New_York', 'Europe/London', 'Europe/Istanbul', 'Australia/Brisbane')
    tzs.map(time_in_tz).map(print)
    print_discord_time(dt)
print_times()
```

    America/Los_Angeles  02:42
    America/Chicago      04:42
    America/New_York     05:42
    Europe/London        10:42
    Europe/Istanbul      13:42
    Australia/Brisbane   20:42
    Discord              <t:1738579355:f>


## Next Steps

Create a Time Converter tool: a FastTag I can use to convert time whenever I need to.
