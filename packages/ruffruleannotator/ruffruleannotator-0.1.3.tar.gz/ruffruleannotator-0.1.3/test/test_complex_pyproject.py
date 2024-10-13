from ruffruleannotator import annotate

CONFIG = """
[tool.ruff.lint]
select = ["F404",
    "F403",
    # Comment lines break the sorting. Rule IDs are sorted
    # seperately above and below the comment line.
    "F406", # already commented lines are not annotated
    "F402",
    # Lines with multiple rule ids are split
    "E112", "E111",
    "E113"]
"""

EXPECTED_OUTPUT = """
[tool.ruff.lint]
select = [
    "F403",      # undefined-local-with-import-star (Pyflakes)
    "F404",      # late-future-import (Pyflakes)
    # Comment lines break the sorting. Rule IDs are sorted
    # seperately above and below the comment line.
    "F402",      # import-shadowed-by-loop-var (Pyflakes)
    "F406", # already commented lines are not annotated
    # Lines with multiple rule ids are split
    "E111",      # indentation-with-invalid-multiple (pycodestyle errors)
    "E112",      # no-indented-block (pycodestyle errors)
    "E113",      # unexpected-indentation (pycodestyle errors)
]
"""


def test_complex_pyproject():
    result = annotate(CONFIG.strip().splitlines())

    assert result == EXPECTED_OUTPUT.strip().splitlines()
