# Semantic Search With Sentence Transformers and a Cross-Encoder Model

Continuing the Sentence Transformers exploration, I use a cross-encoder model to rank my notebooks by similarity to search queries.

## Setup


```python
from fastcore.utils import *
from pathlib import Path
from sentence_transformers import CrossEncoder
```

## Bi-Encoder vs. Cross-Encoder Model

A cross-encoder model takes 2 texts as input and outputs 1 similarity score. That means you can't precompute embeddings like I did with the bi-encoder model, but rather must use the cross-encoder model to generate similarities each time.

| Aspect | Bi-Encoder | Cross-Encoder |
|--------|------------|---------------|
| **Input/Output** | Encodes texts separately into embeddings | Takes text pair, outputs similarity score |
| **Accuracy** | Lower accuracy but sufficient for initial retrieval | Higher accuracy for relevance ranking |
| **Computational Cost** | More efficient (can pre-compute embeddings) | More expensive (must process each text pair) |
| **Scalability** | Good for large-scale retrieval | Poor for large datasets |
| **Use Case** | Initial retrieval from large corpus | Re-ranking a small set of candidates |
| **Storage** | Requires storing embeddings | No embedding storage needed |

Cross-encoders excel at precision, but are typically used after a bi-encoder has narrowed down search results to 10-100 documents. In my case, I have less than 100 notebooks on this site, so I can get away with using just a cross-encoder.

## Download a Cross-Encoder Model


```python
ce_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
```

## Get All Notebook Paths

We put each notebook to be searched into a list.


```python
def get_nb_paths(): 
    root = Path() if IN_NOTEBOOK else Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)
```


```python
nb_paths = get_nb_paths()
```


```python
def read_nb_simple(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        return f.read()
```


```python
nbs = L(nb_paths).map(read_nb_simple)
```

## Search for a Test Query String

Let's search my notebooks for a test string.


```python
q = "Web search"
hits = ce_model.rank(q, nbs, return_documents=False)
```


```python
hits[:10]
```




    [{'corpus_id': 37, 'score': np.float32(-4.74905)},
     {'corpus_id': 70, 'score': np.float32(-5.289769)},
     {'corpus_id': 1, 'score': np.float32(-5.520778)},
     {'corpus_id': 32, 'score': np.float32(-5.8513002)},
     {'corpus_id': 0, 'score': np.float32(-6.227929)},
     {'corpus_id': 38, 'score': np.float32(-6.256436)},
     {'corpus_id': 23, 'score': np.float32(-6.4169016)},
     {'corpus_id': 20, 'score': np.float32(-6.501535)},
     {'corpus_id': 54, 'score': np.float32(-6.5156918)},
     {'corpus_id': 43, 'score': np.float32(-6.5381203)}]




```python
def print_search_result(hit): print(f"{hit['score']} {nb_paths[hit['corpus_id']]}")
```


