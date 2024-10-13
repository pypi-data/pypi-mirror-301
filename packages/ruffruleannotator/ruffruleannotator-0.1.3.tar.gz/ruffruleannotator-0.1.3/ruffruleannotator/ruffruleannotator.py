import re
import subprocess

from .rulesets import RULE_SETS, SPECIAL_RULE_SETS

# Constants
LINT_PREFIXES = ["[lint]", "[tool.ruff.lint]"]
RELEVANT_SECTIONS = ["select", "ignore", "fixable", "unfixable"]
RUFF_RULE_COMMAND = "ruff rule {rule_id}"
INDENTATION = "    "

# Regex patterns
RGX_REL_SEC_NAME = "(?:" + "|".join(RELEVANT_SECTIONS) + ")"
RGX_REL_SEC_START = rf"({RGX_REL_SEC_NAME})\s*=\s*\[(.*)"
RGX_RULE_ID = r"[A-Z]+\d*"
RGX_RULE = rf"(?:'({RGX_RULE_ID})'|\"({RGX_RULE_ID})\")"
RGX_RULES = rf"(?:{RGX_RULE},)*({RGX_RULE},?)?"


def is_commented(line):
    return "#" in line


def is_relavant_section_end(line):
    return "]" in line.split("#")[0]


def get_rule_description(id):
    if id in RULE_SETS:
        return f"{RULE_SETS[id]}"

    if id in SPECIAL_RULE_SETS:
        return SPECIAL_RULE_SETS[id]

    output = subprocess.run(
        RUFF_RULE_COMMAND.format(rule_id=id),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    letters, digits = re.match(r"([A-Z]+)([0-9]*)", id).group(1, 2)
    assert letters in RULE_SETS
    rule_set = RULE_SETS[letters]

    if output.returncode != 0 and output.stderr.startswith("error: invalid value"):
        return f"Subset of {rule_set}"

    description = output.stdout.splitlines()[0]

    if description.startswith("# "):
        description = description[2:]
    if description.endswith(f" ({id})"):
        description = description[: -len(id) - 3]

    return f"{description} ({rule_set})"


def annotate(config: list[str], sort_lines: bool = True) -> list[str]:
    try:
        import ruff  # noqa: F401
    except ModuleNotFoundError:
        print("Ruff not found. Install ruff first.")
        exit(1)

    formatted_lines = []
    lines_to_sort = []
    lint_section = False
    relevant_section = False

    for line_nr, line in enumerate(config):
        if not lint_section:
            if any(line.startswith(prefix) for prefix in LINT_PREFIXES):
                lint_section = True
            formatted_lines.append(line)
            continue

        if line.startswith("["):
            assert not relevant_section
            lint_section = False
            formatted_lines.append(line)
            continue

        if not relevant_section and (m := re.match(RGX_REL_SEC_START, line)):
            relevant_section = True
            formatted_lines.append(rf"{m.group(1)} = [")
            line = m.group(2)

        if relevant_section:
            if is_relavant_section_end(line):
                rules_section, rest = line.split("]")
            elif line.strip().startswith("#"):
                if sort_lines:
                    lines_to_sort = sorted(lines_to_sort)
                formatted_lines.extend(lines_to_sort)
                lines_to_sort = []
                formatted_lines.append(f"{INDENTATION}{line.strip()}")
                continue
            elif is_commented(line):
                lines_to_sort.append(line)
                continue
            else:
                rules_section = line

            rules_section = re.sub(r"\s+", "", rules_section)

            assert re.match(RGX_RULES, rules_section)

            rule_ids = [
                single_quoted or double_quoted
                for single_quoted, double_quoted in re.findall(RGX_RULE, rules_section)
            ]

            for id in rule_ids:
                rule_description = get_rule_description(id)
                rule_id_str = f'{INDENTATION}"{id}",'.ljust(16)
                lines_to_sort.append(f"{rule_id_str} # {rule_description}")

            if is_relavant_section_end(line):
                if formatted_lines[-1].endswith("[") and len(lines_to_sort) == 0:
                    # Empty section
                    formatted_lines[-1] = formatted_lines[-1] + f"]{rest}"
                else:
                    if sort_lines:
                        lines_to_sort = sorted(lines_to_sort)
                    formatted_lines.extend(lines_to_sort)
                    lines_to_sort = []
                    formatted_lines.append(f"]{rest}")
                relevant_section = False
        else:
            formatted_lines.append(line)

    assert not relevant_section
    return formatted_lines
