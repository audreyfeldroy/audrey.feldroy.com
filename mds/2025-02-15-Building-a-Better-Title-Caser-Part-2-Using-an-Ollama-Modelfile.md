# Building a Better Title-Caser, Part 2: Using an Ollama Modelfile

Here I create a local titlecase model based on Mistral, using a local Ollama modelfile and a solid prompt.

## Setup


```python
import google.generativeai as genai
import ollama
from titlecase import titlecase
```

## Create an Mistral-Based Model With an Ollama Modelfile

For better title casing, perhaps I can create an Ollama modelfile starting with a good model like mistral. I put this into `tc.modelfile`:

```
FROM mistral
PARAMETER temperature 0.1
PARAMETER num_ctx 512

# System prompt to specialize the model
SYSTEM """You are a title case expert. You follow these rules:
- Capitalize brand names correctly (e.g. iPhone, iPad)
- Keep acronyms in all caps (e.g. PDF, HTML)
- Hyphenated words have first letter of each word capitalized (e.g. E-Mail)
- Don't capitalize articles/conjunctions unless first word
Return only the properly title-cased text with no explanation."""
```

I created and used this model with:

```sh
ollama create titlecase -f tc.modelfile
```

I can see my new model with:

```sh
(uv) ~ % ollama list
NAME                  ID              SIZE      MODIFIED
titlecase:latest      255c41b01169    4.1 GB    14 minutes ago
```

I then defined a titlecase function with it:


```python
def tc(s):
    return ollama.chat(model='titlecase', messages=[{
        'role': 'user',
        'content': f"Convert to title case: {s}"
    }])['message']['content'].strip()
```


```python
tc("iphone and e-mail tips for pdfs")
```

    [2025-02-16 09:25:08 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"





    'iPhone and E-Mail Tips for PDFs'




```python
tc("iphone and email tips for pdfs")
```

    [2025-02-16 09:25:19 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"





    'iPhone and Email Tips for PDFs'



The results are great. Of course this is just one test case. 

## Future Topics

* Compare the different title case functions more, using other test cases. 
* See if I can get great performance out of another more lightweight local model. 
