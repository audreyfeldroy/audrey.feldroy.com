# FastHTML and MonsterUI Time Converter

A FastHTML app that converts times to different timezones, and to Discord timestamps.


```python
from datetime import datetime
from fastcore.utils import *
from fasthtml.common import *
from fasthtml.jupyter import *
from monsterui.all import *
from zoneinfo import ZoneInfo
```

## Bring Over Time Conversion Functions

This code is from [Functional Programming with datetime, and Omni-Timezone Discord Timestamps](https://audrey.feldroy.com/nbs/2025-01-28-Functional-Programming-with-datetime-and-Omni-Timezone-Discord-Timestamps).


```python
#| export
tzs = L('America/Los_Angeles', 'America/Chicago', 'America/New_York', 'Europe/London', 'Europe/Istanbul', 'Australia/Brisbane',)
tzs
```




    (#6) ['America/Los_Angeles','America/Chicago','America/New_York','Europe/London','Europe/Istanbul','Australia/Brisbane']




```python
#| export
def time_in_tz(tz:str, dt:datetime|None=None) -> str: 
    if dt is None: dt = datetime.now()
    dt = dt.astimezone(ZoneInfo(tz))
    return f"{tz:20} {dt:%H:%M}"
tzs.map(time_in_tz).map(print)
```

    America/Los_Angeles  07:49
    America/Chicago      09:49
    America/New_York     10:49
    Europe/London        15:49
    Europe/Istanbul      18:49
    Australia/Brisbane   01:49





    (#6) [None,None,None,None,None,None]




```python
#| export
def print_discord_time(dt:datetime|None=None) -> None:
    if dt is None: dt = datetime.now()
    print(f"{"Discord":20} <t:{int(dt.timestamp())}:f>")
print_discord_time()
```

    Discord              <t:1738597748:f>



```python
#| export
def print_times(dt:datetime|None=None) -> None:
    if dt is None: dt = datetime.now()
    tzs = L('America/Los_Angeles', 'America/Chicago', 'America/New_York', 'Europe/London', 'Europe/Istanbul', 'Australia/Brisbane')
    tzs.map(time_in_tz).map(print)
    print_discord_time(dt)
print_times()
```

    America/Los_Angeles  07:49
    America/Chicago      09:49
    America/New_York     10:49
    Europe/London        15:49
    Europe/Istanbul      18:49
    Australia/Brisbane   01:49
    Discord              <t:1738597748:f>


## Make a TimeConverter FastTag


```python
app, rt = fast_app(hdrs=(Theme.slate.headers(),))
```


```python
def TimeConverter():
    return Form(
        H3("Convert a Time", cls="text-base font-semibold text-gray-900 dark:text-slate-100"),
        Input(name="dt", type="datetime-local", value="2025-02-03T14:30"),
        Button("Submit", cls=ButtonT.primary), hx_post="/convert", hx_target="#grid", hx_swap="outerHTML")

show(TimeConverter())
```


<form enctype="multipart/form-data" hx-post="/convert" hx-swap="outerHTML" hx-target="#grid" class="space-y-3">  <h3 class="uk-h3 text-base font-semibold text-gray-900 dark:text-slate-100">Convert a Time</h3>
  <input name="dt" type="datetime-local" value="2025-02-03T14:30" class="uk-input ">
<button type="submit" class="uk-button uk-button-primary">Submit</button></form><script>if (window.htmx) htmx.process(document.body)</script>



```python
dt = datetime.now()
dt
```




    datetime.datetime(2025, 2, 3, 16, 8, 55, 368904)




```python
def TimeTable(dt):
    tzs = L('America/Los_Angeles', 'America/Chicago', 'America/New_York', 'Europe/London', 'Europe/Istanbul', 'Australia/Brisbane',)
    return Table(
        Thead(Tr(Th(f"{dt:%a, %b %-d, %Y %H:%M} GMT is also", colspan=2))),
        *[Tr(
            Td(tz),
            Td(time_in_tz(tz, dt).split()[-1])
          ) for tz in tzs],
        Tr(Td("Discord"), Td(f"<t:{int(dt.timestamp())}:f>"))
    )
```


```python
show(TimeTable(dt))
```


<table class="uk-table uk-table-middle uk-table-divider uk-table-hover uk-table-small">
  <thead>
    <tr>
      <th colspan="2">Mon, Feb 3, 2025 16:08 GMT is also</th>
    </tr>
  </thead>
  <tr>
    <td>America/Los_Angeles</td>
    <td>08:08</td>
  </tr>
  <tr>
    <td>America/Chicago</td>
    <td>10:08</td>
  </tr>
  <tr>
    <td>America/New_York</td>
    <td>11:08</td>
  </tr>
  <tr>
    <td>Europe/London</td>
    <td>16:08</td>
  </tr>
  <tr>
    <td>Europe/Istanbul</td>
    <td>19:08</td>
  </tr>
  <tr>
    <td>Australia/Brisbane</td>
    <td>02:08</td>
  </tr>
  <tr>
    <td>Discord</td>
    <td>&lt;t:1738598935:f&gt;</td>
  </tr>
</table>
<script>if (window.htmx) htmx.process(document.body)</script>


## Define Routes


```python
@rt
def index():
    dt = datetime.now()
    return Grid(TimeTable(dt), TimeConverter(), id="grid")
```


```python
@rt
def convert(dt:str):
    dt = datetime.fromisoformat(dt).replace(tzinfo=ZoneInfo('Europe/London'))
    return (TimeTable(dt), TimeConverter())
```


```python
server = JupyUvi(app)
```



<script>
document.body.addEventListener('htmx:configRequest', (event) => {
    if(event.detail.path.includes('://')) return;
    htmx.config.selfRequestsOnly=false;
    event.detail.path = `${location.protocol}//${location.hostname}:8000${event.detail.path}`;
});
</script>



```python
server.stop()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[16], line 1
    ----> 1 server.stop()


    NameError: name 'server' is not defined



```python

```
