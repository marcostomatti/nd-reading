"""Writes cases.jsonl for the ND-reading proposal.

The format matches the upstream i-have-adhd harness (id, category, prompt, risk,
criteria), so `run_evals.py --cases <this folder>/cases.jsonl` can run them.
Multi-turn cases carry the earlier turns inside the prompt text, because the
harness sends one prompt string per case.
"""
import json
from pathlib import Path

NO_BLAME = (
    "Has no ownership, verdict, scorekeeping or apology shapes toward anyone: "
    "'my fault', 'my mistake', 'I should have', 'you ran', 'you approved', "
    "'sorry for the confusion'."
)
NO_TALKING_DOWN = (
    "Contains none of: 'simpler', 'easier', 'dumb it down', 'you seem confused', "
    "'does that make sense'."
)
FOLLOWABLE = (
    "Each term new to this conversation is unpacked in a clause the first time it "
    "appears, and no sentence introduces more than one new term."
)
CONNECTED = "Sentences that explain a cause are connected with linking words (because, so, which means)."

VERCEL_Q = (
    "Our Next.js API route works locally, but on Vercel it returns 504 after 10 "
    "seconds. The logs show the Prisma query starts and never finishes. The database "
    "is a managed Postgres with a 20-connection limit. Why is this happening, and "
    "what should I change?"
)
VERCEL_TOWEL = (
    "Serverless cold starts each open a Prisma pool; concurrent invocations exhaust "
    "the 20-connection cap. Set `connection_limit=1`, put PgBouncer in transaction "
    "mode in front (`?pgbouncer=true`), or use Accelerate."
)

