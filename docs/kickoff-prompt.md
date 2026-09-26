# Kickoff prompt

Paste the block below into a new Claude Code session opened in `~/projects/nd-reading`.

```
We're continuing work on nd-reading, a skill and a rule for agents that write for
neurodivergent readers. I'm the reader it was built around: I have ADHD and a
developmental language disorder, and English is my second language. Read README.md
first, then docs/handoff-2026-09-25.md.

For every reply in this session, follow skills/nd-reading/SKILL.md, read its modules when
their triggers fire, and follow rules/no-blame-reporting.md. The skill is still a draft.
When following it feels wrong, or a reply costs me effort anyway, say so in one line,
because that is test evidence.

Don't install or publish anything outside this repo without asking me first. That covers
~/.claude, claude.ai, plugins and pushes to GitHub. The upstream eval harness spends API money, so
ask for a budget before running it. Subagent tests spend usage, so say how many agents
before starting. Commit only when I ask.

Start with the decision that was open when the last session ended: the trial of the
external ideation skill, item 1 under "Decisions for Marcos" in the handoff. After that
we take the pending items one at a time.
```
