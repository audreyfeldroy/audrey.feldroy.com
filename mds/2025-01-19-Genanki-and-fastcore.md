# Genanki and fastcore

Working with Anki flashcard decks in Python, with genanki to work with the decks and fastcore for ease of use.


```python
import genanki
from fastcore.utils import *
```

## Model

First I define a model with Q&A fields and a card template:


```python
my_model = genanki.Model(
  1607392319,
  'Simple  Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])
```

## Notes

I create a note:


```python
note_gm = genanki.Note(model=my_model, fields=['Magandang umaga', 'Good morning'])
note_gm
```




    Note(model=Model(model_id=1607392319, name='Simple  Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Magandang umaga', 'Good morning'], sort_field='Magandang umaga', tags=_TagList([]), guid='d?PmHtKm}t')



It's nice to bulk-create notes like this:


```python
notes = L(['Magandang hapon', 'Good afternoon'],
    ['Magandang gabi', 'Good evening'],
    ['Paalam', 'Goodbye'])
notes
```




    (#3) [['Magandang hapon', 'Good afternoon'],['Magandang gabi', 'Good evening'],['Paalam', 'Goodbye']]



Recall before that in `my_model` the first field goes into `Question` and the second goes into `Answer`.

Then to actually turn those list items into notes:


```python
def add_note(qa): return genanki.Note(model=my_model, fields=qa)
```


```python
gn = notes.map(add_note)
gn
```




    (#3) [Note(model=Model(model_id=1607392319, name='Simple  Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Magandang hapon', 'Good afternoon'], sort_field='Magandang hapon', tags=_TagList([]), guid='l!E%BkZ4ir'),Note(model=Model(model_id=1607392319, name='Simple  Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Magandang gabi', 'Good evening'], sort_field='Magandang gabi', tags=_TagList([]), guid='lB:)1uVms#'),Note(model=Model(model_id=1607392319, name='Simple  Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Paalam', 'Goodbye'], sort_field='Paalam', tags=_TagList([]), guid='n5_IDz@c|$')]



## Deck

Let's create a deck and add 1 starter note:


```python
my_deck = genanki.Deck(
  2059400110,
  'Tagalog Greetings')

my_deck.add_note(note_gm)
```

We can see the note's in the deck:


```python
my_deck.notes
```




    [Note(model=Model(model_id=1607392319, name='Simple Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Magandang umaga', 'Good morning'], sort_field='Magandang umaga', tags=_TagList([]), guid='d?PmHtKm}t')]



We extend it with the rest of the notes we bulk-created:


```python
my_deck.notes.extend(gn)
```


```python
my_deck.notes
```




    [Note(model=Model(model_id=1607392319, name='Simple Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Magandang umaga', 'Good morning'], sort_field='Magandang umaga', tags=_TagList([]), guid='d?PmHtKm}t'),
     Note(model=Model(model_id=1607392319, name='Simple  Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Magandang hapon', 'Good afternoon'], sort_field='Magandang hapon', tags=_TagList([]), guid='l!E%BkZ4ir'),
     Note(model=Model(model_id=1607392319, name='Simple  Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Magandang gabi', 'Good evening'], sort_field='Magandang gabi', tags=_TagList([]), guid='lB:)1uVms#'),
     Note(model=Model(model_id=1607392319, name='Simple  Model', fields=[{'name': 'Question'}, {'name': 'Answer'}], templates=[{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'}], css='', model_type=0), fields=['Paalam', 'Goodbye'], sort_field='Paalam', tags=_TagList([]), guid='n5_IDz@c|$')]



## Packaging the Deck for Anki

This writes out an Anki package file that we can import:


```python
genanki.Package(my_deck).write_to_file('tagalog_greetings.apkg')
```


```python
!ls *.apkg
```

    tagalog_greetings.apkg


## Opening the Deck in Anki

In Anki Desktop:
    
1. I went to File > Import
2. I chose tagalog_greetings.apkg
3. I was able to go through the cards like any other deck!

## Resources

* Genanki: https://github.com/kerrickstaley/genanki
* fastcore: https://fastcore.fast.ai/
