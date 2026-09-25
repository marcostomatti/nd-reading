"""Bundles the core skill and every module into one file for the upstream eval harness.

The harness runs the model with tools switched off and pastes a single skill file into
the prompt, so the model cannot open the module files itself. The bundle gives it all of
them at once. It tests the rules; it does not test whether the model reads the right
module at the right time.
"""
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "nd-reading"
MODULES = [
    "execution.md",
    "ideation.md",
    "debugging.md",
    "walkthrough.md",
    "second-pass.md",
    "format-check.md",
    "save-approach.md",
]


def bundle() -> str:
    parts = [(SKILL_DIR / "SKILL.md").read_text().rstrip()]
    for name in MODULES:
        body = (SKILL_DIR / name).read_text().rstrip()
        parts.append(f"<!-- module: {name} -->\n\n{body}")
    return "\n\n---\n\n".join(parts) + "\n"


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "build" / "nd-reading-bundled.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(bundle())
    print(f"wrote {out.relative_to(out.parent.parent)} ({len(out.read_text().split())} words)")
