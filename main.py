from pathlib import Path
from fasthtml.common import *
from nb2fasthtml.core import *

app,rt = fast_app()

@rt
def index():
    nbs = L(Path('nbs').glob('*.ipynb'))
    nbs = sorted(nbs)
    return Div(
        H1('My nb2fasthtml-powered blog'), 
        Ul(*[Li(A(nb.stem, href=f'/experiments/{nb.stem}')) for nb in nbs]),
        style="padding: 1em"
    )

@rt('/experiments/{name}')
def experiment(name: str):
    nb = Path(f'nbs/{name}.ipynb')
    return Div(
        render_nb(nb),
        style="padding: 1em"
    )


serve()
