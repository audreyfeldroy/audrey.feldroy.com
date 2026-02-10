# Adopting Idiomatic PyTest: A Code Review

We recently reviewed a pull request from contributor [Martin Saizar](https://msaizar.com/) that refactored our Python tests. The goal was to enable the PyTest (`PT`) linter rule in Ruff, our code formatter and linter. 

This task, part of a larger code quality initiative by Air core contributor pygarap to fully use the power of Ruff rules, led to several interesting improvements in our test suite's style and clarity.

![GitHub Pull Request for PyTest style refactoring](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/01-pr-overview.jpg)

The `PT` ruleset enforces idiomatic PyTest conventions. Before this change, the rule was commented out in our configuration because our codebase had numerous violations. The PR fixed all of them so we could finally enable it.

![The PT ruleset configuration in pyproject.toml](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/02-pt-ruleset-config.jpg)

Let's look at a few of the specific refactorings and why they make our tests better.

### Cleaner Fixtures and Imports

Many of the changes involved removing redundant code and clarifying imports. For example, PyTest fixtures default to `scope="function"`, so explicitly declaring it is unnecessary.

![Code diff showing the removal of a redundant scope argument](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/03-fixture-scope-removal.jpg)

The refactor also changed how we import PyTest components. Instead of importing a class directly (`from pytest import CaptureFixture`), we now import the parent module (`import pytest`) and use the full name (`pytest.CaptureFixture`). This makes it immediately clear where `CaptureFixture` comes from without needing to find the import statement at the top of the file.

![Code diff showing the change from direct import to module import](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/04-module-import-change.jpg)

### Improving Assertions for Better Debugging

The most significant improvement came from splitting chained `assert` statements. Previously, we had tests that checked multiple conditions in a single line.

```python
# Before
assert "expected_string_1" in output and "expected_string_2" in output
```

If this test failed, the error message would not specify which string was missing. The refactor split this into two separate assertions.

![Code diff showing chained assertions split into separate statements](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/05-split-assertions.jpg)

```python
# After
assert "expected_string_1" in output
assert "expected_string_2" in output
```

Now, if a test fails, PyTest will point to the exact line and condition that failed. This saves significant debugging time. It’s a small change that makes a big difference when tracking down failures.

### Activating the Rule and Merging

With all violations fixed, the final change was to enable the `PT` rule in our `pyproject.toml` file. This acts as a safeguard, ensuring all future code automatically adheres to these conventions.

![Final code change uncommenting the PT rule in the configuration file](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/06-enable-pt-rule.jpg)

After a quick review, we approved and merged the PR.

![PR approved and merged on GitHub](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/07-pr-merged.jpg)

The post-merge checks confirmed that all tests passed, and they continue to run incredibly fast.

![Tests passing in the CI/CD pipeline](https://audreyfeldroy.github.io/arg-static/img/2025-12-16-pytest-review/08-tests-passing.jpg)

### Conclusion

This refactor highlights several principles for writing clean, maintainable tests:

- **Enforce Style with a Linter:** Using tools like Ruff to automatically enforce conventions keeps the codebase consistent.
- **One Assert Per Condition:** Write separate `assert` statements for each condition to get more precise failure reports.
- **Prefer Module Imports:** `import pytest` is often clearer than `from pytest import ...` because it preserves the namespace.
- **Remove Redundancy:** Eliminate default arguments and other boilerplate to keep code focused on what it does.

Thanks to Martin Saizar's contribution, our test suite is not only cleaner but also easier to debug.