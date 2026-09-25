# Review: UditAkhourii/adhd, a divergent fan-out skill

Reviewed 2026-09-25 at commit `dd08acc` (main, 2026-09-17). The skill file itself last
changed in `55ed385` (2026-06-04). Files were read through the GitHub API; nothing was
downloaded, installed or run.

## What it is

The name borrows "ADHD" for divergent thinking. It is an ideation engine, and it does
not shape how replies read. When it runs, it starts five subagents in parallel, each
told to think from one "cognitive frame" (a regulator, a speedrunner, a 10-year-old,
biology, and so on). Each subagent writes six short ideas without judging them. The main
session then scores all 30 ideas, groups them into clusters, marks traps, and sends the
top three to three more subagents that develop each one. The result comes back as one
structured report.

The repository has two parts. `skills/adhd/SKILL.md` is the skill, and it is plain
instructions. The rest is an optional npm package, `adhd-agent`, which runs the same
loop from a terminal through the Claude Agent SDK.

## Security

- **The skill runs no code.** The plugin manifest declares the skill and nothing else:
  no hooks, no MCP servers, no commands, no scripts. Installing it cannot execute
  anything on this machine.
- **Its subagents stay inside the session.** The problem text and context go to
  subagents of the same model, in the same session. Nothing goes to a third party.
- **The npm engine is optional and narrow.** `src/llm.ts` calls the model with tools
  switched off, and the engine has no shell calls, file writes or network calls of its
  own. It would run with your Claude credentials and spend usage. The published npm
  version (0.1.4, 2026-05-30) is older than the repository.
- **The one security issue is in their CI.** Issue #58 reports that the bot summarising
  new issues takes the issue text into its prompt. The worst case is someone steering
  the comment the bot posts on their own issue. It does not reach anyone who installs
  the skill.
- **Updates arrive unreviewed.** A plugin installed from its marketplace follows the
  upstream repository, so a later update can change the skill's instructions with no
  review on our side. One maintainer wrote 25 of the 34 commits. The licence is MIT.

## Fit with nd-reading

- **Name clash.** The skill is named `adhd` and runs on `/adhd`, the same command the
  current `marcos-has-adhd` skill answers to.
- **Wide automatic trigger.** Its description matches brainstorming, open-ended design,
  architecture, naming, API design and hard-to-pin bugs. Its own cost note says a run
  takes about 10 agent calls, 30 to 90 seconds, and 5 to 10 times the cost of one
  answer. A self-check skips it on closed questions, but an explicit `/adhd` skips the
  check.
- **Output shape.** A run returns 30 ideas with score chips in clusters, a shortlist,
  three developed branches with 3 to 5 child ideas each, and a closing "provocation"
  that opens a new direction. By core rules 2 and 3 that is a wall of structure with a
  footer that changes the subject.
- **Converges in the same reply.** Its anti-patterns call a reply without a firm pick "a
  cop-out", so every run ends with a recommendation. `ideation.md` holds convergence back
  until the reader's burst is over.

## How it plays

It plays closer to handing over the controls and watching. You serve the problem, ten
agents play the whole match in isolation, and a scoreboard comes back. You have no turn
while it runs. It can still become part of a rally if `ideation.md` uses it as a serve:
run it once on the reader's idea, then present its clusters one at a time and play from
there together.

## What bringing it in would take

| Route | What it takes | What it costs |
|---|---|---|
| Plugin from its marketplace | `/plugin marketplace add UditAkhourii/adhd`, then `/plugin install adhd@adhd` | The `/adhd` clash, the wide automatic trigger, and unreviewed updates |
| Vendored copy, pinned | Copy `skills/adhd/SKILL.md` at `55ed385` into `vendor/adhd-fanout/` with its MIT notice, rename it `adhd-fanout`, add `disable-model-invocation: true`, and install the folder in `~/.claude/skills/` | Manual updates. It runs only when called by name |
| Adapted | After a trial: `ideation.md` calls it as a serve, and its output shape follows core rules 2 and 3 | A fork to maintain |

The vendored copy suits a trial: the skill text stays as its authors wrote it, so the
trial tests the original feel, and it cannot fire on its own or change underneath you.
The npm package is not needed for any route.
