# Bounded recurring review

Prove the manual comparison first. This file installs no schedule and grants no cross-workspace access, launches or expanded authority. A future recurring review needs an explicit owner, source scope and output contract.

Read only explicitly published improvement receipts from authorized task owners. Keep stable work/candidate IDs and an evidence watermark per candidate. Run the read-only review command against the prior receipt and the current validated input with an explicit `--as-of` UTC timestamp. It reads no clock. At or after a known follow-up deadline, incomplete task coverage or missing observation evidence produces one overdue update. Later unchanged overdue reviews produce none. Unknown dates produce no inferred deadline. Rejected and followed-up candidates do not become overdue. New evidence updates the same candidate; a missing candidate remains recorded rather than treated as resolved. A changed digest or newly overdue deadline is a reason to review, not evidence of improvement or a fabricated task observation.

Watermarks cover candidate evidence and overdue status, not the as-of timestamp itself. An older hash-only watermark produces one reconciliation update. Persist the new watermark after delivery; subsequent unchanged reviews deduplicate normally. Use nondecreasing as-of times for sequential deliveries, and the same explicit time when replaying a delivery.

Persist the new watermark only after the report is delivered and its receipt is durable. Reconcile uncertain delivery before retrying. The existing job owner owns serialization and receipt writes. Reports distinguish delivered report, authorized experiment, deployed change and measured improvement. Show repeated mistakes with denominators, overdue evaluations and deployed candidates awaiting follow-up, with evidence links and the smallest next experiment.

Suggested prompt for a future authorized recurring review:

> Within the existing time and source limits, read the designated published improvement receipts. Validate them and compare candidate evidence watermarks with the prior delivered receipt. Report only new or changed candidates and overdue follow-up, retaining stable IDs. Unchanged evidence creates no duplicate proposal or launch. Link actual evidence, acceptance, deployment and uncertainty. Save the resulting watermark in the existing delivery receipt only after successful delivery. Do not launch experiments, change shared instructions, expand source scope or add schedules from this reporting job. Technical implementation continues under each task owner's separately recorded outcome, budget and regression gates.

Integration depends on the schedule owner accepting the published input paths, receipt extension, delivery reconciliation and remaining budget. That owner's workspace requires its own authorization. Do not inspect it merely because a scheduler lists it.
