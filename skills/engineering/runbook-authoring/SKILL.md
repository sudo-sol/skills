---
license: MIT
name: runbook-authoring
description: Draft or review operational runbooks for repeatable procedures, with verified steps, expected results, stop conditions, recovery and escalation. Use when the user wants to document an operational task, turn tribal knowledge or a past incident into steps, or check whether an existing runbook is safe and usable.
---

# Runbook authoring

Produce practical, evidence-based instructions for a recurring operation. A runbook is guidance,
not authorization to perform its steps.

## Draft first

- Return the runbook in the conversation by default. Save to a file only when the user names
  the file or explicitly asks you to save it.
- Never publish to a wiki, tracker, or repo host without an explicit request.
- For a review-only request, report gaps and suggested changes; do not rewrite the source.
- Prefer improving an existing runbook over creating a duplicate.

## Gather and verify

1. Pin down the operation, the operator (who runs it), when to use it, and what it is not for.
2. Read existing local docs and the source of truth (code, config, CLI `--help`) before drafting.
3. Establish prerequisites, access, tools, inputs, expected results, stop conditions, recovery,
   and a real escalation route. Do not invent commands, owners, contacts, dates, permissions,
   or system behavior. Mark gaps as `TBD: <what needs confirming, by whom>`.
4. Separate verified steps from untested ones. Record "Last verified" only with real evidence and
   a date; otherwise label the runbook Draft or Unverified.
5. Walk it as the operator: can they tell what to do, what success looks like, when to stop, and
   whom to call?

Apply extra scrutiny to anything touching infrastructure-as-code, cloud consoles, IAM,
credentials, production data or state files. If the repo has engineering standards, load
the `standards-check` skill through the client’s skill mechanism and distinguish confirmed requirements from candidates.

## Safety

- Make read-only and state-changing steps visibly different (e.g. a ⚠️ marker and an approval line).
- Where infrastructure is managed as code, do not write manual console changes as the procedure.
- Never include real secrets, tokens, sensitive variable values or state contents, or steps that
  extract them from credential stores.
- Document rollback only when a safe, supported one is known. If an action is irreversible or
  recovery is unknown, say so and name the human decision or escalation needed.
- Never call an untested runbook validated, and never run production actions just to test it.

## Template

Keep only the sections that help this procedure. Do not fill sections with invented detail.

```markdown
# <Operation>

**Status:** Draft | Unverified | Verified
**Purpose:** <outcome and when to use it>
**Owner:** <verified owner or TBD>
**Last verified:** <date and evidence, or Not verified>

## Preconditions
- <access, tools, inputs, approvals>

## Safety and stop conditions
- <impact, boundaries, when NOT to proceed>

## Procedure
### 1. <Step>
<exact action or command, only if verified>

**Expected result:** <observable outcome>
**If it fails:** <safe next step, or stop and escalate>

## Verification
- <checks that prove completion>

## Recovery
<known recovery, or why none is documented>

## Escalation
<verified route and when to use it, or TBD>

## Sources and history
<links and dated validation notes>
```

## Review checklist

- Trigger and operator are clear.
- Prerequisites, permissions, inputs and approval gates are explicit.
- Steps are ordered and each has an observable expected result.
- Failure guidance says when to stop instead of improvising.
- Verified vs unverified is honest.
- Recovery and escalation are accurate or clearly marked unknown.
- No secrets, invented owners, unsupported claims, or side effects the user did not ask for.
