# Dependabot auto-merge policy

This repository uses a policy-gated workflow to enable GitHub auto-merge for narrowly scoped Dependabot updates.

## Policy

| Ecosystem | Patch | Minor | Major |
|---|---:|---:|---:|
| GitHub Actions | Automatic after required checks | Automatic after required checks | Manual review |
| Python (`pip`) | Automatic after required checks | Manual review | Manual review |

The workflow does not bypass branch protection or repository rulesets. It only enables auto-merge. GitHub performs the merge after every required review and status check succeeds.

## Required repository settings

1. Enable **Settings → General → Pull Requests → Allow auto-merge**.
2. Protect `main` through a branch protection rule or ruleset.
3. Require the `CTS / conformance` check.
4. Require the Pages `build` check where the workflow is triggered for the changed paths.
5. Do not grant GitHub Actions a ruleset bypass.

The Pages `deploy` job must not be required for pull requests because it intentionally runs only outside pull-request events.

## Authority and revocation

- **Authority:** the workflow has `contents: write` and `pull-requests: write` only.
- **Scope:** only pull requests authored by `dependabot[bot]` are evaluated.
- **Enforcement:** required checks and review rules remain the merge boundary.
- **Revocation:** disable or remove `dependabot-automerge.yml`, or turn off repository auto-merge.
- **Evidence:** workflow logs, Dependabot metadata, check runs, reviews, and merge commits provide the audit trail.

## Validation procedure

1. Open a Dependabot patch update and confirm auto-merge is enabled.
2. Confirm the pull request remains open while a required check is pending.
3. Confirm a failing required check blocks the merge.
4. Confirm a successful eligible update merges using a merge commit.
5. Confirm a major update remains open without auto-merge being enabled.
