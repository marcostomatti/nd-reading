# nd-reading

A skill and a rule for agents that write for neurodivergent readers: people with ADHD, a
developmental language disorder, or English as a second language.

Status: proposal, 2026-09-25. Nothing in this repository is installed anywhere yet.

## What is here

- `skills/nd-reading/` is the skill. `SKILL.md` is the core, which stays on for the whole
  session. The other files are modules, one per scenario, and the model reads a module
  only when its trigger fires.
- `rules/no-blame-reporting.md` is a rule that keeps blame out of every reply and report.
  The skill's core rule 6 carries a short version of it, for places where the rule file
  is not installed.
- `evals/` holds seventeen evaluation cases, a rubric addendum, and the results of the
  first smoke test.
- `docs/external/adhd-fanout-review.md` reviews an ideation skill considered for a trial
  inside the ideation module.

## How the skill is built

The core holds what is true in every scenario: small bites, the shape of a reply, one
ending, open threads, analogies, blame-free error reports, and a pre-send check. It also
holds the trigger table and the reading of a sharp change of subject.

| Module | Read when |
|---|---|
| `execution.md` | The reader asks to build, fix, change or run something |
| `ideation.md` | The reader brings a high-level idea or jumps ahead |
| `debugging.md` | The reader is stuck on errors, dependencies or versions |
| `walkthrough.md` | The reader asks for an explanation |
| `second-pass.md` | A reply did not land |
| `format-check.md` | Two shapes fit the same content, or the case is unclear |
| `save-approach.md` | A format worked and may become the default |

Triggers can overlap. Where two modules would shape the same content differently, the
model uses a saved preference or asks one format question.

Size, in words: the core is 2,500, and the modules run from 160 to 600 each. The
single-file draft that was tested on 2026-09-25 was 2,925, and the upstream
`i-have-adhd` skill it started from is 1,175.

## Installing the skill

For Claude Code on one machine, copy the folder:

```bash
cp -R skills/nd-reading ~/.claude/skills/
```

Then start a session and ask for the skill by name. Only one reading skill should be
active at a time, because older versions delete analogies and this one keeps them. Turn
off `marcos-has-adhd` in claude.ai while this one is in use.

For claude.ai, upload the `skills/nd-reading/` folder as a skill; the modules travel with
it.

## Installing the no-blame rule

Claude Code loads every markdown file under `~/.claude/rules/`, including files in
subfolders, into every session on this machine. From this folder:

```bash
mkdir -p ~/.claude/rules/nd-reading
```

```bash
cp rules/no-blame-reporting.md ~/.claude/rules/nd-reading/
```

To check it loaded, start a new session and ask "which rules file talks about blame?".
The answer should name `no-blame-reporting.md`. The rule reaches Claude Code on this
machine only. Other places get the short version inside the skill.

## Running the evaluations

`evals/build_cases.py` writes `evals/cases.jsonl`, so edit the script and run it again
rather than editing the JSONL by hand. The cases use the format of the harness in the
upstream `i-have-adhd` repository.

That harness runs the model with tools switched off and pastes one skill file into the
prompt, so the model cannot open the modules. `evals/bundle_skill.py` joins the core and
all modules into `evals/build/nd-reading-bundled.md` for it. A harness run therefore
tests the rules. Whether the model reads the right module at the right time needs a run
with tools on, like the 2026-09-25 smoke test, which used Claude Code subagents.

The harness spends API money and asks for a budget per run:

```bash
python3 evals/bundle_skill.py
cd ~/projects/claude-code-stuff/i-have-adhd
CASES=~/projects/nd-reading/evals/cases.jsonl
OUT=~/projects/nd-reading/evals/results/harness.jsonl
python3 scripts/run_evals.py run --runner claude --condition baseline --cases "$CASES" --trials 3 --budget-usd 5 --output "$OUT"
python3 scripts/run_evals.py run --runner claude --condition comparator --condition-skill skills/i-have-adhd/SKILL.md --cases "$CASES" --trials 3 --budget-usd 5 --output "$OUT"
python3 scripts/run_evals.py run --runner claude --condition candidate --condition-skill ~/projects/nd-reading/evals/build/nd-reading-bundled.md --cases "$CASES" --trials 3 --budget-usd 5 --output "$OUT"
```

The budget figures are placeholders. Run the upstream 14 cases too, with the same three
conditions, to check that nothing from the original skill got worse. Scoring is by hand,
with the condition names hidden from the judge; `evals/rubric-addendum.md` adds the
followability and blame-free dimensions.

The smoke test in `evals/results/` measured the single-file draft, saved there as
`tested-skill-2026-09-25.md`. The modules, and the five cases added for them
(`one-ending`, `context-switch`, `ideation`, `stuck`, `save-approach`), have not been run
yet.

## Before publishing

- **Licence.** The skill text started from `i-have-adhd`, MIT, copyright 2026 Ayoub
  Ghriss, so its notice has to ship with this repository. This repository still needs a
  licence of its own.
- **Name.** `nd-reading` is a working name.
- **Credits.** The narrative rules (small bites, the shape of a reply, analogies, closing
  threads) come from the writing desk of Open Tomato, where the paco agent first used
  them for articles.
