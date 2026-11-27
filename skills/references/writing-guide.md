# Writing examples reference

Optional companion for wording choices: tone, sentence repair, and how to lay out code samples. Open only the section that matches the problem in front of you. Every before-and-after pair here is an illustration kept for comparison. Where this page and [Writing reviewable artifacts](writing.md) or [unslop](../unslop/SKILL.md) disagree, those two decide.

All samples describe an invented job-queue library called Taskline and an invented expense-tracking web app called Ledgerly. Neither exists.

## Intended voice

Write as a colleague who built the thing and is walking a teammate through it. State what is true, say what to do next, and back it up with one concrete example. The reader should finish a paragraph knowing something specific.

### Qualities to aim for

| Quality      | In practice                                                    |
| ------------ | -------------------------------------------------------------- |
| Direct       | Assert facts plainly; skip softeners                           |
| Front-loaded | Put the working approach first, before any failed alternatives |
| Practical    | Describe the task to finish, not the theory behind it          |
| Candid       | Name gaps, rough edges, and unfinished parts                   |
| Personable   | A little warmth is fine; chattiness is not                     |

### Qualities to avoid

- Textbook stiffness. Readers are people, not examiners.
- Filler conversation that spends the reader's time.
- Talking down. Assume the reader is capable.
- Brochure tone. Nobody trusts it.

## Voice, shown by contrast

### State things without hedging

**Prefer:**

> The `Worker` class pulls jobs off a queue and runs them.

> A worker handles one job at a time unless you raise `concurrency`.

> Retries are on by default, three attempts per job.

**Avoid:**

> The `Worker` class can generally be used to process jobs from a queue.

> A worker may tend to handle a single job at a time in some configurations.

> Retries are sometimes enabled by default.

### Say what to do

**Prefer:**

> To add a job, call `queue.add`. To drop one, call `queue.remove`.

> A job is a function call that has been saved for later, with its arguments.

> Don't run the in-memory backend in production. It loses everything on restart.

**Avoid:**

> This section covers the methods used for adding and removing jobs.

> A job may be understood as a unit of deferred work inside the system.

> Use of the in-memory backend in production settings is not advised.

### Admit what is missing

**Prefer:**

> Taskline has no scheduler for cron-style jobs. You will need to bring your own.

> Until the guide for plugins is written, read the sample plugin in the repo.

> We may change the wire format between minor versions.

**Avoid:**

> Taskline offers a full-featured solution to nearly every scheduling need.

> Plugin documentation will arrive in due course.

> The wire format is kept stable across releases.

### Use real material

Skip flowery language, long metaphors, and invented scenarios. Show actual code and an actual use.

**Prefer:**

> The queue keeps every pending job in a list ordered by priority.

> Here is a job that emails a receipt after an expense is approved.

> The worker reports failures through its `onError` callback.

**Avoid:**

> Picture the queue as a conveyor belt winding through a factory, carrying parcels toward their fate.

> Suppose you run a rocket-launch company and need a countdown scheduler...

> The worker conducts an orchestra of retries and timeouts.

A brief gloss is fine, as in "a job is just a JSON record". Long analogies are not, and neither are detours into hypothetical products.

## Machine-sounding prose

