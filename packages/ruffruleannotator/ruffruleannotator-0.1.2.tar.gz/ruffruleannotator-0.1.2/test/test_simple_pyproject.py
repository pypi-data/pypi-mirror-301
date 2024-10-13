from ruffruleannotator import annotate

RUFF_SIMPLE_CONFIG_PYPROJECT = """
[project]
name = "packagename"

[tool.ruff.lint]
select = ["D100", "D103", "ERA001", "PLR2004", "F"]

ignore = ["E501", "B"]

[tool.ruff.format]
quote-style = "single"
"""

RUFF_SIMPLE_CONFIG_PYPROJECT_EXPECTED = """
[project]
name = "packagename"

[tool.ruff.lint]
select = [
    "D100",      # undocumented-public-module (pydocstyle)
    "D103",      # undocumented-public-function (pydocstyle)
    "ERA001",    # commented-out-code (eradicate)
    "F",         # Pyflakes
    "PLR2004",   # magic-value-comparison (Pylint [Refactor])
]

ignore = [
    "B",         # flake8-bugbear
    "E501",      # line-too-long (pycodestyle errors)
]

[tool.ruff.format]
quote-style = "single"
"""


def test_ruff_default_pyproject():
    config = RUFF_SIMPLE_CONFIG_PYPROJECT.strip().splitlines()
    result = annotate(config)
    expected_result = RUFF_SIMPLE_CONFIG_PYPROJECT_EXPECTED.strip().splitlines()

    assert len(result) == len(expected_result)
    assert all(result[i] == expected_result[i] for i in range(len(result)))
