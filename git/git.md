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
