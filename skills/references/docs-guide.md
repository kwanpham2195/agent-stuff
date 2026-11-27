# Documentation examples reference

Optional reference for writing docs: how to open a page, order the material, show code, and link between pages. It also covers short technical articles. Read only the sections that apply to the document at hand.

The examples here are kept for comparison. If this guide disagrees with [Writing reviewable artifacts](writing.md) or [unslop](../unslop/SKILL.md), those two win. The [writing examples](./writing-guide.md) are optional reading, not a prerequisite.

## Page structure

### Opening sentence

Begin with a plain definition of the thing the page covers.

> The `Scheduler` class runs queued jobs in the background.

> In this app, a workspace is a shared folder of projects that a team can edit together.

> Caching means keeping a copy of a result so the next request can skip the work.

Put one idea in each sentence. If the opening mixes a definition, use cases, and API names, split it up.

Avoid:

> The notifier sends short messages to users when a build changes state, used for alerts about failures, completed deploys, or queued retries, and reached through `app.notifier`.

Prefer:

> The notifier sends short messages to users when a build changes state. Use it for alerts about failures, completed deploys, or queued retries.

Mention the API entry point after the opening paragraph, or at the first place it is needed.

### Pair each concept with code

After you explain an idea, show it working. For example, after saying there are two ways to get a client:

> You can create a client in two ways.
>
> 1. From the `createApp` function:
>
> ```ts
> const app = createApp({
> 	onReady(client) {
> 		// use the client here
> 	},
> })
> ```

### Go from simple to advanced

Order the material by how many readers need it.

1. Begin with the most common case.
2. Add options and complexity one step at a time.
3. Put edge cases and advanced patterns near the end.

A page about saving data could run like this:

1. A single `storageKey` option, which is the easiest route.
2. Exporting and restoring snapshots, for more control.
3. Supplying your own storage backend, for full control.
4. Schema migrations, for advanced use.

### Keep paragraphs short

Aim for one to three sentences. Long blocks are hard to scan.

Prefer:

> Metadata is extra information that your application attaches to a record. For example, you might store the name of the person who created it, or when it was created.

Avoid:

> Metadata is additional data that can be attached to records and is not used internally by the library but can be leveraged by your application for custom functionality, such as the creator, timestamps, custom identifiers, or any other application-specific values you want to keep with the record without placing them in the main fields.

### Use tables for parallel items

When several methods or options share a shape, list them in a table.

| Method         | Description                          |
| -------------- | ------------------------------------ |
| `app.start()`  | Starts the background workers.       |
| `app.pause()`  | Stops taking new jobs.               |
| `app.stop()`   | Finishes current jobs, then exits.   |

### Asides and callouts

Use a blockquote for a helpful aside.

> If you only need the current status, call `app.status()` instead of reading the whole job list.

Use your docs framework's warning callout for things that can break a reader's setup.

```
<Callout type="warning">
  The client and server must run the same major version.
</Callout>
```

## Cross-references

### Link generously

Point to a related page instead of re-explaining it.

> To learn how to sync local state with other processes, see the storage guide.

### Link API names the same way every time

Use your docs framework's convention for linking to API reference pages, and use it consistently. Link the first mention on a page.

### Link to running examples

If a runnable example exists, link to it.

> For a full plugin that registers custom commands, see the command plugin example.

## Short technical articles

A technical article tells how a team solved an interesting problem. It reads more like an engineering blog post than a reference page. For the full guidance, read [blog-guide](blog-guide.md). The main differences from reference docs are below.

**Opening.** Reference pages open with a definition. Articles open by framing a problem, in a sentence or two, so the reader knows what it is about and why it is interesting.

Reference opening:

> The `Scheduler` class runs queued jobs in the background.

Article opening:

> Most task queues promise "at least once" delivery, and most users read that as "exactly once". We learned the difference after a customer received the same invoice email three times. Here is how we made our scheduler safe to retry.

A good article opening sets the context, states a tension, and shows what is at stake before it explains the fix. Root it in something a person experienced, such as a behavior, a convention, or a plain sense of what feels right.

**Arc.** Frame the problem, give the key insight, walk through the implementation, then close with where the code lives, the trade-offs, and what remains open.

**Tone.** Articles are warmer than reference pages. Use phrases like "the trick is" to mark the main idea. Add short asides about what made the problem hard. Describe the path, including attempts that failed. End with an opinion about the trade-off. Do not ramble, do not claim importance without evidence, and do not turn jokey.

**Voice.** Describe what we did instead of telling the reader what to do.

Avoid:

> Make every job idempotent, then retry freely.

Prefer:

> We could not guarantee a job ran once, so we made each job safe to run twice, and the scheduler retries freely.

## Priorities

When goals compete, favor them in this order.

1. **Accuracy.** Code must run. API references must be right.
2. **Clarity.** The reader should understand it on the first pass.
3. **Brevity.** Say it once. Cut sections that repeat what appears elsewhere.
4. **Scannability.** Use short paragraphs, clear headings, and plenty of code.

### Do not repeat yourself

When detailed examples already show a pattern, do not add a "Common uses" section with the same code shortened. Pick one:

- Keep the detailed examples only (preferred).
- Keep only the quick-reference snippets.
- Make sure each section adds information the others lack.

Show a full implementation once. If a quick-reference section is useful, make it a table that points to the full examples.

## Review checklist

When reviewing documentation, ask:

- [ ] **Opening.** Does the first sentence say what the thing is?
- [ ] **Code.** Does working code follow every concept?
- [ ] **Order.** Does complexity grow gradually?
- [ ] **Links.** Do related concepts link to each other?
- [ ] **Scannability.** Are paragraphs short and headings clear?

For more sentence-level examples, see the relevant part of the [writing examples](./writing-guide.md). Apply the standards in [Writing reviewable artifacts](writing.md) and [unslop](../unslop/SKILL.md).
