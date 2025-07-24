import air
from typing import Iterable, Generator
from listo import listo as L
from pathlib import Path
from datetime import datetime

app = air.Air()


def get_nb_paths():
    root = Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)


def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[0:10])
    except ValueError:
        return datetime.now()


def notebook_card(notebook_path):
    date = get_date_from_iso8601_prefix(notebook_path.name) or datetime.now()
    return air.A(air.Article(
            air.Header(
                air.H3(notebook_path),
                "Description goes here",
            )
        ),
        href=f"{notebook_path}")


@app.page
def index():
    nb_paths = get_nb_paths()
    return air.layouts.picocss(
        air.Title("audrey.feldroy.com"),
        air.H1("audrey.feldroy.com"),
        air.P(
            "The experimental notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ",
            air.A(
                "github.com/audreyfeldroy/audrey.feldroy.com",
                href="https://github.com/audreyfeldroy/audrey.feldroy.com",
            ),
        ),
        air.Div(
            *nb_paths.map(notebook_card),
            # *get_nb_paths().map(notebook_card),
            # class_="grid",
        ),
    )
