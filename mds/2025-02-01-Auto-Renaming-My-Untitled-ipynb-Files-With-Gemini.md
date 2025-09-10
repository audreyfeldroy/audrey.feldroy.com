# Auto-Renaming My Untitled.ipynb Files With Gemini 1.5 Flash

I'm starting to accumulate many UntitledX.ipynb files. Here I use the Gemini 1.5 Flash language model from Google to rename each one based on its contents.


```python
from datetime import datetime
from execnb.nbio import read_nb
from fastcore.utils import *
import google.generativeai as genai
from pathlib import Path
```

## Desired File Format

YYYY-MM-DD-Title-of-Notebook-in-TitleCase-With-Hyphens.ipynb

## Get the Untitled Notebooks


```python
nbs = L(Path().glob("Untitled*.ipynb"))
nbs
```




    (#32) [Path('Untitled10.ipynb'),Path('Untitled7.ipynb'),Path('Untitled12.ipynb'),Path('Untitled5.ipynb'),Path('Untitled1.ipynb'),Path('Untitled16.ipynb'),Path('Untitled30.ipynb'),Path('Untitled29.ipynb'),Path('Untitled3.ipynb'),Path('Untitled14.ipynb'),Path('Untitled4.ipynb'),Path('Untitled13.ipynb'),Path('Untitled6.ipynb'),Path('Untitled11.ipynb'),Path('Untitled1-Copy1.ipynb'),Path('Untitled15.ipynb'),Path('Untitled2.ipynb'),Path('Untitled28.ipynb'),Path('Untitled17.ipynb'),Path('Untitled26.ipynb')...]




```python
nb = nbs[0]
```

## Get the Last Modified Date

To get each file's prefix, I get the file modified stats:


```python
Path(nb).stat().st_mtime
```




    1736267381.7581108



This returns a Unix timestamp. To get a more readable datetime:


```python
last_modified = datetime.fromtimestamp(Path(nb).stat().st_mtime)
last_modified
```




    datetime.datetime(2025, 1, 7, 16, 29, 41, 758111)




```python
last_modified.strftime('%Y-%m-%d')
```




    '2025-01-07'



## Check for an Existing Title

It would be in the first cell:


```python
cells = L(read_nb(nb).cells)
cells[0]
```




```json
{ 'cell_type': 'markdown',
  'id': 'c68e6923',
  'idx_': 0,
  'metadata': {},
  'source': 'git-nbdiffdriver diff: git-nbdiffdriver: command not found'}
```



## Ask Gemini to Title the Notebook


```python
model = genai.GenerativeModel('gemini-1.5-flash-latest')
model
```




    genai.GenerativeModel(
        model_name='models/gemini-1.5-flash-latest',
        generation_config={},
        safety_settings={},
        tools=None,
        system_instruction=None,
        cached_content=None
    )




```python
with open(x) as f:
    nb = f.read()
```


```python
def generate_title_part(nb):
    prompt = f"""Given this Jupyter notebook, create a filename following these EXACT steps:
1. Extract the title from the first cell if it starts with '#'. In this case it's: "FastHTML By Example, Part 2"
2. Convert to the format: Words-In-Title-Case-With-Hyphens.ipynb
3. Remove any special characters (like commas)
4. If the filename sounds repetitive, simplify it.
5. If the first cell does not contain a title, create one based on the entire notebook's contents.

<notebook>
{nb}
</notebook>

Return ONLY the filename, nothing else."""
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE",},
    ]
    response = model.generate_content(prompt, safety_settings=safety_settings, request_options = {"timeout": 1000})
    try:
        return response.text
    except Exception as ex:
        raise ex
```


```python
result = generate_title_part(nb)
print(result)
```

    Git-Nbdiffdriver-And-Nbstripout-Issues.ipynb
    


## Prefix the Title With the Date

Putting the full title together:


```python
full_title = f"{last_modified.strftime('%Y-%m-%d')}-{result.strip()}"
print(full_title)
```

    2025-01-07-Git-Nbdiffdriver-And-Nbstripout-Issues.ipynb


## Rename the File


```python
x
```




    Path('Untitled10.ipynb')




```python
new_path = Path(full_title)
```


```python
if new_path.exists():
    print(f"Warning: {new_path} already exists")
else:
    x.rename(new_path)
    print(f"Renamed {x} to {new_path}")
```

    Renamed Untitled10.ipynb to 2025-01-07-Git-Nbdiffdriver-And-Nbstripout-Issues.ipynb


## Make This All a Function

Let's put this all together into a function that we can call on several files.


```python
def rename_notebook(nb_path):
    """Rename an untitled notebook based on its contents and modification date"""
    date = datetime.fromtimestamp(Path(nb_path).stat().st_mtime).strftime('%Y-%m-%d')
    with open(nb_path) as f: nb = f.read()
    
    title_part = generate_title_part(nb)
    
    new_name = f"{date}-{title_part.strip()}"
    new_path = Path(new_name)
    
    if new_path.exists():
        print(f"Warning: {new_path} already exists")
        return nb_path
    else:
        nb_path.rename(new_path)
        print(f"Renamed {nb_path} to {new_path}")
        return new_path
```


```python
nbs = L(Path().glob("Untitled*.ipynb"))
nbs
```




    (#30) [Path('Untitled12.ipynb'),Path('Untitled5.ipynb'),Path('Untitled1.ipynb'),Path('Untitled16.ipynb'),Path('Untitled30.ipynb'),Path('Untitled29.ipynb'),Path('Untitled3.ipynb'),Path('Untitled14.ipynb'),Path('Untitled4.ipynb'),Path('Untitled13.ipynb'),Path('Untitled6.ipynb'),Path('Untitled11.ipynb'),Path('Untitled1-Copy1.ipynb'),Path('Untitled15.ipynb'),Path('Untitled2.ipynb'),Path('Untitled28.ipynb'),Path('Untitled17.ipynb'),Path('Untitled26.ipynb'),Path('Untitled24.ipynb'),Path('Untitled19.ipynb')...]




```python
new_paths = nbs.map(rename_notebook)
```

    Renamed Untitled12.ipynb to 2025-01-11-Fastai-Tokenizers.ipynb
    Renamed Untitled5.ipynb to 2025-01-06-Fastlite-With-Files.ipynb
    Renamed Untitled1.ipynb to 2025-01-04-Tone-Js-And-FastHTML.ipynb
    Renamed Untitled16.ipynb to 2025-01-10-Untitled.ipynb
    Renamed Untitled30.ipynb to 2025-01-29-Untitled.ipynb
    Renamed Untitled29.ipynb to 2025-01-26-Numberblocks-6.ipynb
    Renamed Untitled3.ipynb to 2025-01-05-Fast-HTML-By-Example-Part-2.ipynb
    Renamed Untitled14.ipynb to 2025-01-14-London-Kolkata-Manila-Brisbane-Time-Conversion.ipynb
    Renamed Untitled4.ipynb to 2025-01-06-Updating-Git-Repos-With-Unstaged-Changes-Check.ipynb
    Renamed Untitled13.ipynb to 2025-01-12-Numberblock-2.ipynb
    Renamed Untitled6.ipynb to 2025-01-06-SQLite-CLI-Power-Users-Guide.ipynb
    Renamed Untitled11.ipynb to 2025-01-16-Using-FastCaddy-With-MonsterUI.ipynb
    Renamed Untitled1-Copy1.ipynb to 2025-01-04-Check-Each-Repo-For-Uncommitted-Changes.ipynb
    Renamed Untitled15.ipynb to 2025-01-11-Untitled-Notebook.ipynb



    ---------------------------------------------------------------------------

    ResourceExhausted                         Traceback (most recent call last)

    Cell In[94], line 1
    ----> 1 new_paths = nbs.map(rename_notebook)


    File ~/git/fastcore/fastcore/foundation.py:163, in L.map(self, f, *args, **kwargs)
    --> 163 def map(self, f, *args, **kwargs): return self._new(map_ex(self, f, *args, gen=False, **kwargs))


    File ~/git/fastcore/fastcore/basics.py:927, in map_ex(iterable, f, gen, *args, **kwargs)
        925 res = map(g, iterable)
        926 if gen: return res
    --> 927 return list(res)


    File ~/git/fastcore/fastcore/basics.py:912, in bind.__call__(self, *args, **kwargs)
        910     if isinstance(v,_Arg): kwargs[k] = args.pop(v.i)
        911 fargs = [args[x.i] if isinstance(x, _Arg) else x for x in self.pargs] + args[self.maxi+1:]
    --> 912 return self.func(*fargs, **kwargs)


    Cell In[90], line 6, in rename_notebook(nb_path)
          3 date = datetime.fromtimestamp(Path(nb_path).stat().st_mtime).strftime('%Y-%m-%d')
          4 with open(nb_path) as f: nb = f.read()
    ----> 6 title_part = generate_title_part(nb)
          8 new_name = f"{date}-{title_part.strip()}"
          9 new_path = Path(new_name)


    Cell In[72], line 20, in generate_title_part(nb)
          2     prompt = f"""Given this Jupyter notebook, create a filename following these EXACT steps:
          3 1. Extract the title from the first cell if it starts with '#'. In this case it's: "FastHTML By Example, Part 2"
          4 2. Convert to the format: Words-In-Title-Case-With-Hyphens.ipynb
       (...)
         12 
         13 Return ONLY the filename, nothing else."""
         14     safety_settings = [
         15         {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE",},
         16         {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE",},
         17         {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE",},
         18         {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE",},
         19     ]
    ---> 20     response = model.generate_content(prompt, safety_settings=safety_settings, request_options = {"timeout": 1000})
         21     try:
         22         return response.text


    File ~/.venv/lib/python3.12/site-packages/google/generativeai/generative_models.py:331, in GenerativeModel.generate_content(self, contents, generation_config, safety_settings, stream, tools, tool_config, request_options)
        329         return generation_types.GenerateContentResponse.from_iterator(iterator)
        330     else:
    --> 331         response = self._client.generate_content(
        332             request,
        333             **request_options,
        334         )
        335         return generation_types.GenerateContentResponse.from_response(response)
        336 except google.api_core.exceptions.InvalidArgument as e:


    File ~/.venv/lib/python3.12/site-packages/google/ai/generativelanguage_v1beta/services/generative_service/client.py:830, in GenerativeServiceClient.generate_content(self, request, model, contents, retry, timeout, metadata)
        827 self._validate_universe_domain()
        829 # Send the request.
    --> 830 response = rpc(
        831     request,
        832     retry=retry,
        833     timeout=timeout,
        834     metadata=metadata,
        835 )
        837 # Done; return the response.
        838 return response


    File ~/.venv/lib/python3.12/site-packages/google/api_core/gapic_v1/method.py:131, in _GapicCallable.__call__(self, timeout, retry, compression, *args, **kwargs)
        128 if self._compression is not None:
        129     kwargs["compression"] = compression
    --> 131 return wrapped_func(*args, **kwargs)


    File ~/.venv/lib/python3.12/site-packages/google/api_core/retry/retry_unary.py:293, in Retry.__call__.<locals>.retry_wrapped_func(*args, **kwargs)
        289 target = functools.partial(func, *args, **kwargs)
        290 sleep_generator = exponential_sleep_generator(
        291     self._initial, self._maximum, multiplier=self._multiplier
        292 )
    --> 293 return retry_target(
        294     target,
        295     self._predicate,
        296     sleep_generator,
        297     timeout=self._timeout,
        298     on_error=on_error,
        299 )


    File ~/.venv/lib/python3.12/site-packages/google/api_core/retry/retry_unary.py:153, in retry_target(target, predicate, sleep_generator, timeout, on_error, exception_factory, **kwargs)
        149 # pylint: disable=broad-except
        150 # This function explicitly must deal with broad exceptions.
        151 except Exception as exc:
        152     # defer to shared logic for handling errors
    --> 153     _retry_error_helper(
        154         exc,
        155         deadline,
        156         sleep,
        157         error_list,
        158         predicate,
        159         on_error,
        160         exception_factory,
        161         timeout,
        162     )
        163     # if exception not raised, sleep before next attempt
        164     time.sleep(sleep)


    File ~/.venv/lib/python3.12/site-packages/google/api_core/retry/retry_base.py:212, in _retry_error_helper(exc, deadline, next_sleep, error_list, predicate_fn, on_error_fn, exc_factory_fn, original_timeout)
        206 if not predicate_fn(exc):
        207     final_exc, source_exc = exc_factory_fn(
        208         error_list,
        209         RetryFailureReason.NON_RETRYABLE_ERROR,
        210         original_timeout,
        211     )
    --> 212     raise final_exc from source_exc
        213 if on_error_fn is not None:
        214     on_error_fn(exc)


    File ~/.venv/lib/python3.12/site-packages/google/api_core/retry/retry_unary.py:144, in retry_target(target, predicate, sleep_generator, timeout, on_error, exception_factory, **kwargs)
        142 for sleep in sleep_generator:
        143     try:
    --> 144         result = target()
        145         if inspect.isawaitable(result):
        146             warnings.warn(_ASYNC_RETRY_WARNING)


    File ~/.venv/lib/python3.12/site-packages/google/api_core/timeout.py:120, in TimeToDeadlineTimeout.__call__.<locals>.func_with_timeout(*args, **kwargs)
        117     # Avoid setting negative timeout
        118     kwargs["timeout"] = max(0, self._timeout - time_since_first_attempt)
    --> 120 return func(*args, **kwargs)


    File ~/.venv/lib/python3.12/site-packages/google/api_core/grpc_helpers.py:78, in _wrap_unary_errors.<locals>.error_remapped_callable(*args, **kwargs)
         76     return callable_(*args, **kwargs)
         77 except grpc.RpcError as exc:
    ---> 78     raise exceptions.from_grpc_error(exc) from exc


    ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).


Several of my notebooks were renamed successfully! I ran out of quota, though. I was probably hitting the Gemini API too fast. Let's see where we are and try again.


```python
nbs = L(Path().glob("Untitled*.ipynb"))
nbs
```




    (#16) [Path('Untitled2.ipynb'),Path('Untitled28.ipynb'),Path('Untitled17.ipynb'),Path('Untitled26.ipynb'),Path('Untitled24.ipynb'),Path('Untitled19.ipynb'),Path('Untitled20.ipynb'),Path('Untitled8.ipynb'),Path('Untitled22.ipynb'),Path('Untitled18.ipynb'),Path('Untitled25.ipynb'),Path('Untitled9-Copy1.ipynb'),Path('Untitled27.ipynb'),Path('Untitled23.ipynb'),Path('Untitled9.ipynb'),Path('Untitled21.ipynb')]




```python
new_paths = nbs.map(rename_notebook)
```

    Renamed Untitled2.ipynb to 2025-01-03-Fast-HTML-By-Example-Part-2.ipynb
    Renamed Untitled28.ipynb to 2025-01-23-Fast-HTML-By-Example-Part-2.ipynb
    Warning: 2025-01-11-My-Daily-Notebook-Workflow.ipynb already exists
    Renamed Untitled26.ipynb to 2025-01-23-Using-fastlite-and-apswutils.ipynb
    Renamed Untitled24.ipynb to 2025-01-19-Exploring-Lucide-Icons.ipynb
    Renamed Untitled19.ipynb to 2025-01-14-Discord-Message-Time-Converter.ipynb
    Renamed Untitled20.ipynb to 2025-01-16-Fast-HTML-By-Example-Part-2.ipynb
    Renamed Untitled8.ipynb to 2025-01-07-Use-Pathlib-For-Paths-Not-Env-Vars.ipynb
    Renamed Untitled22.ipynb to 2025-01-17-AAI-Meeting-Notes-2025-01-17.ipynb
    Renamed Untitled18.ipynb to 2025-01-12-Untitled.ipynb
    Renamed Untitled25.ipynb to 2025-01-21-Making-CLI-Tools-With-Fastcore-Script.ipynb
    Renamed Untitled9-Copy1.ipynb to 2025-01-07-FtResponse-In-FastHTML.ipynb
    Renamed Untitled27.ipynb to 2025-01-23-Modifying-Execnb-Render_outputs-To-Use-Monsterui.ipynb
    Renamed Untitled23.ipynb to 2025-01-26-Understanding-FastHTMLs-FT-Class.ipynb
    Warning: 2025-01-07-FtResponse-In-FastHTML.ipynb already exists
    Renamed Untitled21.ipynb to 2025-01-17-SVD-Finetuning-Exploration.ipynb


Mostly done! The 2 warnings sound like I have duplicates.


```python
nbs = L(Path().glob("Untitled*.ipynb"))
nbs
```




    (#2) [Path('Untitled17.ipynb'),Path('Untitled9.ipynb')]



Finally, I'm checking those remaining notebooks. It appears those are variations on the ones that exist. I can manually merge those.
