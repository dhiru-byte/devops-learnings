### Git

<details>
<summary>Difference between git fetch, merge, rebase  & pull.</code></summary><br><b>

In a collaborative DevOps environment, navigating how code moves from the **Remote (GitHub/GitLab)** to your **Local Workspace** is a fundamental skill.

### 🔍 Git Fetch (The "Safe" Update)
`git fetch` downloads all new commits from the remote repository but **does not change your local files**.
*   **What it does:** Updates your remote-tracking branches (e.g., `origin/main`).
*   **Analogy:** Checking your mailbox to see what's inside without actually opening the letters.
*   **Use Case:** Use this to see what your teammates have done without risking merge conflicts in your current work.

### 🚀 Git Pull (The "Shortcut")
`git pull` is a combination of `git fetch` followed by `git merge`.
*   **What it does:** Downloads changes and immediately tries to integrate them into your current branch.
*   **Risk:** It can create "Merge Commits" automatically, which clutter the history if done frequently.

### 🤝 Git Merge (The "Join")
`git merge` combines two branches together.
*   **What it does:** It creates a new **Merge Commit** that has two parent commits.
*   **History:** It results in a non-linear, "diamond-shaped" history.
*   **Best For:** Merging a completed feature branch back into `main`.

### ⚡ Git Rebase (The "Rewrite")
`git rebase` takes your local commits and "replays" them on top of the latest remote commits.
*   **What it does:** It rewrites history to make it look like you started your work on the very latest version of the code.
*   **History:** It results in a **Linear History** (a straight line).
*   **Best For:** Keeping your feature branch up-to-date with `main` before merging.

## 📊 Comparison Matrix

| Command | Downloads Data? | Changes Local Files? | History Result | Risk Level |
| :--- | :---: | :---: | :--- | :--- |
| **`fetch`** | ✅ Yes | ❌ No | No Change | **Safe** |
| **`pull`** | ✅ Yes | ✅ Yes | Combined | Moderate |
| **`merge`** | ❌ No | ✅ Yes | Non-Linear | Low |
| **`rebase`** | ❌ No | ✅ Yes | **Linear** | **High** (Rewrites History) |

## 💡

1. **The Rebase Rule:** "I never **rebase** a public branch that others are working on. I only rebase my private feature branch to keep the history clean before a [Pull Request](https://docs.github.com)."
2. **Linear History:** "To maintain a professional, readable Git log, I prefer `git pull --rebase` over a standard `git pull`. This avoids unnecessary 'Merge branch...' commits."
3. **Safety First:** "When I'm unsure of the changes my team has made, I always start with a **fetch**. It allows me to use `git diff` or `git log origin/main` to inspect the code before integrating it."

## 🛠️ Typical Workflow Scenario
1. `git fetch origin` (Check for updates)
2. `git rebase origin/main` (Put my work on top of the newest code)
3. *Fix any conflicts*
4. `git push origin feature-branch` (Upload clean, linear work)
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

`git stash` is a powerful tool used to temporarily "shelve" (or archive) changes you've made to your working directory so you can work on something else, then come back and re-apply them later.

## 🚀 1. Common Scenarios
*   **The Urgent Hotfix:** You are mid-feature on `develop` when a critical bug hits `main`. You stash your current work, switch to `main`, fix the bug, then return to `develop` and pop your stash.
*   **The "Dirty" Pull:** You try to `git pull` but Git refuses because your local changes would be overwritten. You stash, pull, and then pop to resolve any conflicts.
*   **Wrong Branch:** You realize you've been coding on the `main` branch for 20 minutes by mistake. Stash your changes, switch to a new feature branch, and pop them there.

## 🛠️ 2. Essential Commands

| Action | Command |
| :--- | :--- |
| **Stash everything** | `git stash` |
| **Stash with a message** | `git stash push -m "descriptive message"` |
| **Include new (untracked) files** | `git stash -u` |
| **List all stashes** | `git stash list` |
| **Apply last stash & delete it** | `git stash pop` |
| **Apply last stash & keep it** | `git stash apply` |
| **View stash contents** | `git stash show -p stash@{0}` |
| **Delete a specific stash** | `git stash drop stash@{0}` |
| **Clear all stashes** | `git stash clear` |

## 📊 3. Stash vs. Commit

| Feature | `git stash` | `git commit` |
| :--- | :--- | :--- |
| **Storage** | Local-only "Stack". | Permanent part of Branch history. |
| **Pushable?** | No, stays on your machine. | Yes, can be shared with the team. |
| **Flexibility** | Can be "popped" onto any branch. | Tied to the specific branch. |
| **Visibility** | Hidden from `git log`. | Visible in project history. |

## 💡

