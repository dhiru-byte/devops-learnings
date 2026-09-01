# Git

Interview notes for Git as it is used day to day in a DevOps workflow: moving
code between remote and local, integrating branches, undoing mistakes, and
enforcing checks before code reaches a pipeline.

## Contents

- [Fetch, pull, merge, and rebase](#fetch-vs-pull-vs-merge-vs-rebase)
- [Merge conflicts](#merge-conflicts)
- [Undoing changes](#undoing-changes-reset-vs-revert-vs-restore)
- [Recovering with reflog](#recovering-lost-work-with-reflog)
- [Stash](#stash)
- [Cherry-pick](#cherry-pick)
- [Hooks](#hooks)
- [Tags and releases](#tags-and-releases)
- [Git in CI/CD](#git-in-a-cicd-pipeline)
- [Inspecting and bisecting history](#inspecting-and-bisecting-history)

## fetch vs pull vs merge vs rebase

`fetch` downloads remote commits without touching your working tree. `pull` is
`fetch` plus an integration step (`merge` by default). `merge` joins two
branches with a merge commit. `rebase` replays your commits on top of another
branch and produces a linear history.

| Command | Contacts remote | Changes working tree | History result | Risk |
| :--- | :---: | :---: | :--- | :--- |
| `fetch` | Yes | No | Unchanged | Safe |
| `pull` | Yes | Yes | Merge or rebase, depending on config | Moderate |
| `merge` | No | Yes | Non-linear, extra merge commit | Low |
| `rebase` | No | Yes | Linear, commits get new hashes | High, rewrites history |

Practical detail:

- `fetch` only updates remote-tracking refs such as `origin/main`. Inspect the
  result with `git log origin/main` or `git diff HEAD origin/main` before you
  integrate anything.
- `git pull --rebase` avoids the "Merge branch 'main' into ..." commits that
  clutter a feature branch. Set it as the default with
  `git config --global pull.rebase true`.
- Rebase only a branch that nobody else has based work on. Rewriting a shared
  branch forces every other contributor to recover their local copy by hand.
- After a rebase of an already-pushed branch, publish with
  `git push --force-with-lease`, never plain `--force`. `--force-with-lease`
  refuses the push if someone else added commits you have not seen.

Typical feature-branch flow:

```bash
git fetch origin
git rebase origin/main
# resolve conflicts, then continue
git rebase --continue
git push --force-with-lease origin feature-branch
```

## Merge conflicts

A conflict happens when two branches change the same region of a file, or when
one side edits a file the other side deleted, and Git cannot decide which
version to keep. You resolve it by editing the file to the intended final
state, staging it, and completing the merge or rebase.

```bash
git status                 # list conflicted paths
git diff                   # show the conflicting hunks
git checkout --ours  file  # keep the current branch version
git checkout --theirs file # keep the incoming version
git add file               # mark as resolved
git merge --continue       # or: git rebase --continue
git merge --abort          # or: git rebase --abort, to start over
```

Practical detail:

- Conflict markers are `<<<<<<<` (current branch), `=======`, `>>>>>>>`
  (incoming branch). Never commit a file that still contains them; add a
  pipeline grep for these markers as a cheap safety net.
- During a **rebase**, "ours" and "theirs" are inverted relative to a merge:
  "ours" is the branch you are replaying onto, "theirs" is your own commit.
- `git rerere` (`git config --global rerere.enabled true`) records how you
  resolved a conflict and replays that resolution when the same conflict
  reappears, which is common on long-lived branches.
- Reduce conflict frequency by rebasing small branches often instead of
  integrating a large branch once.

## Undoing changes: reset vs revert vs restore

Pick based on whether the commit is already published.

| Goal | Command | Effect |
| :--- | :--- | :--- |
| Unstage a file, keep edits | `git restore --staged file` | Index only |
| Discard local edits to a file | `git restore file` | Working tree only, destructive |
| Drop last commit, keep changes staged | `git reset --soft HEAD~1` | Moves branch pointer |
| Drop last commit, keep changes unstaged | `git reset HEAD~1` | Mixed reset, the default |
| Drop last commit and its changes | `git reset --hard HEAD~1` | Destructive |
| Undo a published commit | `git revert <hash>` | Adds a new inverse commit |

Use `reset` only on commits that exist just locally. Use `revert` on anything
already pushed to a shared branch, because it undoes the change without
rewriting history that others have pulled.

## Recovering lost work with reflog

`git reflog` lists every position `HEAD` has held, including commits that no
branch points to any more. It is the recovery path after a bad
`reset --hard`, a botched rebase, or a deleted branch.

```bash
git reflog                       # find the hash you want back
git reset --hard <hash>          # restore the branch to that state
git branch recovered <hash>      # or recover it as a new branch
```

Reflog entries are local and expire (90 days by default for reachable
entries), so recover promptly.

## Stash

`git stash` shelves uncommitted work so you can switch context, then reapply it
later. It is local only and never pushed.

| Action | Command |
| :--- | :--- |
| Stash tracked changes | `git stash` |
| Stash with a label | `git stash push -m "wip: retry logic"` |
| Include untracked files | `git stash -u` |
| List stashes | `git stash list` |
| Apply and delete the entry | `git stash pop` |
| Apply and keep the entry | `git stash apply` |
| Show the contents as a diff | `git stash show -p stash@{0}` |
| Delete one entry | `git stash drop stash@{0}` |
| Delete all entries | `git stash clear` |

Practical detail:

- Common triggers: an urgent hotfix arrives mid-feature, `git pull` refuses to
  run because local changes would be overwritten, or you notice you have been
  committing on the wrong branch.
- Always label stashes with `push -m`. An unlabeled stack of five entries is
  guaranteed to produce a wrong `pop` eventually.
- A stash can be popped onto a different branch, which is the simplest way to
  move uncommitted work you started in the wrong place.
- If the target branch has moved far ahead and `pop` would conflict heavily,
  use `git stash branch <new-branch> stash@{0}`. It creates a branch at the
  commit the stash was made from and applies the stash there cleanly.

Stash versus commit: a stash is a local stack entry, invisible to `git log`,
not pushable, and applicable to any branch. A commit is permanent branch
history, shareable, and tied to its branch.

## Cherry-pick

`git cherry-pick <hash>` copies the change introduced by one commit onto the
current branch as a new commit with a new hash.

| Action | Command |
| :--- | :--- |
| One commit | `git cherry-pick <hash>` |
| Several commits | `git cherry-pick <hash1> <hash2>` |
| A range, excluding A | `git cherry-pick A..B` |
| A range, including A | `git cherry-pick A^..B` |
| Stop and unwind | `git cherry-pick --abort` |

Practical detail:

- The new hash means the same logical change now exists twice in the graph. A
  later merge of the source branch can therefore conflict.
- `git cherry-pick -x <hash>` appends "(cherry picked from commit ...)" to the
  message, which is how release branches stay auditable.
- Main use is porting a verified fix from a development branch to a release or
  hotfix branch without dragging along unfinished features. If you are picking
  ten commits from one branch, merge or rebase instead.

## Hooks

Git hooks are executable scripts in `.git/hooks` that Git runs at defined
points in the commit and receive lifecycle. They are the first place to enforce
standards, before anything reaches CI.

| Hook | Runs | Typical use |
| :--- | :--- | :--- |
| `pre-commit` | Before the commit message is requested | Lint, format, secret scan |
| `prepare-commit-msg` | Before the editor opens | Insert ticket ID from branch name |
| `commit-msg` | After the message is written | Enforce message convention |
| `pre-push` | Before objects are sent | Run fast unit tests |
| `pre-receive` / `update` | On the server, before refs update | Reject force-push, enforce policy |
| `post-receive` | On the server, after refs update | Trigger a pipeline or notification |

Practical detail:

- Client-side hooks live in `.git/hooks`, are not cloned, and can be bypassed
  with `--no-verify`. Treat them as a convenience for developers, not a
  control. Anything that must hold has to be enforced by a server-side hook or
  by a required CI check.
- Share hooks across a team with `git config core.hooksPath <dir>` and a
  tracked directory, or with a manager such as `pre-commit`.
- Keep client hooks fast. A `pre-commit` hook that takes 30 seconds gets
  disabled by the team within a week.

## Tags and releases

A tag is a fixed name for a commit; it is what a release pipeline should build
from, because branches move and tags do not.

```bash
git tag -a v1.4.0 -m "Release 1.4.0"   # annotated tag: has author, date, message
git push origin v1.4.0                  # tags are not pushed by git push alone
git tag -l 'v1.*'                       # list matching tags
git describe --tags                     # nearest tag plus commits since, useful for build IDs
```

Prefer annotated tags (`-a`) over lightweight tags for releases: they are real
objects, can be signed with `-s`, and carry who tagged what and when.

## Git in a CI/CD pipeline

Git events are the triggers for the pipeline, and the Git metadata is what
makes a build traceable. The pipeline's smoke and regression test roles are
covered in [Docker CI/CD](docker-interview-guide.md#docker-in-cicd); Git's job is to
trigger those checks and identify exactly which source revision they tested.

- **Trigger mapping:** a push to a feature branch runs build plus fast tests; a
  pull request runs the full validation set and is a required gate for merge; a
  push of a version tag runs the release and deployment job.
- **Immutable build identity:** tag every artifact and container image with the
  commit SHA, not with `latest`. Given a running version you can then get back
  to the exact source with `git show <sha>`.
- **Shallow clones:** CI runners should use `git clone --depth 1` or the
  equivalent runner setting to cut checkout time, but a job that needs
  `git describe` or a diff against the base branch needs more history.
- **Protected branches:** enforce no direct pushes to `main`, require review and
  passing checks, and require the branch to be up to date so the merge result
  is the state that was actually tested.
- **Merge strategy:** squash merges give `main` one commit per change, which
  makes `git bisect` and `git revert` straightforward at the cost of losing
  intermediate commits.
- **Secrets:** a secret committed once stays in history even after it is
  deleted in a later commit. Rotate the credential first, then scrub history
  with a tool such as `git filter-repo`, and add a secret scanner to
  `pre-commit` and to CI.

## Inspecting and bisecting history

```bash
git log --oneline --graph --decorate --all   # readable topology
git log -S "functionName"                    # commits that changed an occurrence count of a string
git blame -L 40,60 path/to/file              # who last touched these lines and in which commit
git bisect start
git bisect bad                               # current commit is broken
git bisect good v1.3.0                       # this tag was fine
# git checks out midpoints; mark each with git bisect good/bad
git bisect reset
```

`git bisect` performs a binary search over history, so it finds the commit that
introduced a regression in about log2(n) steps. With a scripted test you can
automate it fully using `git bisect run <command>`.
