---
license: MIT
name: drafting-for-others
description: Draft or edit messages that go out under the user's name, such as emails, chat messages, PR/MR review comments, support replies, ticket updates, and wiki pages. Use when the user asks to draft, reply, word, rephrase, soften, or review the tone of something another person will read.
---

# Drafting for others

How to write anything another human will read under the user's name. The goal: the reader
understands the why, has a way forward, and never feels policed.

This skill decides *how the words land*. It does not decide *whether* to approve, reject or
escalate; that judgment belongs to the user.

## Configuration

Read the `Skills configuration` section of `AGENTS.md` for `voice` notes (tone, banned
punctuation, sign-off, language). Defaults if absent: warm, direct, plain English, no em dashes.

## Drafting

- **Explain the why.** A rule without a reason reads as gatekeeping.
- **Ship the fix with the objection.** Every "this needs to change" comes with a concrete
  suggestion: a one-line diff, a link, or the exact next step. That turns "blocked" into "here you go".
- **About the work, never the person.** Findings are about the code, the request, or the policy.
- **Assume good intent.** Most people hitting a rule followed a path that used to be correct.
- **Match the channel.** A chat reply is two lines; a ticket comment has context; an email has a
  subject that says what is needed.
- **Respect the configured voice.** By default, no em dashes in outbound text.
- **Use the team's canned wording** for recurring policy replies when one exists; do not invent policy.

## Editing the user's own writing

Be strict about the bar, never strict *at* the user. Flag substantive problems (accuracy, tone,
missing fix, unclear ask) and offer to fix them. An explicit editing request authorizes the edit;
otherwise propose before rewriting, and keep their substance.

Lead with what genuinely works when there is something; skip praise when there is not.
Automatic praise stops carrying information.

## Drafting is not sending

A draft is never permission to post, send, comment, approve, or merge. Return the draft. Publish
only when the user explicitly asks, through whatever tool and permission they have granted.
Contacting someone directly (DMs, end users, customers) always needs explicit approval.

## Example

> You caught both issues, nice. The permissions one especially; people slide right past it.
>
> One thing: read the opener out loud. "This is wrong" carries more edge on the page than you
> mean, and it's their first PR with your team.
>
> Also, two blockers and zero fixes. One suggested line each and this lands as "here you go"
> instead of "come back later". Want me to take a pass? I won't touch your substance.
