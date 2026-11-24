# Usability evaluation methods for walkthroughs

Established methods adapted to GitHub Skills exercises. They find defects; they do not measure learning or real
learner time (see [Limits](#limits)).

## Cognitive walkthrough (per instruction)

Answer four questions for every instruction and every transition (Wharton et al., 1994):

| # | Question | Typical failure in exercises |
| --- | --- | --- |
| Q1 | Will the learner try to achieve the right effect? | The purpose is unclear; theory did not prepare the action |
| Q2 | Will the learner notice that the correct action is available? | The location is not described, or the control is hidden in a menu |
| Q3 | Will the learner associate the correct action with the effect? | The label in the text differs from the UI ("Save" vs **Commit changes**) |
| Q4 | If the action is performed, will the learner see progress? | No confirmation cue; Mona's feedback is slow or silent |

Record each "no" as a finding with the instruction, what was expected, what the UI shows, and the fix.

## Heuristic evaluation (exercise-level)

Nielsen's ten heuristics (Nielsen, 1994), with what they mean for an exercise:

| Heuristic | Look for |
| --- | --- |
| Visibility of system status | Learners can tell whether Mona is checking, passed, failed, or not running |
| Match between system and the real world | Plain words; scenario matches real work; no internal jargon |
| User control and freedom | Safe retries; a way to recover from a wrong branch or commit |
| Consistency and standards | Same labels, headings, and badge styles in every step |
| Error prevention | Exact names stated before typing; hints before common traps |
| Recognition rather than recall | Navigation help stays visible (retrieval belongs to concepts, not to finding buttons) |
| Flexibility and efficiency of use | Optional fast paths for experienced learners, graded fairly |
| Aesthetic and minimalist design | No theory or images the activity does not need |
| Help users recognize, diagnose, and recover from errors | Failure rows and tips name the problem and the next action |
| Help and documentation | Having trouble after each activity; Docs links where depth is needed |

## Single Ease Question (per step)

After completing each step as the persona, rate: "Overall, how difficult or easy was this step to complete?" from
1 (very difficult) to 7 (very easy), with a one-sentence justification tied to observed friction (Sauro, 2012).
Ratings from an agent are a structured judgment, not user data; label them as such.

## Negative testing (graded steps)

Before the correct action, try one plausible mistake from the outline's test plan. There are two kinds, and they
need different expectations:

| Mistake | Example | Expected result | Harness |
| --- | --- | --- | --- |
| Matches the trigger, wrong work | Right branch and file, missing heading or keyphrase | The step does not advance; the results table and tips explain the fix | `wait-step --expect fail` → `failed-check` |
| Filtered out by the trigger | Wrong branch, wrong file path, closing a pull request instead of merging | Nothing happens: no graded run, no new step, no reply from Mona | `wait-step --expect none` → `ignored` |

Then:

1. For a graded failure, confirm the step's Having trouble block covers the mistake and recover by following only
   the feedback and hints.
2. For a filtered mistake, confirm the Having trouble block tells learners what to check when Mona stays silent
   (branch, path, event), because they get no feedback at all.
3. Perform the correct action and confirm the step advances.

A step that advances on wrong work is Blocking. A failure message, or silence, that does not lead to recovery is
Important.

## Time

- The agent's own pace is not a learner's. Report: the validator's content estimate, the measured automation
  latency (copy to first step, action to feedback), and steps where waiting exceeded about 60 seconds.
- Compare with the README promise; flag gaps for human testing.

## Accessibility spot checks

- Images in rendered comments have alt text and load.
- Collapsible blocks open with a click (and keyboard).
- Instructions do not depend on color or image-only cues.
- Shortcut instructions name both platforms; record shortcuts that could not be verified.

## Personas to simulate

| Persona | How to act | Finds |
| --- | --- | --- |
| Literal novice (default) | Follow every instruction exactly as written; assume nothing not stated | Ambiguity, missing steps, label mismatches |
| Skimmer | Read only bold text and code; skip theory | Hidden requirements, buried critical details |
| Keyboard-first | Prefer keyboard navigation where possible | Mouse-only instructions, unclear focus |

## Severity

Rate each problem by frequency (how many learners), impact (how hard to overcome), and persistence (once or every
time), then map: 4 catastrophe → Blocking, 3 major → Important, 2 minor → Important or Nice to improve,
1 cosmetic → Nice to improve (Nielsen, 1994b).

## Limits

An automated walkthrough does not replace testing with representative learners: an agent reads faster, does not
tire, may infer missing steps, and sees an accessibility tree rather than pixels. Use it to remove defects before
people test, and say so in the report.

## References

- Nielsen, J. (1994). *10 usability heuristics for user interface design*. https://www.nngroup.com/articles/ten-usability-heuristics/
- Nielsen, J. (1994b). *Severity ratings for usability problems*. https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
- Sauro, J. (2012). *10 things to know about the Single Ease Question (SEQ)*. https://measuringu.com/seq10/
- Wharton, C., Rieman, J., Lewis, C., & Polson, P. (1994). The cognitive walkthrough method: A practitioner's guide. In J. Nielsen & R. L. Mack (Eds.), *Usability inspection methods*. Wiley.