```python
L(hits[:10]).map(print_search_result)
```

    -4.749050140380859 2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb
    -5.289769172668457 2024-07-16_Xtend_Pico.ipynb
    -5.520778179168701 2025-04-14-Semantic-Search-With-Sentence-Transformers-and-a-Bi-Encoder-Model.ipynb
    -5.851300239562988 2025-01-20-Dark-and-Light-Mode-in-FastHTML.ipynb
    -6.22792911529541 2025-04-15-Semantic-Search-With-Sentence-Transformers-and-a-Cross-Encoder-Model.ipynb
    -6.256435871124268 2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb
    -6.416901588439941 2025-01-27-This-Site-Is-Now-Powered-by-This-Notebook-Part-3.ipynb
    -6.501534938812256 2025-01-30-This-Site-Is-Now-Powered-by-This-Notebook-Part-5.ipynb
    -6.515691757202148 2024-12-30-Images-In-Every-Way-In-Notebooks.ipynb
    -6.538120269775391 2025-01-08-HTML-Title-Tag-in-FastHTML.ipynb





    (#10) [None,None,None,None,None,None,None,None,None,None]



Those results seem not as good as those from the bi-encoder. Let's try another cross-encoder model.

## Another Cross-Encoder: ms-marco-MiniLM-L12-v2


```python
ce_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L12-v2")
```


    config.json:   0%|          | 0.00/791 [00:00<?, ?B/s]



    model.safetensors:   0%|          | 0.00/133M [00:00<?, ?B/s]



    tokenizer_config.json:   0%|          | 0.00/1.33k [00:00<?, ?B/s]



    vocab.txt:   0%|          | 0.00/232k [00:00<?, ?B/s]



    tokenizer.json:   0%|          | 0.00/711k [00:00<?, ?B/s]



    special_tokens_map.json:   0%|          | 0.00/132 [00:00<?, ?B/s]



    README.md:   0%|          | 0.00/3.66k [00:00<?, ?B/s]



```python
hits = ce_model.rank(q, nbs, return_documents=False)
```


```python
L(hits[:10]).map(print_search_result)
```

    -2.2172038555145264 2024-07-16_Xtend_Pico.ipynb
    -4.159910202026367 2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb
    -4.701387882232666 2025-04-15-Semantic-Search-With-Sentence-Transformers-and-a-Cross-Encoder-Model.ipynb
    -5.170993328094482 2025-02-12-My-Self-Analysis-of-How-to-Get-Back-to-Posting-Every-Day.ipynb
    -5.205975532531738 2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb
    -5.208843231201172 2025-04-14-Semantic-Search-With-Sentence-Transformers-and-a-Bi-Encoder-Model.ipynb
    -5.574733257293701 2025-01-20-Dark-and-Light-Mode-in-FastHTML.ipynb
    -5.780138969421387 2024-12-30-Images-In-Every-Way-In-Notebooks.ipynb
    -5.9362897872924805 2024-12-27-Notebook-Names-to-Cards.ipynb
    -6.101370334625244 2025-01-24-Creating-In-Notebook-Images-for-Social-Media-With-PIL-Pillow.ipynb





    (#10) [None,None,None,None,None,None,None,None,None,None]



Fascinating how "Web" is emphasized so much, rather than the idea of "Web search".

## Another Cross-Encoder: ms-marco-TinyBERT-L2-v2


```python
ce_model = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L2-v2")
hits = ce_model.rank(q, nbs, return_documents=False)
L(hits[:10]).map(print_search_result)
```


    config.json:   0%|          | 0.00/787 [00:00<?, ?B/s]



    model.safetensors:   0%|          | 0.00/17.6M [00:00<?, ?B/s]



    tokenizer_config.json:   0%|          | 0.00/1.33k [00:00<?, ?B/s]



    vocab.txt:   0%|          | 0.00/232k [00:00<?, ?B/s]



    tokenizer.json:   0%|          | 0.00/711k [00:00<?, ?B/s]



    special_tokens_map.json:   0%|          | 0.00/132 [00:00<?, ?B/s]



    README.md:   0%|          | 0.00/3.50k [00:00<?, ?B/s]


    -8.323616981506348 2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb
    -8.499364852905273 2025-04-14-Semantic-Search-With-Sentence-Transformers-and-a-Bi-Encoder-Model.ipynb
    -8.768281936645508 2025-04-15-Semantic-Search-With-Sentence-Transformers-and-a-Cross-Encoder-Model.ipynb
    -8.79620361328125 2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb
    -10.260381698608398 2024-08-05-Claudette-FastHTML.ipynb
    -10.28246784210205 2025-01-07-Verifying-Bluesky-Domain-in-FastHTML.ipynb
    -10.379759788513184 2024-07-15-Printing_Components.ipynb
    -10.407485961914062 2025-01-18-Alarm-Sounds-App.ipynb
    -10.417764663696289 2024-12-23-Exploring-execnb-and-nb2fasthtml.ipynb
    -10.446236610412598 2025-02-06-Creating-an-Accessible-Inline-Nav-FastTag.ipynb





    (#10) [None,None,None,None,None,None,None,None,None,None]



This seems the best! I like this ranking.

## Reflection

After experimenting with a few cross-encoder models, I found that the TinyBERT model (`cross-encoder/ms-marco-TinyBERT-L2-v2`) gave the most intuitive results out of both the cross-encoder and bi-encoder models. 

It seemed to understand the semantic relationship between "Web search" and my notebooks about search functionality better than the larger models.
