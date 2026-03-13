# SQLite FTS5 Tokenizers: `unicode61` and `ascii`

The SQLite FTS5 (full-text search) extension includes the built-in tokenizers unicode61, ascii, porter, and trigram, implemented in [fts5_tokenize.c](https://github.com/sqlite/sqlite/blob/master/ext/fts5/fts5_tokenize.c). [APSW](https://github.com/rogerbinns/apsw) provides a Python API to use those. 

Here we explore the default tokenizer `unicode61` and built-in tokenizer `ascii` in detail.

## Overview

When you use SQLite's FTS5 extension, you create a FTS5 virtual table and specify which of its tokenizers to use (or a custom one of your own).

The tokenizer defines how text is split into tokens, and how it'll be matched in searches.

## Setup


```python
import apsw
import apsw.ext
```


```python
connection = apsw.Connection("dbfile")
connection
```




    <apsw.Connection at 0x10dfb6e30>



## The Default SQLite FTS5 Tokenizer `unicode61`

This is implemented in SQLite [fts5_tokenize.c starting at line 175](https://github.com/sqlite/sqlite/blob/master/ext/fts5/fts5_tokenize.c#L175) with Python wrapper in APSW [fts5.py](https://github.com/rogerbinns/apsw/blob/master/apsw/fts5.py).


```python
tokenizer = connection.fts5_tokenizer("unicode61")
tokenizer
```




    <apsw.FTS5Tokenizer at 0x10df61c00>



I like the [apsw tokenizer docs'](https://rogerbinns.github.io/apsw/example-fts.html#tokenizers) test text:


```python
txt = """🤦🏼‍♂️ v1.2 Grey Ⅲ ColOUR! Don't jump -  🇫🇮你好世界 Straße
    हैलो वर्ल्ड Déjà vu Résumé SQLITE_ERROR"""
```


```python
encoded = txt.encode("utf8")
encoded
```




    b"\xf0\x9f\xa4\xa6\xf0\x9f\x8f\xbc\xe2\x80\x8d\xe2\x99\x82\xef\xb8\x8f v1.2 Grey \xe2\x85\xa2 ColOUR! Don't jump -  \xf0\x9f\x87\xab\xf0\x9f\x87\xae\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c Stra\xc3\x9fe\n    \xe0\xa4\xb9\xe0\xa5\x88\xe0\xa4\xb2\xe0\xa5\x8b \xe0\xa4\xb5\xe0\xa4\xb0\xe0\xa5\x8d\xe0\xa4\xb2\xe0\xa5\x8d\xe0\xa4\xa1 D\xc3\xa9j\xc3\xa0 vu R\xc3\xa9sum\xc3\xa9 SQLITE_ERROR"



Yeah, remember `txt` ends in `SQLITE_ERROR`, that's expected. Interesting that it doesn't get encoded by `fts5_tokenizer`.


```python
tokenized = tokenizer(encoded, apsw.FTS5_TOKENIZE_DOCUMENT, None, include_offsets=False)
tokenized
```




    [('🤦🏼',),
     ('v1',),
     ('2',),
     ('grey',),
     ('ⅲ',),
     ('colour',),
     ('don',),
     ('t',),
     ('jump',),
     ('你好世界',),
     ('straße',),
     ('ह',),
     ('ल',),
     ('वर',),
     ('ल',),
     ('ड',),
     ('deja',),
     ('vu',),
     ('resume',),
     ('sqlite',),
     ('error',)]



Observations about tokenization with `unicode61`:

| Observation | Example |
|------------|---------|
| Emojis are preserved as single tokens | `🤦🏼` |
| Numbers are separated on decimal points | `v1.2` → `v1`, `2` |
| Case is normalized to lowercase | `ColOUR` → `colour` |
| Single Roman numeral Unicode characters are preserved | `Ⅲ` → `ⅲ` |
| Apostrophes split words | `Don't` → `don`, `t` |
| Hyphens and spaces are removed | `jump -  🇫🇮你好世界` → `jump`, `你好世界` |
| Chinese characters stay together (Google Translate says `你好世界` is "Hello World") | `你好世界` kept as one token |
| German eszett (ß) is preserved | `Straße` → `straße` |
| Hindi written in Devanagari script is split into parts (Google Translate detects `हैलो वर्ल्ड` as Hindi for "Hello World": `है` "is", ) | `हैलो` → `ह`, `ल` |
| Diacritics are removed | `Déjà` → `deja` |
| Underscores split words | `SQLITE_ERROR` → `sqlite`, `error` |
| Emojis as part of a word are ignored (?) | `🇫🇮` in `🇫🇮你好世界` not tokenized |

## Included SQLite FTS5 Tokenizer `ascii`

This is implemented in SQLite [fts5_tokenize.c starting at line 18](https://github.com/sqlite/sqlite/blob/master/ext/fts5/fts5_tokenize.c#L18) with Python wrapper in APSW [fts5.py](https://github.com/rogerbinns/apsw/blob/master/apsw/fts5.py).


```python
tokenizer_ascii = connection.fts5_tokenizer("ascii")
tokenizer_ascii
```




    <apsw.FTS5Tokenizer at 0x10de5aec0>




```python
tokenized = tokenizer_ascii(encoded, apsw.FTS5_TOKENIZE_DOCUMENT, None, include_offsets=False)
tokenized
```




    [('🤦🏼\u200d♂️',),
     ('v1',),
     ('2',),
     ('grey',),
     ('Ⅲ',),
     ('colour',),
     ('don',),
     ('t',),
     ('jump',),
     ('🇫🇮你好世界',),
     ('straße',),
     ('हैलो',),
     ('वर्ल्ड',),
     ('déjà',),
     ('vu',),
     ('résumé',),
     ('sqlite',),
     ('error',)]



Comparing our `ascii` tokenization here with the above `unicode61` tokenization:

| Feature | unicode61 | ascii | Example |
|---------|-----------|--------|---------|
| Emoji handling | Preserves simple emojis | Keeps composite emojis with modifiers | `🤦🏼` vs `🤦🏼\u200d♂️` |
| Number splitting | Splits on decimal points | Same | `v1.2` → `v1`, `2` |
| Case normalization | Converts to lowercase | Same | `ColOUR` → `colour` |
| Roman numeral unicode characters | Preserves and lowercases as equivalent Unicode character | Preserves original Unicode character | `Ⅲ` → `ⅲ` vs `Ⅲ` |
| Apostrophes | Splits words | Same | `Don't` → `don`, `t` |
| Spaces/hyphens | Removes | Same | `jump -` → `jump` |
| CJK characters | Keeps together | Same | `你好世界` stays as one token |
| German eszett | Preserves | Same | `Straße` → `straße` |
| Devanagari script | Splits into parts | Keeps words together | `हैलो` → `ह`, `ल` vs `हैलो` |
| Diacritics | Removes | Preserves | `Déjà` → `deja` vs `déjà` |
| Underscores | Splits words | Same | `SQLITE_ERROR` → `sqlite`, `error` |
| Emoji as part of a word | Ignores | Keeps with following text | `🇫🇮你好世界` |

## Choosing a Tokenizer

There's no best tokenizer: choose based on your use case. Here I'm considering the use case of implementing search for a blog or simple personal website, such as this one.

Since I write my notebooks in English and don't really use emoji, the default of `unicode61` is fine.

## Search

To be continued...

## Credits

Thanks to [Daniel Roy Greenfeld](https://daniel.feldroy.com) for reviewing.

Tags: sqlite, python