1. **On Context Switching:** "I use **git stash** as my primary tool for context switching. It allows me to handle production emergencies without cluttering our Git history with 'Work in Progress' (WIP) commits."
2. **On Safety:** "I always prefer `git stash push -m` over a plain `git stash`. When working on multiple bug fixes, having a labeled stash list ensures I don't accidentally apply the wrong logic to the wrong branch."
3. **On Portability:** "A great trick I use is stashing changes on one branch and popping them onto another. It’s the easiest way to move uncommitted work when I realize I've started coding in the wrong place."

### ⚠️ Pro-Tip: The "Stash to Branch" Move
If you have a large stash and your current branch has changed so much that `git stash pop` causes massive conflicts, use:

git stash branch <new-branch-name> stash@{0}

</b></details>

<details>
<summary>What is cherry-picking in git?.</code></summary><br><b>

`git cherry-pick` allows you to pick specific commits from one branch and apply them to another. It is a powerful tool for hotfixes and selective feature migration.

### 📍 Key Commands
| Action | Command |
| :--- | :--- |
| **Apply one commit** | `git cherry-pick <hash>` |
| **Apply multiple** | `git cherry-pick <hash1> <hash2>` |
| **Apply range** | `git cherry-pick A..B` |
| **Abort process** | `git cherry-pick --abort` |

### ⚠️ Important Best Practices
*   **New Hashes:** Cherry-picking creates a **new commit** with a new hash on your current branch, even though the content is the same as the source.
*   **Avoid Overuse:** If you find yourself cherry-picking 10+ commits from the same branch, a **merge** or **rebase** is likely a better architectural choice.
*   **Traceability:** Use `git cherry-pick -x <hash>` to append a line to the commit message saying "(cherry picked from commit...)", which helps teams track the origin of the change.

### 💡
"I use **cherry-pick** primarily for porting critical bug fixes across branches. It allows us to maintain a clean production branch by only pulling in verified fixes without merging unstable features from the development branch."
</b></details>

<details>
<summary>💨 Smoke Testing VS Regression Testing?.</code></summary><br><b>

# 🧪 Smoke Testing vs. Regression Testing

In a robust CI/CD pipeline, different types of tests are used at different stages to ensure both **speed** and **stability**.

## 📊 Quick Comparison Matrix

| Feature | Smoke Testing | Regression Testing |
| :--- | :--- | :--- |
| **Objective** | Verify if the build is **stable**. | Verify if the build is **correct**. |
| **Scope** | Core/Critical features only. | Comprehensive (New + Old features). |
| **Depth** | Shallow (Surface-level). | Deep (Detailed scenarios). |
| **Execution Time** | Very Fast (Minutes). | Slower (Hours/Days). |
| **Automation** | Always Automated. | Frequently Automated (but can be manual). |
| **Outcome** | Go / No-Go to further testing. | Verification of code quality. |

## 💨 1. Smoke Testing (The "Stable?" Test)
Also known as **Build Verification Testing (BVT)**. It is a non-exhaustive suite that ensures the most crucial functions of an application work.

*   **When to run:** Immediately after a new build is deployed to an environment (Dev, QA, or Staging).
*   **The Analogy:** If you turn on a new machine and see "smoke," you turn it off immediately. You don't bother checking the settings.
*   **Production Example (E-commerce):** 
    1. Does the app launch? 
    2. Can a user log in? 
    3. Can a user reach the checkout page?

## 🔄 2. Regression Testing (The "Broken?" Test)
The process of testing an application after a code change to ensure that the **existing functionality** still works as expected.

*   **When to run:** After bug fixes, feature additions, or configuration changes.
*   **The Focus:** Ensuring that a fix in "Module A" didn't accidentally break a feature in "Module B."
*   **Production Example (E-commerce):** 
    1. Checking all payment gateways (Credit Card, PayPal, Stripe).
    2. Verifying tax calculations for all 50 states.
    3. Testing "Forgot Password" email delivery across all browsers.

## 🛠️ DevOps Implementation Pattern

In a modern [GitHub Actions](https://github.com) or [Jenkins](https://www.jenkins.io) pipeline:

1.  **Code Commit** ➡️ Build Container.
2.  **Unit Tests** ➡️ Verify logic.
3.  **Deployment** ➡️ Deploy to Staging.
4.  **Smoke Tests** ➡️ **(Gatekeeper)** If this fails, abort everything.
5.  **Regression Tests** ➡️ Run the full suite for 1-2 hours.
6.  **Production Deployment** ➡️ Final rollout.

## 💡 Interview "Gold Lines"

*   **On ROI:** "Smoke testing provides the highest ROI in CI/CD. It catches major 'showstopper' bugs in minutes, preventing the QA team or the automated regression suite from wasting hours on a fundamentally broken build."
*   **On Scope:** "I view Smoke Testing as the **Happy Path** check, whereas Regression Testing is the **Edge Case** check."
*   **On Confidence:** "Regression testing is what gives us the confidence to refactor code or update dependencies like the Linux Kernel or Kubernetes versions."
</b></details>
