# Illustrative chat exercise

This anonymous example demonstrates scope and reasoning, not a universal interview or architecture. Adapt it to the role and agreed duration. All numbers and assumptions below belong to this example only.

## Candidate brief

Design text chat between a customer and a support agent in one region. Customers and agents can send messages, receive incoming messages, and retrieve conversation history after reconnecting. Access requires membership in the conversation. Exclude attachments, group chat, cross-region disaster recovery, and search.

Assume 100,000 concurrent connections and 10,000 message sends per second at peak, with text payloads at most 4 KiB. Assume each conversation has one customer and one assigned agent, with at most two connected devices per participant. Retain messages for 30 days. These are exercise assumptions, not facts about a production service.

For this example, evaluate a 10 minute peak-load window. Eligible recipient operations are those accepted while the recipient has an authenticated live connection and has acknowledged a health check within the preceding 30 seconds; determine eligibility at acceptance, not from later delivery behavior. Target p95 delivery within 500 ms from server acceptance to the recipient device's delivery acknowledgement. Define acceptance as a durable commit that survives a single process crash. Report eligible attempts, timely acknowledgements, late acknowledgements and missing acknowledgements separately. Include missing acknowledgements as deadline misses rather than dropping them from latency samples; require at least 95% of all eligible attempts to acknowledge within the deadline. A recipient becoming slow or disconnecting after acceptance remains in that denominator. Recipients ineligible at acceptance still need an explicit recovery or expiry outcome. These window and eligibility choices are illustrative exercise assumptions. Discuss authorization, ordering within a conversation, retries, duplicates, and how you would measure these guarantees.

Trace these failures:

1. A message commits, then the accepting process crashes before replying to the sender.
2. A recipient device reconnects while new messages arrive.
3. A recipient is slow, or a delivery consumer falls behind.

Produce a component sketch, important contracts, and scenario traces. Explain tradeoffs and recovery limits. No particular language, database, broker, or transport is required.

## Private timing and clarification replies

An illustrative 60 minute schedule uses 8 minutes for clarification, 15 for the first design, 20 for the three failure traces, 10 for selected risk followups, and 7 for tradeoffs and candidate questions. For a different duration, reduce scope and probe count.

Ready replies consistent with this brief:

- Ordering is per conversation, not global. The candidate should define the ordering mechanism and its interaction with retries.
- A reconnect within retention must recover missed committed messages. An older cursor may expire, but the service must tell the device how to resynchronize and what history is no longer available.
- A delivery acknowledgement means the device reports receiving the message. Read status requires a separate user action or explicit client contract. Presence and typing hints need not be durable.
- Unauthorized sends and deliveries must be rejected. Ask the candidate to propose a bounded revocation policy rather than hiding one in the reference answer.

## One defensible reference design

Authenticated connection gateways route sends to a conversation service. The service checks membership, deduplicates a client operation identifier, assigns a conversation sequence, and commits the message with a durable delivery event in one transaction. A delivery worker routes events to connected devices. Devices acknowledge receipt and use history queries with sequence cursors to recover gaps. This is one possible design, not a required technology stack.

For the first failure, retrying the same operation identifier returns the original committed result. Discuss the deduplication retention boundary. Acceptance does not prove a socket write, device receipt, or user read.

For reconnect, establish a history boundary and combine replay with live traffic without losing messages at the handoff. Sequence identifiers let the device detect gaps and discard duplicates. A candidate may propose another protocol if its ordering and recovery argument holds.

For slow recipients or lagged workers, bound buffers, measure lag, and recover from durable history. If retention has expired, return an explicit expiry result. Ephemeral hints may be dropped. A successful socket write alone does not establish durable recovery or receipt.

Prioritize these failure guarantees before deeper probes. Select authorization revocation, resource fairness, or recipient load validation when the emerging design makes them useful. Record independent reasoning, neutral probes, hints, and topics not covered separately. Do not grade by matching this architecture.
