from pathlib import Path
from fasthtml.common import *
from nb2fasthtml.core import *

hdrs = (
    MarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css',]),
)

app,rt = fast_app(hdrs=hdrs, pico=False)

@rt
def index():
    nb_dir = Path('nbs')
    nbs = L(nb_dir.glob('*.ipynb'))
    nbs = sorted(nbs)
    return Div(
        H1('audrey.feldroy.com'), 
        P("The notebooks of Audrey M. Roy Greenfeld"),
        Ul(*[Li(A(nb.stem, href=f'/experiments/{nb.stem}')) for nb in nbs]),
        style="padding: 1em"
    )

@rt('/experiments/{name}')
def experiment(name: str):
    nb = Path(f'nbs/{name}.ipynb')
    return Div(
        render_nb(nb, wrapper=Div),
        style="padding: 1em"
    )


serve()
