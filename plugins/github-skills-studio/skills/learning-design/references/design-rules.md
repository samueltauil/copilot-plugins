# Design rules by exercise part

Apply these while outlining, writing, and reviewing. Each rule cites the principle it comes from in
[evidence-base.md](evidence-base.md). Rules marked **(official)** come from the
[exercise-creator guidance](https://github.com/skills/exercise-creator/tree/main/docs).

## README (landing page)

| Rule | Principle |
| --- | --- |
| Promise one new, observable skill and the artifact the learner will build | Alignment, motivation (relevance) |
| Write "Who is this for" as a specific learner, not "everyone" | Learner analysis, expertise reversal |
| List prerequisites, required plans or access (Copilot, Codespaces), and possible Actions cost **before** the Copy Exercise button | Accessibility, expectancy |
| State a realistic time measured with testers, not a wish | Usability, honesty |
| One objective per step under "In this exercise, you will" | Constructive alignment |
| Never put content the learner needs mid-exercise in the README; it is replaced when the exercise starts | Framework contract |

## Story (opening of each step)

| Rule | Principle |
| --- | --- |
| One to three sentences: the situation, and the question this step answers | Curiosity, relevance |
| Connect to what the learner just did ("Now that your branch exists...") | Activation (Merrill), coherence |
| Keep one consistent scenario across steps; never let the story hide the task | Coherence |
| Resolve the opening question by the end of the step | Curiosity (no unresolved gaps) |

## 📖 Theory

| Rule | Principle |
| --- | --- |
| Exactly the concept the activity needs, at awareness level **(official)** | Cognitive load, coherence |
| Define new terms right before they are used; spell out acronyms | Pre-training, plain language |
| Link key terms inline to GitHub Docs instead of a references list **(official)** | Signaling, coherence |
| Prefer one small table, list, or diagram over paragraphs when it shows structure | Multimedia, signaling |
| Never copy GitHub Docs; introduce and link **(official)** | Maintainability |
| Avoid content that changes often, such as quotas and prices **(official)** | Maintainability |

## ⌨️ Activity

| Rule | Principle |
| --- | --- |
| One activity practices one concept; one to three activities per step **(official)** | Segmenting, cognitive load |
| Step 1: exact, complete instructions (worked example). Later steps: fade to goals with hints | Worked examples, fading, expertise reversal |
| Location first, then the control in **bold**, then the value in `code` **(official)** | Signaling, spatial contiguity |
| Call out context switches ("Switch back to the exercise issue tab") **(official)** | Cognitive walkthrough (noticing the action) |
| After each consequential action, say what the learner should now see | Feed up, cognitive walkthrough (seeing progress) |
| Ask for generation where exact text is not graded (commit message, prompt variations) | Generation effect |
| From step 2 onward, include one retrieval moment ("Create a branch, as in step 1") | Retrieval practice |
| Optionally ask for a prediction before a key action, then compare | Metacognition |
| Keep instructions to two levels and about twelve items at most **(official)** | Cognitive load |
| End with the triggering action and "Wait a moment for Mona..." | Feed up, honest status |

## Having trouble? 🤷 (one per activity)

| Rule | Principle |
| --- | --- |
| Each bullet: symptom → likely cause → safe recovery | Error management, feed forward |
| Order hints from clue to explicit instruction | Scaffolding |
| Cover the top two or three mistakes found in walkthrough tests | Usability evidence |
| Mention how to re-trigger the check (push again, re-run the workflow) | Error management |

## Grading feedback (results table and tips)

| Rule | Principle |
| --- | --- |
| Grade only when the check gives actionable feedback or protects later steps **(official)** | Feedback, validity |
| Each row states the expectation in learner language ("`docs/plan.md` exists on your branch") | Feed up |
| Failed rows come with a next action (tips) | Feed forward |
| Check intent, not wording: case-insensitive keyphrases, several accepted phrases | Validity, generation |
| Describe work, not the learner; no "Wrong!" | Attribution, mindset |
| Never let a failed check advance the learner (`needs: check_step_work`) | Validity, error management |

## Review (`x-review.md`)

| Rule | Principle |
| --- | --- |
| Recap accomplishments as capabilities ("You can now...") | Satisfaction (ARCS), metacognition |
| One or two recall questions with collapsible answers | Retrieval practice |
| One transfer prompt ("Where would you use this in your own repository?") | Transfer, reflection |
| One clear next step: the follow-up exercise and the Docs page to go deeper | Spacing, transfer |
| End honestly and warmly; do not oversell | Endings (exploratory) |

## Workshop sequencing (several exercises)

| Rule | Principle |
| --- | --- |
| Map prerequisites per exercise and offer a bypass for what learners already know | Expertise reversal, adult learning |
| Revisit earlier skills in later exercises without reprinting their instructions | Spacing, retrieval, spiral curriculum |
| Each exercise is an independent repository copy; never assume files carry over | Framework contract |
| Finish with an integration (capstone) exercise and a reflection | Merrill integration, transfer |
| Publish a schedule with setup time, breaks, checkpoints, and an async continuation path | Usability, inclusion |
| Evaluate reaction, learning (a less-supported task), and later behavior separately | Kirkpatrick |

## Everywhere

| Rule | Principle |
| --- | --- |
| Alt text on informative images; descriptive link text; status never by color alone | WCAG 2.2, UDL |
| Plain language; "repository" not "repo"; consistent terminology | ISO 24495-1, official style |
| Friendly, casual, active voice with sparing emoji **(official)** | Personalization |
| Test with representative learners before release **(official)** | Usability evaluation |
