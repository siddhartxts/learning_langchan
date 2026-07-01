---
name: save
description: Safely save your Git work — stage, auto-write a Conventional Commit message, commit, and push the current branch. Use when the user says "save my work", "save", or runs /save.
tools: Bash
---

# Save

Stage, commit (with an auto-generated Conventional Commit message), and push the
current branch in one step — safely, without committing secrets/junk and without
rewriting history.

## Workflow

1. **Inspect the repo.** Run `git status --short`, `git branch --show-current`,
   and `git remote -v`.

2. **Clean tree → stop.** If `git status --short` prints nothing, tell the user
   the working tree is clean and do nothing else.

3. **Review the changes.** Run `git diff` to read the unstaged changes; note any
   untracked files from step 1.

4. **Screen for risky files** among the changed and untracked paths. Treat these
   as risky:
   - `.env` and `.env.*` (anything but `.env.example`)
   - files holding API keys, passwords, tokens, or other secrets
   - database dumps — `*.sql`, `*.dump`, `*.sqlite`, `*.db`
   - dependency / virtualenv dirs — `.venv`, `venv`, `node_modules`
   - caches / compiled junk — `__pycache__`, `*.pyc`
   - large generated/binary artifacts

5. **Stage.**
   - If **no** risky files: `git add .`.
   - If risky files **are** present: stage only the safe files explicitly with
     `git add <file>` (one per safe path) — **never** `git add .` in this case —
     and remember the skipped list to report later.

6. **Review staged changes.** Run `git diff --staged`.

7. **Generate a commit message** from the staged diff, in Conventional Commits
   format:

   ```
   type(scope): short subject

   - what changed
   - why (optional)
   ```

   - **type** — one of `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `test`.
   - **subject** — under 60 chars, imperative mood, no trailing period.
   - Only ask the user for a message if the changes are genuinely unclear.

8. **Commit.** `git commit -m "<message>"` (use multiple `-m` for the body).

9. **Push.** Run `git push`. If it fails because the branch has no upstream, run
   `git push -u origin <current-branch>`.

10. **Report.** Tell the user:
    - the **branch**,
    - the **commit message** used,
    - any **risky files skipped** (by name only),
    - whether the **push succeeded**.

## Rules

- **Never rewrite history.** Do not run `git commit --amend`, `git rebase`, or
  `git push --force` / `--force-with-lease`.
- **Never run destructive commands** — no `git reset --hard`, `git clean -fd`,
  `git checkout -- <file>`, or `git restore` that discards work.
- **Never echo a flagged secret's contents** — name the file only.
- Don't prompt for a commit message unless the diff is genuinely ambiguous.