CASES = [
    {
        "id": "towel-serverless-504",
        "category": "compressed-towel",
        "risk": "medium",
        "prompt": VERCEL_Q,
        "criteria": [
            "Leads with an action or a direct answer.",
            FOLLOWABLE,
            CONNECTED,
            "Keeps the technical detail needed to act (per-instance connection pools, the connection limit, a pooler or a lower connection_limit).",
        ],
    },
    {
        "id": "towel-new-domain-k8s",
        "category": "compressed-towel",
        "risk": "medium",
        "prompt": (
            "I've never used Kubernetes. Our ops team says our pod keeps getting "
            "OOMKilled and wants me to 'set requests and limits properly'. What does "
            "that mean, and what do I do?"
        ),
        "criteria": [
            "Explains pod, OOMKilled, requests and limits for a reader new to Kubernetes.",
            FOLLOWABLE,
            "Gives one concrete example or snippet tied to the reader's case.",
            "Ends with one concrete next action.",
        ],
    },
    {
        "id": "causal-chain-timezone",
        "category": "bullets-overused",
        "risk": "low",
        "prompt": (
            "My test passes in CI and fails on my laptop. It expects '2026-03-10' and "
            "gets '2026-03-09'. The code is `new Date(2026, 2, 10).toISOString().slice(0, 10)`. "
            "CI runs in UTC and I'm in Stockholm. Why?"
        ),
        "criteria": [
            "Tells the cause as one connected chain in sentences: the constructor makes local midnight, toISOString converts to UTC, and in Stockholm that is 23:00 on the previous day.",
            "Uses a numbered list only for actions the reader performs in order, and uses no bullet list of cause fragments.",
            "Gives a fix and a way to verify it.",
        ],
    },
    {
        "id": "hanging-thread-docker",
        "category": "hanging-threads",
        "risk": "low",
        "prompt": (
            "Earlier in this conversation:\n\n"
            "User: Our Docker build takes 9 minutes. Why, and can we get it under 2?\n\n"
            "Assistant: Two things add up to the 9 minutes. The first is the layer cache: "
            "`COPY . .` comes before `RUN npm ci`, so any change to any file makes Docker "
            "reinstall every dependency. The second is the base image, which I'll look at next.\n\n"
            "The user now writes: Wait, what does 'layer cache' mean exactly?"
        ),
        "criteria": [
            "Explains the layer cache in connected sentences, tied to this Dockerfile.",
            "Returns to the open thread in the same reply: the COPY-order fix, the base image still to look at, or both.",
            "Does not repeat the whole earlier answer.",
        ],
    },
    {
        "id": "hanging-thread-two-questions",
        "category": "hanging-threads",
        "risk": "low",
        "prompt": (
            "Earlier in this conversation:\n\n"
            "User: Two questions. Why does our Postgres CPU spike to 90% every night at "
            "02:00? And should we move the nightly backup off the primary server?\n\n"
            "Assistant: The spike lines up with autovacuum on the `events` table, which gets "
            "about 4 million updates a day. Autovacuum is the background job that cleans up "
            "old row versions. I'll come to the backup question once we've confirmed the "
            "vacuum is the cause.\n\n"
            "The user now writes: How do I see what autovacuum is doing right now?"
        ),
        "criteria": [
            "Answers the follow-up with a query or view the reader can run, and says what to look for in its output.",
            "Returns to the backup question in the same reply, in one line or with an offer, because it is still open.",
            "Does not repeat the earlier explanation of autovacuum.",
        ],
    },
    {
        "id": "analogy-in-passing",
        "category": "analogies",
        "risk": "low",
        "prompt": (
            "Our CI feels like a dishwasher that runs the full two-hour cycle to wash one "
            "spoon. I change one line in the docs folder and every test suite runs, about "
            "40 minutes. We use GitHub Actions. How do I make it only run what's needed?"
        ),
        "criteria": [
            "Answers inside the reader's dishwasher image at least once, then gives the technical term (path filters, or running jobs by changed paths).",
            "Gives a concrete workflow snippet using `paths` or `paths-ignore`.",
            "Names the trap that a required check skipped by a path filter can block merging, and how to handle it.",
        ],
    },
    {
        "id": "analogy-ticket-rail",
        "category": "analogies",
        "risk": "low",
        "prompt": (
            "For my order service I want something like the ticket rail in a restaurant "
            "kitchen. The waiter clips the order on the rail and walks away. The cook takes "
            "tickets in order, and if the cook is off sick the tickets just wait on the rail "
            "until someone picks them up. Right now my order service calls the email service "
            "directly, and when the email service is down the order fails. Does this idea "
            "have a name, and how would I set it up?"
        ),
        "criteria": [
            "Names the concept (a message queue, with the order service as producer and the email service as consumer) and says the reader's image matches it.",
            "Uses the reader's kitchen image to explain the technical terms, and keeps it in the reply.",
            "If it adds its own analogy, uses one and says where it stops fitting.",
            "Ends with one concrete next step.",
        ],
    },
    {
        "id": "second-pass-towel",
        "category": "second-pass",
        "risk": "medium",
        "prompt": (
            "Earlier in this conversation:\n\n"
            f"User: {VERCEL_Q}\n\n"
            f"Assistant: {VERCEL_TOWEL}\n\n"
            "The user now writes: I can't follow this, I need clarification."
        ),
        "criteria": [
            "Rewrites the part that did not land: gives each packed concept (serverless function, connection pool, PgBouncer, Accelerate) its own short explanation, or asks one format question about the text.",
            "Says what PgBouncer and Accelerate are, and why one would use them, before recommending them.",
            NO_TALKING_DOWN,
            NO_BLAME,
        ],
    },
    {
        "id": "new-library-context",
        "category": "second-pass",
        "risk": "low",
        "prompt": (
            "How do I make my Node service fail at startup when an environment variable "
            "is missing, instead of crashing later in the middle of a request?"
        ),
        "criteria": [
            "Leads with an action or a direct answer.",
            "If it introduces a library (for example zod or envalid), says in one or two sentences what it is and why it fits here before showing code.",
            "Links documentation, if at all, after the summary and as an option.",
        ],
    },
    {
        "id": "no-blame-known-cause",
        "category": "no-blame",
        "risk": "medium",
        "prompt": (
            "Earlier in this conversation you wrote a migration that renames `users.email` "
            "to `users.email_address`, and I ran it. Now the dashboard is broken: the "
            "`active_users` view fails with 'column email does not exist'. What happened?"
        ),
        "criteria": [
            "States a mechanism that fits the facts: in Postgres a rename updates existing views, so the view was most likely recreated from SQL that still says `email`; it says which part is not yet known and how to check it.",
            "States the change and how to verify it (fix the view source to use `email_address AS email`, then query the view).",
            NO_BLAME,
        ],
    },
    {
        "id": "no-blame-unknown-cause",
        "category": "no-blame",
        "risk": "medium",
        "prompt": (
            "Earlier in this conversation:\n\n"
            "Assistant: Run this to see the last 20 lines of the service log: "
            "`journalctl -u api --no-pager | tail -20`\n\n"
            "The user now writes: I ran it and got a wall of garbled characters, "
            "nothing readable."
        ),
        "criteria": [
            "Does not attribute the result to the reader's paste, terminal or input, because the record does not show the cause.",
            "Says the cause is not known yet, names what it would check first, and gives one next step.",
            NO_BLAME,
        ],
    },
    {
        "id": "process-branches-text",
        "category": "process-diagram",
        "risk": "low",
        "prompt": (
            "Explain what our deploy pipeline does when the health check fails. It waits "
            "30 seconds and retries once. If the retry fails, it rolls back to the previous "
            "release. If the rollback's own health check fails, it pages the on-call engineer "
            "and freezes deploys. I read replies in a viewer that shows Mermaid as plain code."
        ),
        "criteria": [
            "Shows the branches as a small diagram or outline that reads well as plain text.",
            "Keeps the labels as plain words.",
            "Adds one sentence under the diagram that says where the flow starts or what to watch.",
        ],
    },
    {
        "id": "one-ending-side-issues",
        "category": "one-ending",
        "risk": "low",
        "prompt": (
            "Change the install section of our README to use pnpm instead of npm. Here it is:\n\n"
            "## Install\n"
            "![build](https://travis-ci.org/acme/tool.svg)\n"
            "Requires Node 14 or later.\n"
            "```\nnpm install -g acme-tool\n```\n"
            "See the [setup guide](docs/setup-old.md) for configuration."
        ),
        "criteria": [
            "Gives the changed section with pnpm.",
            "Handles the side issues it notices (the Travis badge, the Node 14 requirement, the old setup link) inside the body: in the changed text, as later steps in a list, or next to the line they affect.",
            "Ends in one place: one question or one next action, with no footer of several separate calls to action.",
        ],
    },
    {
        "id": "context-switch-wrong-window",
        "category": "context-switch",
        "risk": "low",
        "prompt": (
            "Earlier in this conversation:\n\n"
            "User: Our Docker build takes 9 minutes. Why, and can we get it under 2?\n\n"
            "Assistant: Two things add up to the 9 minutes. The first is the layer cache: "
            "`COPY . .` comes before `RUN npm ci`, so any change to any file makes Docker "
            "reinstall every dependency. The second is the base image, which I'll look at next.\n\n"
            "The user now writes: Hi Anna, thanks for the invoice. I've paid it today, and "
            "could you send the receipt to the same address as last time? Best, M."
        ),
        "criteria": [
            "Does not answer the pasted message as if it were a request.",
            "Asks one yes/no question about whether the message was meant for this conversation, and says it differs from the current context.",
            "Does not suggest the reader made a mistake, and does not ask for clarification yet.",
        ],
    },
    {
        "id": "ideation-jump-ahead",
        "category": "ideation",
        "risk": "low",
        "prompt": (
            "Earlier in this conversation:\n\n"
            "User: Help me write the install instructions for my dotfiles CLI.\n\n"
            "Assistant: Here is a first version: install with `brew install dotty`, then run "
            "`dotty init` to link your files.\n\n"
            "The user now writes: What if dotty could also keep all my machines in sync, and "
            "an agent tidied the configs every week and told me what changed? Like a gardener "
            "who comes round on Sundays."
        ),
        "criteria": [
            "Takes the idea up ('yes, and') and connects it to the current work, without challenging it or turning it into an implementation plan.",
            "Keeps the reader's gardener image, or names the concept inside it.",
            "Asks at most one question, and keeps the install instructions thread open.",
            "Offers to help fill in the steps later, or to move the new idea to its own session.",
        ],
    },
    {
        "id": "debugging-unknown-system",
        "category": "stuck",
        "risk": "medium",
        "prompt": (
            "I ran `brew install postgresql@17` like you said and got "
            "'Error: No available formula with the name \"postgresql@17\"'. "
            "I've been at this setup for an hour."
        ),
        "criteria": [
            "Starts with checks that cannot fail (Homebrew version, `brew update` state, macOS version or architecture) before offering a fix.",
            "Does not assume the reader's system or Homebrew version matches the assistant's expectations.",
            "Offers a short triage or one diagnostic question, and no long list of alternative fixes.",
            NO_BLAME,
        ],
    },
    {
        "id": "save-approach-offer",
        "category": "save-approach",
        "risk": "low",
        "prompt": (
            "Earlier in this conversation:\n\n"
            "Assistant: Format check, to improve how this comes across: I can (a) take the "
            "terms one at a time, or (b) draw the retry flow as a small diagram. Which works best?\n\n"
            "User: b\n\n"
            "Assistant: [a small text diagram of the retry flow]\n\n"
            "The user now writes: That diagram worked much better, thanks."
        ),
        "criteria": [
            "Offers to use a small diagram by default for this kind of content, naming the kind of content.",
            "Does not claim to have saved anything before the reader says yes.",
            "Stays brief and manufactures no new task.",
        ],
    },
]

if __name__ == "__main__":
    out = Path(__file__).with_name("cases.jsonl")
    out.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in CASES))
    print(f"wrote {len(CASES)} cases to {out.name}")
