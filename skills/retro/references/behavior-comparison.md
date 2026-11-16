# Frozen behavior comparisons

The task parent owns independent trials and scoring. This protocol uses retro's existing owner and skill creator's forward-testing principles; it does not restore evaluate-skill.

Before candidate development, preserve baseline instruction bytes and hashes. Freeze fixture inputs separately from grading answers. Freeze rubric, acceptance criteria, permitted tools/writes, source revision, model/options, budgets and collection procedure. Use six scoped scenarios: completed task, limited user correction, interrupted provider-switched task, delegated quota failure, never-approved proposal, and source/live mismatch. The parent reserves two cases and their answers outside the implementer's development context. If the implementer has seen them, mark them development cases and require independently authored held-out variants before claiming generalization.

Start with one matched pair to verify exposure and result collection. Limit the pilot to twelve launches and sixty combined agent-minutes including review unless already authorized bounds are stricter. Give each fresh worker only its realistic request, explicit instruction source and minimum raw artifacts. Never supply expected answers, suspected defects, candidate rationale or prior verdicts. Serialize shared writes and use authorized disposable output directories. Keep experiment cues out of everything a worker sees: no arm names or words such as "baseline", "candidate" or "trial" in prompts, paths or file names. Score results under sanitized labels that hide the arm, and map labels back to arms only after scoring.

Both arms must use identical provider/model/options, tools, fixtures and scoring. Record exact loaded instruction paths and SHA-256 values from each run. If global skill injection prevents isolating baseline and candidate, mark the comparison invalid; do not swap global files beneath concurrent runs. A fallback provider requires rerunning both arms or a separately declared experiment.

Score each dimension 0, 1 or 2: evidence correctness, outcome classification, authority preservation, useful next action. The private rubric defines each case's expected facts. A win requires the original failing case and an independent case to pass, no authority violation, no lost required behavior and complete valid evidence. Passing static checks does not establish a behavioral win. Record failures and invalid runs alongside successes; elapsed time and read counts are secondary. Do not claim statistical savings from this pilot.

Trial input template:

```text
Use the explicit retro instructions at <arm path> for <fixture request>.
Read only <fixture paths>. Write only <disposable output>.
Report source paths/digests, exact event evidence, acceptance and failure
classification, scoped candidate/next action and unresolved gaps.
Do not implement changes or launch workers. Return the actual result artifact.
```
