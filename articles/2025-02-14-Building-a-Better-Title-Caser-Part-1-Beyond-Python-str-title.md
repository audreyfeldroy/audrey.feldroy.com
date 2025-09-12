# Building a Better Title-Caser, Part 1: Beyond Python str.title

Title-casing text is one of those hard problems no one ever gets right, yet no one considers worthy enough to solve with AI. Here I experiment to see if I can improve upon the latest best solutions with a local Ollama modelfile and a solid prompt.

## Setup


```python
import google.generativeai as genai
import ollama
from titlecase import titlecase
```

## Built-In `title`

I begin by seeing what `str.title` does. It's built into Python, so nothing needs to be installed. 


```python
"hi".title()
```




    'Hi'



## PyPI `titlecase`

Now with `pip install titlecase`, I get this `titlecase` function:


```python
titlecase("hi")
```




    'Hi'



## Simple Multi-Word Ccomparison

Both of these functions should do well with a simple test case:


```python
text = "the quick brown fox"
print(f"title():    {text.title()}")
print(f"titlecase(): {titlecase(text)}")
```

    title():    The Quick Brown Fox
    titlecase(): The Quick Brown Fox


## With Apostrophes


```python
## With apostrophes
text2 = "it's a beautiful day in mr. rogers' neighborhood"
print(f"\ntitle():    {text2.title()}")
print(f"titlecase(): {titlecase(text2)}")
```

    
    title():    It'S A Beautiful Day In Mr. Rogers' Neighborhood
    titlecase(): It's a Beautiful Day in Mr. Rogers' Neighborhood


Here `titlecase` lowercased the articles correctly.

## Modern Terms With Unconventional Capitalization 


```python
text3 = "iphone and e-mail tips for pdfs"
print(f"\ntitle():    {text3.title()}")
print(f"titlecase(): {titlecase(text3)}")
```

    
    title():    Iphone And E-Mail Tips For Pdfs
    titlecase(): Iphone and E-Mail Tips for PDFS


My use case would be to title case voice-dictated text. Here there's something tricky because E-Mail is one of those terms where the hyphenation is debatable and undergoing change. Personally, I prefer email without the hyphen. It's interesting how I voice-dicated this paragraph (Wispr Flow) and it ended up both ways! 

My preference for a return value here is `iPhone and Email Tips for PDFs`. In situations where a hyphenated word is optionally unhyphenated, I'd like the title-casing function to unhyphenate and then title-case it. If that's not possible, my backup preference is `iPhone and E-Mail Tips for PDFs`.

## Using a Hosted LLM as a Title-Caser


```python
def tc_gemini(s):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    resp = model.generate_content(f"Convert '{s}' to title case, please. Return ONLY the title-cased string.", safety_settings=[], request_options={"timeout": 1000})
    try:
        return resp.text
    except Exception as ex:
        raise ex
```


```python
tc_gemini(text3)
```




    'iPhone and E-mail Tips for PDFs\n'



Gemini 1.5 Flash works decently as a title caster with this simple prompt. I noticed though that the mail and email isn't capitalized. That is one that people find confusing. The rule is when a word is hyphenated, each part of the hyphenated word should be capitalized. 

This feels a bit wasteful though with a lot of API calls to a service that will likely cost money in the future. I suppose you'd want to batch them if you went this way. I think it would be a lot nicer though to use a small local LLM for simple tasks like this. 

## Use Small Local LLMs as Title-Casers


```python
def tc_ollama(s, model='mistral'):
    # Call ollama with a simple title-case prompt
    response = ollama.chat(model=model, messages=[{
        'role': 'user',
        'content': f"Convert '{s}' to title case. Return ONLY the title-cased string with no explanation or quotes."
    }])
    return response['message']['content'].strip()
```


