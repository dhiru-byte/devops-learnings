# Git

Pointer-style interview notes for Git in a DevOps workflow.

- **Owns:** history workflows — integrating branches, rewriting safely, undoing,
  recovering. OS and shell fundamentals: [Linux guide](linux-interview-guide.md);
  container and pipeline artifact behaviour: [Docker guide](docker-interview-guide.md).
- **Safety rule for everything below:** rewrite only your own unmerged feature
  branch; never rebase, squash, or force-push `main`, `master`, `develop`,
  `release`, or any shared branch.

## Contents

- **Integrating and rewriting:** [fetch vs pull vs merge vs rebase](#fetch-vs-pull-vs-merge-vs-rebase) ·
  [Merge conflicts](#merge-conflicts) · [Rebase, squash, and force-with-lease](#rebase-squash-and-force-with-lease)
- **Undoing and recovering:** [Undoing changes](#undoing-changes-reset-vs-revert-vs-restore) ·
  [Reflog recovery](#recovering-lost-work-with-reflog) · [Stash](#stash) · [Cherry-pick](#cherry-pick)
- **Delivery:** [Hooks](#hooks) · [Tags and releases](#tags-and-releases) ·
  [Git in a CI/CD pipeline](#git-in-a-cicd-pipeline) ·
  [Inspecting and bisecting history](#inspecting-and-bisecting-history) ·
  [Troubleshooting scenarios](#troubleshooting-scenarios)

## fetch vs pull vs merge vs rebase

**Docs:** [`git-fetch`](https://git-scm.com/docs/git-fetch) ·
[`git-pull`](https://git-scm.com/docs/git-pull) ·
[`git-merge`](https://git-scm.com/docs/git-merge)

| Command | Contacts remote | Changes working tree | History result | Risk |
| :--- | :---: | :---: | :--- | :--- |
| `fetch` | Yes | No | Unchanged; only remote-tracking refs move | Safe |
| `pull` | Yes | Yes | Merge or rebase, depending on config | Moderate |
| `merge` | No | Yes | Non-linear, extra merge commit | Low |
| `rebase` | No | Yes | Linear, commits get **new hashes** | High, rewrites history |

```bash
git fetch origin                       # only updates origin/main and friends
git log origin/main; git diff HEAD origin/main   # inspect before integrating
git config --global pull.rebase true   # make pull rebase, avoiding merge noise

git rebase origin/main                 # typical feature-branch flow
# resolve conflicts, git add <file>, then git rebase --continue
git push --force-with-lease origin feature-branch
```

**Gotchas**

- Rebase only a branch nobody else has based work on; rewriting a shared branch
  forces every other contributor to recover their local copy by hand.
- After rebasing an already-pushed branch, publish with
  `git push --force-with-lease`, never plain `--force`.

## Merge conflicts

**Docs:** [`git-merge` conflict handling](https://git-scm.com/docs/git-merge#_how_conflicts_are_presented) ·
[`git-rerere`](https://git-scm.com/docs/git-rerere)

- **Cause:** two branches change the same region, or one side edits a file the
  other deleted.
- **Resolve:** edit the file to the intended final state, stage it, continue.
- **Markers:** `<<<<<<<` starts the current branch's version, `=======` divides,
  `>>>>>>>` ends the incoming version.

```bash
git status                 # list conflicted paths
git diff                   # show the conflicting hunks
git checkout --ours  file  # keep the current branch version
git checkout --theirs file # keep the incoming version
git add file               # mark as resolved
git merge --continue       # or: git rebase --continue
git merge --abort          # or: git rebase --abort, to start over
git config --global rerere.enabled true   # replay recorded resolutions
```

**Gotchas**

- During a **rebase**, "ours" and "theirs" are inverted relative to a merge:
  "ours" is the base you are replaying onto (`origin/main`), "theirs" is your
  own commit. This is the usual interview trap.
- Never commit a file still containing conflict markers; a pipeline grep is a
  cheap safety net.
- Rebase small branches often rather than one large branch late, and never start
  a second rewrite inside an in-progress rebase — finish or abort first.

## Rebase, squash, and force-with-lease

**Docs:** [`git-rebase`](https://git-scm.com/docs/git-rebase) ·
[`git-reset`](https://git-scm.com/docs/git-reset) ·
[`git-push`](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt)

Goal: a branch on the latest base, with one reviewable commit, that merges
without surprises. Rebase updates the branch, squash removes noise,
`--force-with-lease` publishes a rewrite without clobbering others' work.

| Situation | Use | Do not |
| :--- | :--- | :--- |
| Feature branch is behind `main` | `git fetch` then `git rebase origin/main` | Merge `main` into the feature branch |
| Five "wip / fix / typo" commits before a PR | Squash to one commit | Leave the noise on `main` |
| You rebased a branch you already pushed | `git push --force-with-lease` | `git push --force` |
| The commit is already on `main`, or reviewers cited its hash | New commit, `git revert`, or squash at merge time | Rebase, squash, or force-push it |

Non-interactive squash onto the latest base (safe in scripts):

```bash
git fetch origin
git switch feature-branch
git rebase origin/main          # first sit on the latest base
git reset --soft origin/main    # keep all file changes, drop the extra commits
git status                      # confirm what goes into the one commit
git commit -m "Retry image pulls when the registry token expires."
git push --force-with-lease origin feature-branch
```

- `reset --soft` moves the branch pointer, leaving index and working tree as the
  combined result: the next commit is the whole feature as one snapshot.
- `git rebase -i origin/main` (`pick` the first, `squash` the rest) does the same
  but needs an interactive editor, a poor fit for automation.
- Host-side "squash and merge" keeps `main` linear while preserving branch commits.

| Option | What it checks | Use |
| :--- | :--- | :--- |
| `--force-with-lease` | Remote still points at the commit **you last fetched** | Default for your own rewritten branch |
| `--force-with-lease=refs/heads/br:<hash>` | Remote still points at a specific hash | Extra-precise with several remotes |
| `--force` | Nothing | Almost never; overwrites commits you have not seen |

**Gotchas**

- If the lease fails (`! [rejected] ... (stale info)`), **do not retry with
  `--force`.** Fetch, inspect `git log origin/feature-branch`, integrate their
  commits, then push with lease again. Never force-push a protected branch.
- Do not squash merge commits from `main` into your branch (rebase instead),
  commits already on a shared branch, or a mix of unrelated features.
- After `git rebase --abort`, the pre-rebase tip is still in
  [reflog](#recovering-lost-work-with-reflog).

## Undoing changes: reset vs revert vs restore

**Docs:** [`git-reset`](https://git-scm.com/docs/git-reset) ·
[`git-revert`](https://git-scm.com/docs/git-revert) ·
[`git-restore`](https://git-scm.com/docs/git-restore) — pick by whether published.

| Goal | Command | Effect |
| :--- | :--- | :--- |
| Unstage a file, keep edits | `git restore --staged file` | Index only |
| Discard local edits to a file | `git restore file` | DESTRUCTIVE, working tree only |
| Drop last commit, keep changes staged | `git reset --soft HEAD~1` | Moves branch pointer |
| Drop last commit, keep changes unstaged | `git reset HEAD~1` | Mixed reset, the default |
| Drop last commit and its changes | `git reset --hard HEAD~1` | DESTRUCTIVE |
| Undo a published commit | `git revert <hash>` | Adds a new inverse commit |

**Gotchas.** Use `reset` only on commits that exist locally. Use `revert` on
anything already pushed to a shared branch, because it undoes the change without
rewriting history others have pulled.

## Recovering lost work with reflog

**Docs:** [`git-reflog`](https://git-scm.com/docs/git-reflog)

`git reflog` lists every position `HEAD` has held, including commits no branch
points to — the recovery path after a bad `reset --hard`, botched rebase, or
deleted branch.

```bash
git reflog                       # find the hash you want back
git branch recovered <hash>      # safest: recover as a new branch
git reset --hard <hash>          # or restore the current branch to that state
```

**Gotchas.** Reflog entries are **local only** and expire (90 days by default),
so recover promptly, and prefer creating a branch over `reset --hard` so you
keep the current state while investigating.

## Stash

**Docs:** [`git-stash`](https://git-scm.com/docs/git-stash)

`git stash` shelves uncommitted work so you can switch context. It is local
only and never pushed.

| Action | Command |
| :--- | :--- |
| Stash with a label / include untracked | `git stash push -m "wip: retry"` / `git stash -u` |
| List / show as a diff | `git stash list` / `git stash show -p stash@{0}` |
| Apply and delete / apply and keep | `git stash pop` / `git stash apply` |
| Delete one / delete all | `git stash drop stash@{0}` / `git stash clear` |
| Apply onto a fresh branch | `git stash branch <new-branch> stash@{0}` |

- **Triggers:** urgent hotfix mid-feature, `git pull` refusing to run because
  local changes would be overwritten, or work started on the wrong branch — a
  stash pops onto any branch.
- **Versus a commit:** a stash is a local stack entry, invisible to `git log` and
  not pushable.

**Gotchas**

- Always label with `push -m`; an unlabelled stack of five entries guarantees a wrong `pop` eventually.
- If the target branch has moved far ahead and `pop` would conflict heavily, use `git stash branch`, which recreates the branch at the commit the stash was made from.

## Cherry-pick

**Docs:** [`git-cherry-pick`](https://git-scm.com/docs/git-cherry-pick)

`git cherry-pick <hash>` copies the change from one commit onto the current
branch as a **new commit with a new hash**.

| Action | Command |
| :--- | :--- |
| One or several commits | `git cherry-pick <hash1> <hash2>` |
| A range, excluding / including A | `git cherry-pick A..B` / `git cherry-pick A^..B` |
| Record provenance in the message | `git cherry-pick -x <hash>` |
| Stop and unwind | `git cherry-pick --abort` |

Main use: porting a verified fix to a release or hotfix branch without dragging
along unfinished features; `-x` appends "(cherry picked from commit ...)", which
keeps release branches auditable.

**Gotchas.** The new hash means the same logical change exists twice in the
graph, so a later merge of the source branch can conflict. Picking ten commits
from one branch means you should merge or rebase instead.

## Hooks

**Docs:** [`githooks`](https://git-scm.com/docs/githooks)

Executable scripts Git runs at defined points in the commit and receive
lifecycle — the first place to enforce standards, before CI.

| Hook | Runs | Typical use |
| :--- | :--- | :--- |
| `pre-commit` | Before the message is requested | Lint, format, secret scan |
| `prepare-commit-msg` | Before the editor opens | Insert ticket ID from branch name |
| `commit-msg` | After the message is written | Enforce message convention |
| `pre-push` | Before objects are sent | Run fast unit tests |
| `pre-receive` / `update` | Server-side, before refs update | Reject force-push, enforce policy |
| `post-receive` | Server-side, after refs update | Trigger a pipeline or notification |

**Gotchas**

- Client-side hooks live in `.git/hooks`, are **not cloned**, and can be bypassed with `--no-verify`: developer convenience only, so anything that must hold needs a server-side hook or a required CI check.
- Share them via `core.hooksPath` and a tracked directory, or a manager such as `pre-commit`; keep them fast, since a 30-second hook gets disabled within a week.

## Tags and releases

**Docs:** [`git-tag`](https://git-scm.com/docs/git-tag) ·
[`git-describe`](https://git-scm.com/docs/git-describe)

A tag is a fixed name for a commit and what a release pipeline should build
from, because branches move and tags do not.

```bash
git tag -a v1.4.0 -m "Release 1.4.0"   # annotated: author, date, message; -s signs
git push origin v1.4.0                 # tags are NOT pushed by git push alone
git tag -l 'v1.*'                      # list matching tags
git describe --tags                    # nearest tag plus commits since (build IDs)
```

**Gotchas.** Prefer annotated tags over lightweight ones for releases: they are
real objects, can be signed, and record who tagged what and when. Plain
`git push` does not publish tags.

## Git in a CI/CD pipeline

**Docs:** [`git-clone` (`--depth`)](https://git-scm.com/docs/git-clone) ·
[`git-filter-repo`](https://github.com/newren/git-filter-repo)

Git events trigger the pipeline and Git metadata makes a build traceable; the
build, scan, smoke, and regression stages are in
[Docker CI/CD](docker-interview-guide.md#docker-in-cicd).

| Concern | Practice |
| :--- | :--- |
| Trigger mapping | Feature-branch push = build plus fast tests; PR = full validation as a required gate; version tag = release and deploy |
| Immutable build identity | Tag every artifact and image with the commit SHA, never `latest`, so `git show <sha>` gets you back to the exact source |
| Checkout speed | `git clone --depth 1`, but jobs needing `git describe` or a base-branch diff need more history |
| Protected branches | No direct pushes to `main`; require review, passing checks, and up-to-date branches so the merge result is what was tested |
| Merge strategy | Squash merges give `main` one commit per change, keeping `git bisect` and `git revert` simple, at the cost of intermediate commits |

**Gotchas**

- A secret committed once **stays in history** even after a later commit deletes it: rotate the credential first, scrub history with `git filter-repo`, then add a secret scanner to `pre-commit` and CI.
- Rewriting a shared repository's history requires coordination: every clone must be re-cloned or reset.

## Inspecting and bisecting history

**Docs:** [`git-log`](https://git-scm.com/docs/git-log) ·
[`git-blame`](https://git-scm.com/docs/git-blame) ·
[`git-bisect`](https://git-scm.com/docs/git-bisect)

```bash
git log --oneline --graph --decorate --all   # readable topology
git log -S "functionName"                    # commits changing that string's count
git blame -L 40,60 path/to/file              # who last touched these lines

git bisect start; git bisect bad; git bisect good v1.3.0
git bisect run ./test.sh      # or mark each midpoint with bisect good/bad
git bisect reset              # always finish with this
```

`git bisect` binary-searches history, finding the offending commit in about
log2(n) steps.

## Troubleshooting scenarios

Fixed template: **Symptom -> Check -> Cause -> Fix -> Prevent.**

### 1. Push rejected, or the lease fails after a rebase

- **Symptom:** `! [rejected] ... (fetch first)`, or `--force-with-lease` fails
  with "stale info".
- **Check:** `git fetch origin && git log --oneline HEAD..origin/<branch>`.
- **Cause:** the remote has commits you never fetched. On a rewritten branch the
  lease is doing exactly its job.
- **Fix:** integrate first (`git pull --rebase`), then push — with lease if the
  branch was rewritten. **Never** escalate to `--force`.
- **Prevent:** fetch before starting work, enable `pull.rebase`, and coordinate
  before rewriting a branch someone else uses. See
  [Rebase, squash, and force-with-lease](#rebase-squash-and-force-with-lease).

### 2. Commits vanished after `reset --hard`

- **Symptom:** work is missing and `git log` does not show it.
- **Check:** `git reflog` and `git fsck --lost-found`.
- **Cause:** the branch pointer moved; the commits are unreferenced, not gone.
- **Fix:** `git branch recovered <hash>` from the reflog entry, then verify
  before deleting anything.
- **Prevent:** commit or `git stash push -m` before any `reset --hard`; recover
  within the reflog expiry window.

### 3. A secret was committed

- **Symptom:** a scanner or review finds a credential in the repository.
- **Check:** `git log -S "<fragment>" --all`; confirm whether the commit was
  pushed.
- **Cause:** the secret stays in history, readable after a later deletion.
- **Fix:** **rotate the credential first**, treating it as compromised, then
  rewrite history with `git filter-repo` and coordinate re-clones.
- **Prevent:** secret scanning in `pre-commit` and CI; keep credentials in a
  secrets manager. See [Git in a CI/CD pipeline](#git-in-a-cicd-pipeline).
