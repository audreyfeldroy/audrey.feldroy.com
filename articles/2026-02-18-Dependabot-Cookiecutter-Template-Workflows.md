# How to Make Dependabot Update Actions Inside a Cookiecutter Template

If you maintain a Cookiecutter template that generates GitHub Actions workflows, you have a quiet problem: Dependabot keeps your outer repo's action SHAs current, but it completely ignores the template's workflows. The generated projects ship with whatever versions you happened to pin last.

The fix is to make each workflow conf valid YAML both before and after templating. Weird but it works. I think at least. We'll see what actually happens with the next Dependabot updates.

## The problem

Cookiecutter templates that generate GitHub Actions workflows typically wrap them in Jinja `{% raw %}` blocks to prevent Cookiecutter from mangling the `${{ }}` expressions during baking:

```yaml
{% raw -%}
name: CI
on:
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
...
{%- endraw %}
```

This works great for baking. But Dependabot's GitHub Actions updater runs `YAML.safe_load` on every workflow file it finds ([`file_parser.rb` line 68](https://github.com/dependabot/dependabot-core/blob/main/github_actions/lib/dependabot/github_actions/file_parser.rb)). `{% raw %}` on line 1 isn't valid YAML, so the file gets silently skipped as unparseable.

## The fix

Replace the whole-file `{% raw %}` wrapper with per-expression Jinja escaping. Instead of:

```yaml
group: ${{ github.workflow }}
```

Write:

```yaml
group: ${{ "{{" }} github.workflow {{ "}}" }}
```

Jinja2 sees `{{ "{{" }}` and outputs a literal `{{`. The baked result is identical: `${{ github.workflow }}`. But now the file is valid YAML that Dependabot can parse.

Then point Dependabot at both directories using `directories` (plural):

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directories:
      - "/"
      - "/{{cookiecutter.pypi_package_name}}/.github/workflows"
    schedule:
      interval: weekly
```

For non-root directories, Dependabot's [file fetcher](https://github.com/dependabot/dependabot-core/blob/main/github_actions/lib/dependabot/github_actions/file_fetcher.rb) looks for `*.yml` directly in the specified path (it only prepends `.github/workflows/` for the root directory). So you need the full path to the workflows subdirectory.

## Why it works

Two things make this safe:

1. **YAML doesn't care.** The `{{ "{{" }}` syntax is just string content to a YAML parser. Values starting with `$` are plain scalars, so the braces inside them aren't interpreted as flow mappings.

2. **Dependabot does string replacement, not YAML round-tripping.** The [file updater](https://github.com/dependabot/dependabot-core/blob/main/github_actions/lib/dependabot/github_actions/file_updater.rb) uses `gsub` to swap old SHAs for new ones in the raw file content. Your Jinja escaping survives untouched.

## What about `publish.yml`?

If your publish workflow uses `{{ cookiecutter.package_name }}` (without `{% raw %}`), it probably already parses as valid YAML. The `{{ }}` inside a quoted YAML string is just string content. Check with:

```python
import yaml
yaml.safe_load(open("path/to/publish.yml").read())
```

If it parses, Dependabot can already update it. No changes needed.

## The result

Dependabot now opens PRs for both sets of workflows. When it bumps `actions/checkout` in your outer CI, it also bumps the version your users get when they generate a new project. No more drift between what you run and what you ship.
