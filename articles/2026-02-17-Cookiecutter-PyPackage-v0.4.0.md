# Cookiecutter PyPackage v0.4.0: Everything a Modern Python Package Needs

I've put out the biggest release of [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) since the modern rewrite. Generated projects now ship with a documentation site, type checking, cross-version coverage enforcement, and security-hardened CI, all configured and working out of the box.

```bash
uvx cookiecutter-pypackage
```

## What's new

**Documentation site with Zensical and API autodoc.** Every generated project now includes a [Zensical](https://zensical.org/) documentation site with the Material theme, light/dark mode, and automatic API reference from your docstrings via [mkdocstrings](https://mkdocstrings.github.io/). A GitHub Actions workflow builds the docs and deploys to GitHub Pages. Preview locally with `just docs-serve`.

**Type checking with ty.** Generated packages include a [py.typed](https://peps.python.org/pep-0561/) marker, the "Typing :: Typed" classifier, and type hints on all starter code. CI runs [ty](https://docs.astral.sh/ty/) as a separate job. Locally, `just type-check` runs it once, and `just type-check-watch` re-checks on every save.

**Coverage the coverage.py way.** Branch coverage, parallel mode, cross-version combining (3.12, 3.13, 3.14), and a `fail_under` floor of 50% that you raise as your project grows. CI collects coverage from every Python version, combines the results, and posts a report to the GitHub Actions summary page.

**CLI accepts extra key=value arguments.** Override any template variable from the command line, especially useful with `--no-input`:

```bash
uvx cookiecutter-pypackage --no-input full_name="Audrey M. Roy Greenfeld" pypi_package_name=my-package
```

**Creator attribution in generated READMEs.** A bold "Created by" line at the top of the README with links to your GitHub and PyPI profiles. A new `author_website` prompt lets you link to your personal site too.

## What's better

- **Security-hardened GitHub Actions.** SHA-pinned actions, `persist-credentials: false`, minimal permissions, Dependabot for action updates. The publish workflow uses [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) with build provenance attestation.
- **Dependency groups (PEP 735)** instead of optional-dependencies for dev, test, lint, typecheck, and docs.
- **Python 3.12, 3.13, and 3.14** in CI and the `just testall` recipe.
- **Leaner template.** Removed MANIFEST.in, `.readthedocs.yaml`, empty `slug.py`, empty `tests/__init__.py`, `__author__`/`__email__` dunders, and the ReadTheDocs badge.
- **Rewritten docs** for both the template repo and the generated project. The tutorial walks through all nine steps from generation to PyPI release.

Full changelog: [v0.4.0](https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/main/CHANGELOG/v0.4.0.md)

Tags: python, cookiecutter, open-source