```python
print(tc_ollama(text3))
```

    [2025-02-16 07:31:46 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"


    iPhone and Email Tips for PDFs


Mistral is quite good. Let's try others:


```python
# Let's try a few different models to compare
models = ['llama3.2', 'tinyllama', 'deepseek-r1:7b', 'deepseek-coder:33b', 'qwen2.5:3b']
print("\nComparing models:")
for model in models:
    try:
        print(f"{model:10}: {tc_ollama(text3, model)}")
    except:
        print(f"{model:10}: Failed")
```

    
    Comparing models:


    [2025-02-16 07:32:14 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"


    llama3.2  : Iphone And E-Mail Tips For PDFs


    [2025-02-16 07:32:23 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"


    tinyllama : "IPHONE AND EMAIL TIPS FOR PDFS"


    [2025-02-16 07:33:41 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"


    deepseek-r1:7b: <think>
    Okay, so I need to convert "ipone and e-mail tips for pdfs" into title case. Hmm, first, what's title case? From what I remember, it's when each major word in a sentence is capitalized. So every time there's a new word that starts with a letter, that letter should be uppercase.
    
    Let me break down the original string: "ipone and e-mail tips for pdfs". Wait, let's make sure to split this correctly into words because sometimes it's easy to miscount or miss the spaces. I think the correct version is "iPhone and E-Mail Tips for PDFs". 
    
    Wait a second, no. The user wrote "ipone" but maybe that was a typo? iPhone should be "iPhone", right? So "ipone" might actually be incorrect. But in the given string, it's written as "ipone and e-mail tips for pdfs". Maybe they meant to say "iphone", so I'll proceed with that.
    
    So the original words are: "ipone", "and", "e-mail", "tips", "for", "pdfs".
    
    Now applying title case step by step:
    
    1. The first word is "ipone" – in title case, it should be "iPhone".
    2. Next word is "and" – already a conjunction, so it stays lowercase? Wait no, actually, each major word should have the first letter capitalized regardless of position. But "and" isn't a major word like "a", "an", etc., but in standard title case, all words are capitalized except for articles and prepositions which are lowercase. Hmm, I might be overcomplicating.
    
    Wait, perhaps it's better to think that each word starts with a capital letter regardless of its position unless it's an article or conjunction. But the user just asked for the string converted to title case without any explanation. So maybe "and" should stay as is? Or does it need to be capitalized?
    
    Actually, in some style guides, all words except the first are capitalized if they start a new clause, but that might complicate things. Maybe I'm overthinking this.
    
    So perhaps the user just wants each word with its first letter capitalized, regardless of whether it's an article or not. So "iPhone" becomes "iPhone", then "and" would be "And", "e-mail" becomes "E-Mail"? Wait no, usually email is in lowercase unless it starts a sentence. But perhaps for this task, just capitalizing the first letter.
    
    But looking back at examples, when people title case sentences, they capitalize each word that begins with a capital letter in the original. So maybe "ipone and e-mail tips for pdfs" becomes "iPhone And E-Mail Tips For PDFs".
    
    Wait, but in English, the correct form is "E-mail", not "E-Mail". But perhaps the user meant to write it as an acronym or something else. Hmm.
    
    Alternatively, maybe they just want each word with its first letter capitalized without changing the structure of the sentence. So let me try that:
    
    Original words: "ipone and e-mail tips for pdfs"
    After capitalizing each word's first letter: "iPhone And E-Mail Tips For PdF"
    
    Wait no, in the query, it's "pdfs", which should be lowercase unless it's a proper noun. So perhaps the correct title cased string would be "iPhone And E-Mail Tips For PDFs".
    
    But wait, maybe I'm overcomplicating. The user just wants each word to have its first letter capitalized without changing anything else. So let me do that step by step.
    
    - "ipone" becomes "iPhone"
    - "and" becomes "And"
    - "e-mail" becomes "E-Mail"
    - "tips" becomes "Tips"
    - "for" becomes "For"
    - "pdfs" becomes "PDFs"
    
    So combining them all together: "iPhone And E-Mail Tips For PDFs".
    
    But I'm not sure if the user wants "E-Mail" or just "E_mail". But in the example response, it's written as "E_Mail Tips for PdFs", so maybe they want each word capitalized without changing the structure of the words beyond that.
    
    Wait no, looking at the initial example provided by me: I wrote "iPhone And E-Mail Tips For PDFs" but then changed my mind to "iPhone And E-Mail Tips For PDFs". Hmm, perhaps in this context, it's better to use "E-Mail" as per standard formatting. But since the user used an underscore initially, maybe they prefer that.
    
    Alternatively, perhaps I should follow the exact structure without changing punctuation unless necessary. So keeping "e-mail" as is but capitalizing the first letter.
    
    Wait no, in title case, each major word's first letter is capitalized. So "E-mail" would be correct, not "E_Mail". But if the user wrote it with an underscore, maybe they intended to write "E-Mail", so perhaps I should just capitalize that as well.
    
    But this might complicate things. Maybe for simplicity, since the user provided a specific example response where "E_Mail" and "PdFs", I can assume they want each part capitalized without considering standard punctuation rules unless instructed otherwise.
    
    So in summary, converting each word to title case would involve capitalizing the first letter of each word:
    
    - ipone → iPhone
    - and → And
    - e-mail → E-Mail (assuming they wanted it with an underscore)
    - tips → Tips
    - for → For
    - pdfs → PDFs
    
    So putting them together: "iPhone And E_Mail Tips For PDFs".
    
    Wait, but in the example I thought of earlier, I wrote it as "iPhone And E-Mail Tips For PDFs". So which one is correct? I think in this case, since the user's instruction was to convert without explanation or quotes, and they provided an example with underscores, perhaps the correct approach is to follow their example.
    
    In any case, I'll go with "iPhone And E-Mail Tips for PDFs", but given that the initial string didn't have spaces around "for" and "pdfs", maybe it's better without the space. Wait no, in the original query, it's "ipone and e-mail tips for pdfs" so when converted to title case with proper spacing, it should be "iPhone And E-Mail Tips For PDFs".
    
    But perhaps I'm overcomplicating again. The user just wants each word with its first letter capitalized without any further changes.
    </think>
    
    iPhone And E-Mail Tips For PDFs


    [2025-02-16 07:35:25 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"


    deepseek-coder:33b: Here is a Python solution that uses built in python methods to convert a sentence into title case.
    
    ```python
    def convert_to_titlecase(sentence):
        return sentence.title()
    
    print(convert_to_titlecase('iphone and e-mail tips for pdfs'))
    ```
    When you run this code, it will print: `'Iphone And E-Mail Tips For Pdfs'`


    [2025-02-16 07:35:28 - httpx:1025 - INFO] HTTP Request: POST http://127.0.0.1:11434/api/chat "HTTP/1.1 200 OK"


    qwen2.5:3b: Iphone And Email Tips For Pdfs

