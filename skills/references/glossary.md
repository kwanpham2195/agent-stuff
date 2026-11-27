# Working vocabulary

Words that change what an agent does. Say one of them and the agent knows the scope, the stopping point and what you expect back. Each entry says what you get.

## Limit how far the agent goes

| Say | You get |
| --- | --- |
| **Read-only** | Investigation only. Nothing is written. |
| **Draft only** | The artifact, then a stop for your decision. |
| **Authorized for X** | Exactly action X. Anything outside it needs a new yes. |
| **Non-goal** | A named thing the work must not touch. |
| **Reversible / irreversible** | Irreversible actions (push, delete, send, publish) get a question first. |
| **Gate** | A point where the agent stops and waits for you. |

## Say what done looks like

| Say | You get |
| --- | --- |
| **Acceptance** | "Accept when X": the agent finishes without asking again. |
| **Define outcome** | Observable acceptance written down before any building. |
| **Verify** | Evidence read back from the source, not a claim. |
| **Blocker** | Something that stops the work. Preferences are not blockers. |

## Choose how much process

| Say | You get |
| --- | --- |
| **Oneshot** | Small change: made, verified, delivered. No artifacts. |
| **RPI** | Medium work: research, design, outline, phases, verify, deliver. |
| **PRD** | Large work: research, requirements document, design, outline, phases. |
| **Freeform** | You pick the stages. |

## Choose the thinking mode

| Say | You get |
| --- | --- |
| **Research** | A bounded investigation with sources and findings saved. |
| **Discuss** | Short rounds of questions that turn an idea into a plan. |
| **Plan** | An ordered outline of the work, before any code. |
| **Prototype** | A throwaway build that answers one design question. |
| **Advisor** | A second opinion on a hard tradeoff. |
| **Review** | An independent check of a change, plan or document. |
| **Audit** | A systematic check of a whole area against a standard. |
| **Show me** | A diagram or contract instead of prose. |
| **Unslop** | Writing with the AI-sounding phrasing removed. |

## Run the backlog (Desk)

| Say | You get |
| --- | --- |
| **Intake** | Record new work or file an issue for later. |
| **Triage** | The backlog, one item at a time, each with a recommendation. |
| **Continue / park / close** | The three outcomes for a work item. |
| **Now / next / later** | The priority you set on an issue. Only you set it. |
| **Drop** | An issue you will not do, with a one-line reason. |
| **Promote** | A local issue moved to a real tracker. |
| **Broadcast** | One rule message sent to every running task thread. |
| **What needs me?** | A short list of decisions waiting on you, with links. |
| **Settle** | You close out the briefs you have read. |

## Move work along

| Say | You get |
| --- | --- |
| **Take #N** | The agent picks up GitHub issue N, implements it and opens a PR. |
| **Address** | Review comments answered or fixed, each cited by file and line. |
| **Commit** | A completed, verified slice committed. It grants no push. |
| **Push / land** | Push the branch. Land is merge plus tidy-up. |
| **Watch** | The agent monitors a PR's checks and comments. |
| **Checkpoint** | State saved so work survives a pause. |
| **Handoff** | Work passed to another owner with what they need. |
| **Recall** | Workspace state rebuilt from records and saved sessions after compaction or a harness change. |
| **Reconcile** | Saved evidence checked against the current source and any verified discrepancy resolved. |
| **Supersede** | A new decision replaces an older one. |
| **Deliver** | The finished result handed to you for acceptance. |

## Hand work to agents (T3)

| Say | You get |
| --- | --- |
