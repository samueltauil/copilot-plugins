# Step anatomy

Every step file follows the same rhythm, so learners always know where they are. Each part exists for a learning
reason; keep the reason in mind when you write it.

| Part | Markdown | Purpose | Principle |
| --- | --- | --- | --- |
| Heading | `## Step N: <outcome title>` | Orientation and progress | Signaling, progress |
| Story hook | 1–3 sentences | Raise the one question this step answers; connect to the last step | Curiosity, activation |
| Theory | `### 📖 Theory: <concept>` | Just enough concept for the activity | Cognitive load, pre-training |
| Activity | `### ⌨️ Activity: <verb + object>` (or `Activity 1`, `Activity 2`) | Practice one concept on real GitHub | Application, segmenting |
| Confirmation cues | "You should now see ..." | Let learners verify progress themselves | Feed up, cognitive walkthrough |
| Triggering action + Mona line | Last instruction | Make the feedback loop explicit | Honest status |
| Having trouble? 🤷 | `<details>` after each activity | Recover from the likely mistakes | Scaffolding, error management |

## Worked example (step 1, full support)

````markdown
## Step 1: Start your feature branch

Your team never edits `main` directly, so before you change anything you need a safe place to work. How do you
get one in a few clicks?

### 📖 Theory: What is a branch?

A [branch](https://docs.github.com/get-started/using-git/about-branches) is a parallel version of your
repository. Changes on a branch stay separate from `main` until you choose to merge them with a pull request.

| | `main` | Your feature branch |
| --- | --- | --- |
| Who uses it | Everyone | You, while you work |
| Safe to experiment? | No | Yes |

### ⌨️ Activity: Create the `add-docs` branch

1. In a new browser tab, open your repository: [https://github.com/{{ full_repo_name }}](https://github.com/{{ full_repo_name }}).

1. Above the file list, on the left, click the branch selector that shows **main**.

1. In the **Find or create a branch** box, type `add-docs`, then click **Create branch add-docs from main**.

   <img width="300" alt="Branch selector menu with add-docs typed and the Create branch option highlighted" src="../images/create-branch.png" />

1. Check the branch selector: it now shows **add-docs**. That is your safe place to work.

1. Wait a moment for Mona to check your work, provide feedback, and share the next lesson.

<details>
<summary>Having trouble? 🤷</summary><br/>

- **No "Create branch" option?** The name may already exist. Type it exactly as `add-docs`, all lowercase.
- **No reply from Mona after two minutes?** Open the **Actions** tab and look for a **Step 1** run. If none
  started, make sure the branch is named exactly `add-docs`.

</details>
````

Why it works: one concept, a table that contrasts the two cases, a direct link to the learner's own repository
through `{{ full_repo_name }}` (posted with `vars:`), location before control, a screenshot only where the menu is
hard to describe, a confirmation cue, and hints written as symptom, cause, fix.

## Faded example (later step, completion level)

```markdown
### ⌨️ Activity: Open a pull request for your docs

1. Open a pull request from `add-docs` into `main`. Need a reminder? The **Pull requests** tab has a
   **New pull request** button.

1. Write your own title that says what the change does. There is no single right answer.

   > 💡 **Tip:** Good titles start with a verb, such as "Add setup guide".

1. Click **Create pull request**, then wait for Mona's feedback.
```

The learner now recalls the navigation (retrieval), writes their own title (generation), and gets a tip instead
of exact text (fading).

## Review (`x-review.md`)

Recap capabilities, ask one or two recall questions with collapsible answers, add one transfer prompt, and give
one next step. See the scaffold template `assets/steps/x-review.md`.

## Length heuristics

These are practice heuristics, not research thresholds. Validate with testers.

| Element | Typical size |
| --- | --- |
| Story hook | 1–3 sentences |
| Theory | 2–5 sentences plus at most one table, list, or diagram (validator flags over about 250 words) |
| Activity | 3–8 numbered instructions; split above about 12 |
| Having trouble | 2–4 bullets per activity |
| Step total | 5–12 learner minutes |
