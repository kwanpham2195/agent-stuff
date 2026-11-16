# Private interviewer guide

## Plan the conversation

Choose timed phases whose minutes sum to the agreed duration. Allow time for clarification, a coherent first design, core scenario and failure traces, selected deeper probes, and candidate questions. Adjust depth for role and seniority. A shorter interview needs fewer probes, not faster coverage of every topic.

For each phase, provide its purpose, a ready opening question, the expected discussion, and a transition or stopping point. Explain what the question reveals near the question itself. Keep illustrative reasoning separate from candidate requirements.

Prepare ready replies to likely functional and workload questions. Cover users and permissions, scope, traffic shape, payload sizes, fanout or concurrency where relevant, retention, consistency expectations, and target measurement boundaries. State which replies are fixed exercise facts and which are interview assumptions. If a missing fact changes the intended problem, clarify with the user before finalizing. During the interview, record any newly agreed assumption and assess the design against it.

## Reference reasoning

First define the observable expectations for selected competencies at the target seniority. Use concrete evidence anchors, not a universal score: for example, identifying an uncertain outcome, explaining a retry contract, and tracing its limits. Keep reasoning quality and correctness separate from assistance level and coverage; independent reasoning can be wrong, and a hinted answer can be correct without demonstrating independence.

Offer one defensible design to help the interviewer follow the conversation. It is not a grading key. Describe responsibilities and data flow before naming products. Candidates may choose other technologies if their guarantees, constraints, and tradeoffs are coherent.

Include enough detail to trace a normal operation and the selected failures:

- Identify the contract, durable decision point, ownership, identifiers, and ordering boundary. Name relevant entities, access patterns and invariants; connect them to storage, partitioning and consistency choices.
- Trace requests, state changes, responses, retries, and recovery. Explain where duplicates, gaps, or stale state can appear.
- Start with the simplest adequate design. Use capacity estimates that change a decision; identify the bottleneck, cost and measured thresholds that would justify added complexity. Distinguish average traffic from bursts and fanout.
- Explain operational signals, recovery limits, and a strong alternative with its tradeoff. Leave unresolved issues visible.

Do not require every candidate to independently discover every reference detail. Evaluate the agreed guarantees and the reasoning that supports them.

## Select followups by risk

Prioritize core guarantees and failures. Choose deeper followups based on the problem, role, emerging design, and remaining time. These are a menu, not a mandatory checklist:

| Risk | Useful probe | Reasoning to explore |
| --- | --- | --- |
| Authorization on existing connections | What happens to an already connected device when access is revoked? | Enforcement at operation and delivery boundaries, revocation propagation, bounded stale access, and reconnect behavior. |
| Abuse and resource fairness | Can one tenant or slow client exhaust shared resources? | Admission, quotas, bounded buffers, backpressure, isolation, and observable rejection behavior. |
| Retention and cursor expiry | What happens when a reconnect cursor predates retained history? | An explicit expiry contract, resynchronization or loss disclosure, and retention consistency. |
| Backup and failover | Which acknowledged operations survive failover or restore? | Replication versus backup, recovery point and time, split ownership, fencing, and stated data loss boundaries. |
| Protocol and schema rollout | Can old and new clients or consumers coexist during rollout? | Version negotiation, compatible changes, migration ordering, rollback, and incompatible payload handling. |
| Recipient load and faults | How would you test delivery under fanout, slow readers, and consumer lag? | Realistic recipient distributions, load at the receiving side, controlled faults, recovery measurements, and correctness checks beyond send throughput. |

Use a neutral question first. Give a hint only when it serves the interview's purpose, and record the help. Do not silently turn a followup into a new requirement or penalize a candidate for declining an unsupported guarantee.

## Record evidence

For each selected competency, record the observed reasoning or decision, relevant scenario, and assistance level:

- Independent: the candidate raised and reasoned through it without prompting.
- Neutral probe: the interviewer asked an open question without suggesting the mechanism.
- Hint: the interviewer supplied a direction, mechanism, or missing insight. Record the hint and what the candidate did afterward.
- Not covered: time or scope prevented assessment. This is absent evidence, not failure.

Distinguish a contradicted guarantee or unresolved flaw from an unasked topic. Keep CV claims separate from observations. Use concrete notes rather than inferred personality or confidence. If a rating is requested, anchor it to the chosen competencies, seniority, and observed evidence, and disclose coverage limits.
