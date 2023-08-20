### Git

<details>
<summary>Difference between git fetch rebase  & pull.</code></summary><br><b>

`git fetch` is used to retrieve changes from a remote repository to your local repository. It doesn't change your local working branch.

* It fetches the latest commits, branches, and tags from the remote repository but does not automatically integrate them into your local branch.

* It's a non-destructive operation and is often used to check for changes on the remote without affecting your local work.

`git rebase` is used to integrate changes from one branch into another by moving or replaying the commits from your local branch on top of a different branch.

* It is typically used to keep your branch history linear and avoid unnecessary merge commits.

* It is helpful when you want to incorporate changes from the remote repository into your local branch and make it appear as if you had made your changes on top of the latest remote commits.

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