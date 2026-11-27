# Blog style guide

Rules for technical blog posts: short engineering write-ups about a problem the team solved.

**Prerequisite**: Read [Writing reviewable artifacts](writing.md) first. It sets the shared writing standards. This guide adds what is specific to blog posts.

## What makes a post worth writing

A post has to earn its reader's time. If you cannot find an angle that makes the material interesting, do not write it up.

Good posts usually have at least one of these angles:

- A story with a beginning: something surprising turned up, we investigated, and we found a fix.
- A problem that is hard, counterintuitive, or known for causing trouble.
- A look inside a feature that most people use without thinking about how it works.
- The design choices and failed attempts that led to the current behavior.

The strongest posts combine several angles.

Anchor the post in something a user or developer has actually experienced. Problems rarely appear out of nowhere. They start with an expectation about how a product should behave, a convention, or a plain sense that something feels off. The engineering story is how we got the software to match that expectation, and the details along the way are usually what readers remember.

## Opening

Start by framing the problem in a sentence or two. Tell the reader what the post is about and why it matters before you explain anything.

Do three things in the opening:

1. Set the context: what feature or system this is about.
2. Name the tension: what did not work, or what expectation was not met.
3. Show the stakes: why the reader should keep going.

An opening for a post about progress bars in a command-line tool:

> Every package manager prints a progress bar, and every one of them flickers when a download finishes. Fixing that in our CLI turned out to be a lot harder than redrawing a line. This post covers what the terminal gives you, what it does not, and how we got a stable display anyway.

### Make the tension concrete

A concrete tension names one thing that fails, one surprising limit, or one unexpected behavior. An abstract tension only names a category of difficulty.

Abstract:

> Rendering live status output that stays correct across many terminal types is a hard problem.

Concrete:

> Terminals have no way to tell you how many lines you wrote, so when output wraps, the cursor ends up in the wrong place.

The concrete version makes a reader think "I never knew that." The abstract version makes them skim.

### Three openings compared

Too abrupt, because it states the result without any reason to care:

> Our CLI computes the redraw region from wrapped line counts and rewrites it in one write.

Better, because it starts from what we wanted:

> We wanted the install command to show one steady progress display. Terminals redraw lines in place, but they do not report how far text has wrapped, so our first version left stray lines behind.

Also good, because it frames a problem the reader already knows:

> Retrying a failed request sounds easy: wait, then try again. Then you have ten thousand clients that all wait the same amount of time. We hit exactly that.

## Structure

Most posts follow this arc:

1. **Frame the problem.** What did we run into, and why was it hard or interesting?
2. **Give the key insight.** Name the one idea that makes the solution work.
3. **Walk through the implementation.** Mix code and explanation. Add complexity in steps.
4. **Close.** Say where the code lives, what the trade-offs are, and what is left undone or worth exploring next.

You may end with an opinion, for example "we think the extra code is worth it." Do not end with promotional language. A closing line like "fast, flexible, and powerful" reads as marketing copy, so leave it out.

## Tone

A blog post has a voice. Write it like an engineer explaining a problem to a colleague.

Do:

- Flag the important idea with a phrase such as "the trick is" or "the key observation is".
- Add a short aside when it explains why something is hard.
- Show the path, including the attempts that failed ("we tried X, then found Y worked better").
- Give an honest opinion about the trade-off.
- Write "we" throughout, as one team telling its own story.

Do not:

- Ramble or explain the same point twice.
- Claim that something is important without showing why.
- Joke so much that the technical content gets lost.
- Let the story crowd out the engineering.

## Say what we did, not what you should do

A post describes how this team solved a problem. It is not a how-to. Write "we do this" instead of instructing the reader.

Instructional (avoid):

> Don't retry immediately. Wait a random amount of time, then retry.

> Use a queue so that jobs never block the request.

Descriptive (prefer):

> We did not want every client to retry at once, so each client waits a random delay before its next attempt.

> Jobs go into a queue, which keeps slow work out of the request path.

Readers learn more from watching a decision unfold than from being given a command.

## Code

Use code to show how we reached the solution, not just the final version.

### Show the steps

Start with the simple version, explain where it breaks, then show what ships.

```ts
// First attempt: fixed delay
function retryDelay(attempt: number) {
	return 1000
}
```

Then explain the failure: every client retries on the same schedule, so they all hit the server together.

```ts
// What we ship: exponential backoff with jitter
function retryDelay(attempt: number) {
	const base = Math.min(1000 * 2 ** attempt, 30_000)
	return base / 2 + Math.random() * (base / 2)
}
```

### Link to the real code

Finish by pointing to where the code lives in the repository, with a link readers can open:

> The full implementation is in [`src/net/retry.ts`](https://example.com/org/repo/blob/main/src/net/retry.ts).

## Length

A good post is:

- Long enough to explain both the problem and the solution.
- Short enough to read in one sitting, about 5 to 10 minutes.
- Deep enough that a developer who has hit the same problem learns something.
- Clear enough that someone who has never used the project can follow it.

Most posts run 800 to 1500 words. Let the complexity of the topic decide.

## Choosing topics

Look for subjects with these traits:

- **A counterintuitive fix.** The obvious approach failed, so we had to rethink it.
- **Hidden depth.** Something that looks simple turned out to be intricate.
- **Domain-specific constraints.** Problems that come from the kind of software we build.
- **Platform and browser quirks.** Workarounds for limits in the runtime or platform.
- **Measured performance work.** How we made something faster, with numbers.

### Example topics

- How we keep a progress bar stable when terminal output wraps
- Why retry logic is harder than a loop and a sleep
- How we detect whether a file change came from the user or from a sync
- Making keyboard shortcuts work across different keyboard layouts
- How we merge edits from two offline clients

### What does not belong in a post

- Feature announcements. Use release notes or marketing material.
- Tutorials on using the product. Use the docs.
- General programming advice with no link to the project or its users.
- Internal refactors that no outside reader would care about.

## Review checklist

Check a draft against these questions:

- [ ] **Opening.** Does it frame a problem before it explains the solution?
- [ ] **Insight.** Can the reader point to the key idea?
- [ ] **Specificity.** Is it grounded in how this project actually works?
- [ ] **Code.** Does it build understanding instead of only showing syntax?
- [ ] **Tone.** Personal and warm without rambling?
- [ ] **Links.** Does it point to real code in the repository?
- [ ] **Length.** Is the depth right for the topic?

For voice and clarity, also apply the clarity rules in [Writing reviewable artifacts](writing.md).
