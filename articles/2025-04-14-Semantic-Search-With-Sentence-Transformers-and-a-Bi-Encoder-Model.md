# Semantic Search With Sentence Transformers and a Bi-Encoder Model

Here I use sentence transformers and a bi-encoder model to encode my notebooks as embeddings and implement semantic search.

## Setup


```python
from fastcore.utils import *
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
```

## Initialize Bi-Encoder

Here we download a bi-encoder model to use for the precomputed embeddings.


```python
bienc_model = SentenceTransformer('all-MiniLM-L6-v2')
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
nb_paths
```




    (#74) [Path('2025-04-15-Semantic-Search-With-Sentence-Transformers-and-a-Cross-Encoder-Model.ipynb'),Path('2025-04-14-Semantic-Search-With-Sentence-Transformers-and-a-Bi-Encoder-Model.ipynb'),Path('2025-04-08-Get-a-Jupyter-Notebook-Filename-From-Itself.ipynb'),Path('2025-03-20-Minimal-Screen-Recording-on-macOS-No-Third-Party-Apps-Required.ipynb'),Path('2025-03-14-Pi.ipynb'),Path('2025-02-20-One-Liner-to-Clean-Python-Bytecode.ipynb'),Path('2025-02-15-Building-a-Better-Title-Caser-Part-2-Using-an-Ollama-Modelfile.ipynb'),Path('2025-02-14-Building-a-Better-Title-Caser-Part-1-Beyond-Python-str-title.ipynb'),Path('2025-02-13-Excavating-a-Lost-CLI-Tool.ipynb'),Path('2025-02-12-My-Self-Analysis-of-How-to-Get-Back-to-Posting-Every-Day.ipynb'),Path('2025-02-09-An-Informationally-Dense-Index-Page.ipynb'),Path('2025-02-08-This-Notebook-Is-Also-a-Keylogger.ipynb'),Path('2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb'),Path('2025-02-06-Creating-an-Accessible-Inline-Nav-FastTag.ipynb'),Path('2025-02-05-Create-a-CLI-Tool-With-Fastcore-Script.ipynb'),Path('2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb'),Path('2025-02-03-FastHTML-and-MonsterUI-Time-Converter.ipynb'),Path('2025-02-02-Text-Embeddings-and-Cosine-Similarity.ipynb'),Path('2025-02-01-Auto-Renaming-My-Untitled-ipynb-Files-With-Gemini.ipynb'),Path('2025-01-31-Performance-Optimization-Moving-HTML-Class-Injection-from-lxml-to-Mistletoe.ipynb')...]



## Create an Embedding for Each Notebook

Now we can turn that list of notebook paths into embeddings by:

1. Opening each notebook file
2. Putting notebook content into a list of notebooks
3. Passing the notebook list to the bi-encoder model to generate a list of embeddings


```python
def read_nb_simple(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        return f.read()
```


```python
nbs = L(nb_paths).map(read_nb_simple)
```


```python
nb_embs = bienc_model.encode(nbs)
```


```python
len(nb_embs)
```




    74




```python
print(nb_embs.shape)
```

    (74, 384)


## Encode the Query String

If we search for a particular query string, that string needs to be encoded as an embedding using the same bi-encoder as before. Then we can compare it to the notebook embeddings.


```python
q = "Web search"
```


```python
q_emb = bienc_model.encode(q)
q_emb[:10]
```




    array([-0.0328431 , -0.00064043, -0.06456785,  0.01314389, -0.02520958,
            0.02097196,  0.03034499,  0.05960393, -0.03566388, -0.03963251],
          dtype=float32)



## Create a Cosine Similarities Tensor

Sentence Transformers provides a function to get the similarity between the query and each of the notebook embeddings. It defaults to cosine similarity. We use it to get a tensor of how similar the query embedding is to each notebook.


```python
sims = bienc_model.similarity(q_emb, nb_embs)
sims
```




    tensor([[ 0.2022,  0.1729, -0.0333, -0.0670,  0.0745,  0.0353,  0.0670,  0.0779,
              0.0709,  0.0786,  0.1814,  0.0342,  0.0047,  0.0716,  0.0518, -0.0770,
              0.1202,  0.1646,  0.0790,  0.0343,  0.0567,  0.0842,  0.0070,  0.1067,
              0.0751, -0.0592, -0.0341, -0.0082,  0.0048,  0.0697,  0.0034,  0.0660,
              0.1866,  0.0680,  0.0811,  0.0612,  0.1918,  0.2615,  0.2304,  0.1414,
              0.0626,  0.1566,  0.0056,  0.1292,  0.0197,  0.1162, -0.0663,  0.0835,
              0.0663,  0.0659,  0.0946,  0.1104,  0.0101,  0.1370,  0.0635,  0.0044,
              0.0777, -0.0330, -0.0023,  0.0593,  0.0358,  0.0823,  0.0667,  0.0458,
              0.1565,  0.1318,  0.1485,  0.1480,  0.0771,  0.0885,  0.0954,  0.0929,
              0.0607,  0.1207]])




```python
sims.shape
```




    torch.Size([1, 74])



## Get Top 10 Similar Results

Sentence Transformers also provides a semantic search utility that returns search results:


```python
hits = util.semantic_search(q_emb, nb_embs, top_k=10)
hits
```




    [[{'corpus_id': 37, 'score': 0.2615070044994354},
      {'corpus_id': 38, 'score': 0.2304057776927948},
      {'corpus_id': 0, 'score': 0.20217692852020264},
      {'corpus_id': 36, 'score': 0.1918058693408966},
      {'corpus_id': 32, 'score': 0.18661072850227356},
      {'corpus_id': 10, 'score': 0.18138977885246277},
      {'corpus_id': 1, 'score': 0.17291493713855743},
      {'corpus_id': 17, 'score': 0.16460277140140533},
      {'corpus_id': 41, 'score': 0.15658749639987946},
      {'corpus_id': 64, 'score': 0.15653304755687714}]]



Let's display the search results:


```python
L(hits[0])
```




    (#10) [{'corpus_id': 37, 'score': 0.2615070044994354},{'corpus_id': 38, 'score': 0.2304057776927948},{'corpus_id': 0, 'score': 0.20217692852020264},{'corpus_id': 36, 'score': 0.1918058693408966},{'corpus_id': 32, 'score': 0.18661072850227356},{'corpus_id': 10, 'score': 0.18138977885246277},{'corpus_id': 1, 'score': 0.17291493713855743},{'corpus_id': 17, 'score': 0.16460277140140533},{'corpus_id': 41, 'score': 0.15658749639987946},{'corpus_id': 64, 'score': 0.15653304755687714}]




```python
def print_search_result(hit): print(f"{hit['score']:.4f} {nb_paths[hit['corpus_id']]}")
```


```python
L(hits[0]).map(print_search_result)
```

    0.2615 2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb
    0.2304 2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb
    0.2022 2025-04-15-Semantic-Search-With-Sentence-Transformers-and-a-Cross-Encoder-Model.ipynb
    0.1918 2025-01-16-Cosine-Similarity-Breakdown-in-LaTeX.ipynb
    0.1866 2025-01-20-Dark-and-Light-Mode-in-FastHTML.ipynb
    0.1814 2025-02-09-An-Informationally-Dense-Index-Page.ipynb
    0.1729 2025-04-14-Semantic-Search-With-Sentence-Transformers-and-a-Bi-Encoder-Model.ipynb
    0.1646 2025-02-02-Text-Embeddings-and-Cosine-Similarity.ipynb
    0.1566 2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb
    0.1565 2024-12-23-Daddys_Snowman_Card.ipynb





    (#10) [None,None,None,None,None,None,None,None,None,None]



## Define a Function

Putting together everything we've figured out:


```python
def bienc_search_nbs(q):
    nb_paths = get_nb_paths()
    nbs = L(nb_paths).map(read_nb_simple)
    nb_embs = bienc_model.encode(nbs)
    q_emb = bienc_model.encode(q)
    hits = util.semantic_search(q_emb, nb_embs, top_k=10)
    L(hits[0]).map(print_search_result)
```

We can try out our biencoder-based semantic search function:


```python
bienc_search_nbs("search")
```

    0.2891 2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb
    0.2425 2025-04-15-Semantic-Search-With-Sentence-Transformers-and-a-Cross-Encoder-Model.ipynb
    0.2348 2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb
    0.2180 2025-04-14-Semantic-Search-With-Sentence-Transformers-and-a-Bi-Encoder-Model.ipynb
    0.1928 2024-12-23-Daddys_Snowman_Card.ipynb
    0.1794 2025-02-02-Text-Embeddings-and-Cosine-Similarity.ipynb
    0.1778 2025-02-13-Excavating-a-Lost-CLI-Tool.ipynb
    0.1713 2024-12-24-Trying-execnb.ipynb
    0.1703 2025-02-09-An-Informationally-Dense-Index-Page.ipynb
    0.1624 2025-01-12-A-Better-Notebook-Index-Page.ipynb


## Reflection

A bi-encoder is nice because it allows you to pregenerate embeddings and later use those for comparison. But I'm reading that it's not as accurate as a cross-encoder. In the next post we'll see if that's true.