Generated text leans on a recognizable set of habits. Cutting them keeps the page sounding like a person. A fuller list lives at [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

### Claims of importance with no content

The text announces that something matters but never says why. Typical offenders: "stands as a testament to", "plays a pivotal role", "highlights how essential it is", "a defining moment", "a turning point", "a long and storied tradition", "a lasting legacy".

**Avoid:**

> The scheduler plays a pivotal role in Ledgerly's design and stands as a testament to thoughtful engineering.

**Prefer:**

> The scheduler decides when each reminder email goes out. It checks for due reminders every minute.

### Sentences that end in an -ing clause

This is the most frequent habit, so look for it on every pass. A sentence finishes with a participle phrase that gestures at significance without adding a fact:

- "...reinforcing the value of X"
- "...demonstrating the lasting impact of Y"
- "...showing how much Z matters"
- "...delivering a smooth experience"
- "...reflecting a dedication to quality"

**Avoid:**

> The worker retries failed jobs automatically, delivering strong reliability and showing how much resilience matters.

**Prefer:**

> The worker retries failed jobs automatically. A temporary network error no longer loses the job.

Plain participles at the end of a sentence are also weak. The point lands last, after the verb has already done its work, and a page full of them reads as monotone and machine-made. Typical shapes:

- "...so you can X"
- "...which lets teams X"
- "...which simplifies X"
- "...offering X"
- "...building X"
- "...leading to X"
- "...triggering X"

**Avoid:**

> Queues are durable, letting you restart the server without losing work.

> If `delay` is set, the job waits before its first attempt, producing a staggered start.

> The client has helpers for bulk operations, simplifying large imports.

**Prefer:**

> Queues are durable. You can restart the server without losing work.

> If `delay` is set, the job waits before its first attempt. This produces a staggered start.

> The client has helpers for bulk operations, which you can use for large imports.

Or start from the main point:

> Set `delay` to stagger the start: the job waits before its first attempt.

> Use the bulk helpers for large imports.

How to fix it: cut the sentence in two, or reorder so the key fact comes first. A comma followed by a word ending in -ing near the end of a sentence is the cue to rewrite.

### Stock connectors

These show up so often that they carry no meaning: "Moreover," "Furthermore," "In addition," "It should be noted that," "It's worth pointing out that," "That said,". Deleting them nearly always improves the sentence. When a link between two ideas is needed, a short word does it ("But," "And," "So") or the sentences can be reordered.

**Avoid:**

> The worker logs every attempt. Furthermore, it records how long each took. Moreover, it keeps the last error for each job.

**Prefer:**

> The worker logs every attempt, how long it took, and the last error for the job.

### Lists of exactly three

Generated text reaches for triples by reflex. Real material comes in twos, fives, or nines. When you notice three, check whether the content has three things or whether the rhythm asked for them.

**Avoid:**

> Ledgerly is simple, fast, and reliable.

> The report gives you clarity, speed, and insight.

**Prefer:**

> Ledgerly is simple and fast.

> The report shows spending by category for any date range.

### Sales vocabulary

Training data is full of marketing copy. In technical writing, drop words such as "stunning", "elegant", "seamless", "effortless", "powerful", "robust", "state-of-the-art", along with phrases like "empowers teams to" and "unlocks the full potential of".

**Avoid:**

> Ledgerly empowers households to unlock the full potential of their money through a seamless and powerful budgeting experience.

**Prefer:**

> Ledgerly tracks household expenses and shows monthly totals per category. You can import bank statements as CSV files.

### Dashes used for drama

Several em dashes in one paragraph usually mean commas, colons, or full stops would have worked. One per paragraph is acceptable. The worst cases mimic ad copy, stressing a clause for effect, or take the place of a comma or a parenthesis.

**Avoid:**

> It isn't merely a retry setting—it's a safety net for your whole pipeline.

> The queue is durable—it survives restarts—and it's typed—end to end.

**Prefer:**

> The retry setting also protects the rest of your pipeline from one-off failures.

> The queue is durable and survives restarts. Its types cover the whole API.

### "Not X but Y" framing

Setting up a denial just to contradict it is a tell. Say what the thing is.

**Avoid:**

> Taskline isn't only a queue; it's a full job platform.

> The dashboard isn't just a chart, it's a window into your spending.

**Prefer:**

> Taskline is a queue with a worker, a retry policy, and a plugin system.

> The dashboard charts your spending by week.

### Words that give it away

Some words occur far more often in generated text than in human text. They are not banned, but check that each is the real fit.

| Word          | Often better as          |
| ------------- | ------------------------ |
| delve         | look at, dig into        |
| crucial       | important, needed        |
| highlight     | show, point out          |
| harness       | use                      |
| employ        | use                      |
| tapestry      | mix, set                 |
| intricate     | detailed, involved       |
| cultivate     | grow, build              |
| enhance       | improve                  |
| champion      | back, lead               |
| landscape     | field, area              |
| synergy       | (nearly always cut)      |

### Bullets that start with a bold label

In running explanation, a list of bold-labeled lines is a chatbot trademark.

**Avoid:**

> - **Durability**: Jobs survive a server restart.
> - **Typing**: Every payload has a declared type.
> - **Backends**: Redis and SQLite are both supported.

**Prefer:**

> Jobs survive a server restart, and every payload has a declared type. Redis and SQLite are both supported as backends.

The bold-label list is acceptable in reference pages such as API listings or changelogs, where readers scan instead of read. If the items are truly parallel, a table works too.

### Averaging out specifics

Generated text swaps unusual, concrete facts for upbeat generalities, because most of what it learned describes notable things in the same few approving words.

**Avoid:**

> The export feature is a versatile and powerful tool that helps users produce polished reports.

> Priya is an accomplished engineer who has contributed greatly to the project.

**Prefer:**

> The export feature writes a month of expenses to a CSV or PDF file, with one row per transaction.

> Priya wrote the retry logic that most users rely on.

Keep the specifics. If you lack them, find them, or drop the claim. A vague endorsement tells the reader nothing.

### Same-sized sentences

Generated paragraphs run at one tempo, with sentences and paragraphs of about equal length. Human writing alternates: a short sentence, then a longer one that carries more detail. Let the material set paragraph size.

**Avoid:**

> The queue stores pending jobs. The worker runs each job. Plugins add extra behavior. Hooks react to job events.

**Prefer:**

> The queue stores pending jobs, and the worker takes them one by one. Plugins add behavior around that loop. Each plugin can attach hooks, which fire on job events such as start, finish, and failure.

If a passage sounds flat, mix sentence lengths and openings. Begin some with the subject and others with a clause.

## Grammar and mechanics

### Who is speaking

**Address the reader as "you":**

> You can reach the queue from the worker in two ways.

> Change a job's priority with `queue.setPriority`.

> Make sure only one `Scheduler` instance runs per deployment.

**Use "we" for advice and project-level statements:**

> We start the worker after the queue is configured, not before.

> We suggest the Redis backend for anything beyond a single machine.

**Name the software when the software acts:**

> Taskline ships with a built-in logger.

> The worker records each attempt in its log.

> The retry policy decides how long to wait. It multiplies the delay after each failure.

Don't write "we log each attempt" when the worker does it. That mixes up the team and the code.

**Skip:**

- The singular first person ("I'd suggest...")
- Passives that hide who acts ("It is advised that...")

### Active and passive

**Default to the active voice:**

> The queue keeps pending jobs in a sorted list.

> Each plugin wraps the job and then calls the next plugin in the chain.

> Taskline serializes payloads as JSON before saving them.

**Use the passive only when the doer is unimportant or unknown:**

> Jobs are stored as rows with a status column.

> The payload is validated before the job is saved.

**Active voice in tables too.** When a table describes what happens, give the sentence a subject that acts:

| Avoid                              | Prefer                                                    |
| ---------------------------------- | --------------------------------------------------------- |
| "The job is held for a while"      | "The worker holds the job" or "The job waits briefly"     |
| "The email is being sent"          | "The mailer sends the email"                              |
| "Old entries are dropped from log" | "The logger drops old entries from the log"               |

### Sentence shape

Write as a person talks, favoring short and clear sentences without turning stiff. Natural text has a pulse: some sentences are brief, some run a little longer. Aim for easy reading, not uniform length.

**Prefer:**

> In Taskline, a job is a saved function call.

> Jobs are plain records in the backend. Here is one for a receipt email.

> When a job fails, the worker waits and tries again. After the last attempt, it moves the job to the dead list.

**Avoid tangled, nested sentences:**

> When a job throws an error during execution, the failure is first captured by the worker's error handler so that attempt counts can be updated before the job is handed back to the queue, from which the retry policy decides whether it re-enters circulation.

Length is not the real issue. The load on the reader's memory is. Split an idea when a sentence makes the reader juggle too many parts.

### Contractions

Contractions are welcome: it's, we've, you'll, won't, don't, can't, shouldn't.

> It's a small library for background jobs, and it's what runs our nightly exports.

### Headings

**Use sentence case.** Capitalize only the first word:

- "Retry policies", not "Retry Policies"
- "Writing a plugin", not "Writing a Plugin"
- "Queues and priorities", not "Queues and Priorities"

**Exception:** keep capitals on proper nouns and technical names:

- "Redis backend"
- "HTTP endpoints"
- "WorkerOptions type"

## Code samples

### Open with a full, working one

The first snippet in a section should run as written. Later ones may show only the changed part.

**Prefer:**

```ts
import { Queue, Worker } from 'taskline'

const queue = new Queue('receipts', { backend: 'sqlite://jobs.db' })

new Worker(queue, async (job) => {
  await sendReceipt(job.data.expenseId)
})
```

**Avoid:**

```ts
// Pass a backend to the Queue
new Queue('receipts', { backend: '...' })
```

### Comments that add information

Comment on what the code can't say for itself, not on what it plainly does.

```ts
queue.add(
  'receipts',
  { expenseId: 'exp_204' },
  { attempts: 5 } // Overrides the default of three
)
```

### Realistic data

Use values a real app would have, not stand-ins.

**Prefer:**

```json
{
  "name": "receipts",
  "data": {
    "expenseId": "exp_204",
    "recipient": "ana@example.com"
  },
  "attempts": 3
}
```

**Avoid:**

```json
{
  "name": "job-name",
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

When a type requires branded identifiers, build them with the helper, such as `jobId('204')`, so the compiler stays quiet.

## Other rules

- Leave out any mention that an AI wrote the text
- Spell in American English
- Keep grammar plain; skip rare words, jokes, and idioms tied to a culture
