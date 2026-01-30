### Git

<details>
<summary>Difference between git fetch, merge, rebase  & pull.</code></summary><br><b>

`git fetch` is used to retrieve changes from a remote repository to your local repository without merging. It doesn't change your local working branch.

* It fetches the latest commits, branches, and tags from the remote repository but does not automatically integrate them into your local branch.

* It's a non-destructive operation and is often used to check for changes on the remote without affecting your local work.

`git merge` is used to integrate changes from one branch into another, creating a new merge commit.

* It creates a new commit that combines changes from the source branch into the destination branch.

* 

`git rebase` is used to integrate changes from one branch into another maintaining a linear history.

* It is typically used to keep your branch history linear and avoid unnecessary merge commits.

* It Rewrites commit history, providing a linear history without merge commits.

`git pull` is a combination of git fetch and git merge. It fetches changes from the remote repository and automatically merges them into your current branch.

* It's a convenient way to update your local branch with the latest changes from the remote, but it can introduce merge commits, especially if there are conflicting changes.

* By default, git pull performs a merge, but you can configure it to perform a rebase using the --rebase option.

</b></details>

<details>
<summary>What is a merge conflict in Git, and how do you resolve it?.</code></summary><br><b>

A merge conflict occurs when Git cannot automatically merge changes from different branches due to conflicting modifications in the same part of a file. To resolve it, you need to manually edit the conflicted files, choose which changes to keep, and then commit the resolution.

</b></details>

<details>
<summary>What are Git hooks, and how can they be useful in a Git workflow?.</code></summary><br><b>

Git hooks are scripts that run at specific points in the Git workflow, such as pre-commit or post-receive. They can be used to enforce coding standards, perform tests, and trigger automated processes.

</b></details>


<details>
<summary>What is a Git stash, and why would you use it?.</code></summary><br><b>

A Git stash is a temporary storage area for changes that are not ready to be committed but need to be saved for later. Developers use it to switch to a different branch or to temporarily set aside work in progress.

</b></details>

<details>
<summary>What is cherry-picking in git?.</code></summary><br><b>

`cherry-picking` refers to the process of selecting and applying a specific commit from one branch onto another branch. This allows you to pick a single commit and apply it to a different branch without merging the entire branch. Cherry-picking is useful when you want to selectively bring changes from one branch into another, perhaps to apply a bug fix or feature that exists in one branch but not in another.

```shell
git cherry-pick <commit-hash>
```

</b></details>