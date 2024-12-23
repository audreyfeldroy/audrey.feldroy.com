from pathlib import Path
from fasthtml.common import *
from nb2fasthtml.core import (
    render_nb, read_nb, get_frontmatter_raw,render_md,
    strip_list
)

app,rt = fast_app()

@rt
def index():
    nbs = L(Path('nbs').glob('*.ipynb'))
    return Div(
        H1('My nb2fasthtml-powered blog'), 
        Ul(*[Li(A(nb.stem, href=f'/nb/{nb.stem}')) for nb in nbs]),
        style="padding: 1em"
    )

serve()
