---
name: grilling
description: Run a structured interview to stress-test a plan, decision, or idea. Use when the user asks to grill an idea or uses a related trigger phrase.
---

Interview the user until the in-scope decisions are understood or the user asks to stop. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), use available tools or dispatch a sub-agent when delegation is available; don't ask the user for anything you could look up yourself. If exploration is delegated, ask only the independent frontier questions while it runs. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty, the user asks to stop, or the user confirms that the remaining branches are out of scope. Do not act on unresolved design decisions until the user confirms shared understanding, unless the user has already explicitly authorized implementation with the current decisions.
