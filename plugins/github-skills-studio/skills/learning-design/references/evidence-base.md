# Evidence base for exercise design

Evidence-based principles from learning science and instructional design, each translated into concrete rules
for GitHub Skills exercises. Use it to justify design decisions and to avoid confident claims the evidence does
not support.

## How to read this file

Every principle carries an evidence label:

| Label | Meaning |
| --- | --- |
| **Strong** | Substantial converging experimental or review evidence (not necessarily from GitHub exercises) |
| **Moderate** | Useful evidence with material boundary conditions |
| **Framework** | A design model that organizes decisions; not a demonstrated effect |
| **Exploratory** | Indirect evidence or uncertain application to tutorials |

Two cautions apply everywhere:

- None of this research establishes exact sentence counts, step counts, or durations for GitHub Skills. Treat the
  official limits (five steps or fewer, about four times expert time, drop-off after 30 to 45 minutes) as
  practitioner observations from [exercise-creator](https://github.com/skills/exercise-creator/blob/main/docs/reference/exercise.md),
  not laws.
- A workflow pass shows that specified checks passed. It does not show that the learner understands or can
  transfer the skill. See [assessment validity](#22-assessment-validity).

---

## A. Load and presentation

### 1. Cognitive load, worked examples, expertise reversal — Strong (specific effects)

Working memory is limited when material is unfamiliar. Intrinsic load depends on how many elements must be
handled together and on prior knowledge; extraneous load comes from avoidable demands of presentation or
procedure. Worked examples help novices build a mental model; completion problems and fading shift the work to
the learner gradually. Support that helps novices can become redundant for learners who already know the task
(expertise reversal) (Sweller et al., 1998, 2019; Kalyuga et al., 2003; Renkl et al., 2002).

Caveats: load is not measured by word count. Splitting a genuinely integrated task into disconnected fragments
can make it harder. Expertise reversal is task-specific, not a permanent learner category.

Rules for exercises:

1. Introduce only the concepts the next action needs, and define a term right before it is used.
2. Keep the instruction, the command or prompt, and the expected result next to each other.
3. Step 1: a complete, exact example (worked example). Middle steps: partly specified tasks (completion).
   Last step: a goal with light guidance (independent attempt).
4. Offer an optional fast path for learners who already know the prerequisites, without hiding the supported path.
5. Remove decoration that competes with the task; keep context needed to understand it.

### 2. Multimedia learning — Moderate to strong (transfer to Markdown is indirect)

Mayer's principles concern learning from words and relevant pictures under limited processing capacity:
coherence (remove the irrelevant), signaling (highlight essentials), redundancy, spatial and temporal contiguity
(keep corresponding words and pictures together), segmenting (learner-paced chunks), pre-training (introduce key
components first), modality, multimedia (relevant words plus graphics), personalization (conversational
language), voice, and image (an instructor picture does not automatically help) (Mayer, 2020, 2021; Mayer &
Fiorella, 2014).

Caveats: the redundancy finding is mostly about simultaneous narration plus identical on-screen text. It is not a
reason to remove captions, transcripts, or alt text.

Rules for exercises:

1. Add a screenshot only when it clarifies a location or a state that words cannot; put the sentence that
   explains it directly beside it.
2. Name the control in text. Never rely on an arrow or a color in the image alone.
3. Use the ⌨️ and 📖 headings, bold control names, and `code` values consistently as signals.
4. If you use video, add captions and a transcript, and never require audio.
5. Let Mona's conversational voice support clarity, not replace a precise instruction.

---

## B. Memory and practice

### 3. Retrieval practice — Strong for retention

Bringing information or a procedure to mind strengthens later retention more than rereading, even when
rereading looks better on an immediate test (Roediger & Karpicke, 2006; Karpicke & Blunt, 2011; Rowland, 2014;
Adesope et al., 2017).

Caveats: copying visible instructions is not retrieval. Give corrective information after an attempt.

Rules for exercises:

1. In a later step, ask the learner to repeat an earlier action without the full instructions
   (for example, "Create a branch for this fix, as you did in step 1").
2. Add one or two low-stakes recall questions in `x-review.md`, with the answer in a collapsible block.
3. Keep navigation help visible. Retrieving a concept does not mean making the interface hard to find.

### 4. Spacing and interleaving — Strong (spacing); moderate and conditional (interleaving)

Spacing distributes practice over time. Interleaving mixes already-introduced problem types so learners must
choose the right approach; its benefit depends on the material (Cepeda et al., 2006; Rohrer & Taylor, 2007;
Brunmair & Richter, 2019).

Caveats: repetitions inside one 45-minute session are not proven long-term spacing. Interleaving helps most when
learners must discriminate similar choices; arbitrary topic switching is not interleaving.

Rules for exercises:

1. Revisit the core skill in the review, then point to a follow-up exercise for another day.
2. In a series, make a later exercise use an earlier skill without reprinting its solution.
3. Introduce each procedure clearly before mixing similar choices (for example, picking between two triggers
   you have already taught).

### 5. Desirable difficulties — Moderate (stronger for retrieval and spacing specifically)

Some conditions make practice feel slower but improve retention or transfer. The difficulty must engage a useful
learning process, not just consume attention (Bjork, 1994; Bjork & Bjork, 2011, 2020).

Rules for exercises:

1. Start with a supported success, then ask for a modest independent variation.
2. Make hints available during or after an attempt; do not force long unproductive struggle.
3. Broken links, hidden controls, missing prerequisites, and ambiguous grading are never "desirable". Fix them.

### 6. Generation, self-explanation, elaboration — Moderate

Generating an answer, explaining why a step works, and connecting new ideas to prior knowledge can beat reading a
supplied answer (Slamecka & Graf, 1978; Chi et al., 1989, 1994; Bisra et al., 2018). Dunlosky et al. (2013)
rated practice testing and distributed practice as high utility; self-explanation, elaborative interrogation, and
interleaving as moderate; rereading and highlighting as low.

Rules for exercises:

1. Let the learner write their own commit message, issue title, or prompt where the exact text does not matter
   for grading.
2. Ask a short "why" question after an action ("Why is a pull request better here than committing to `main`?")
   and give a model answer after the attempt.
3. Never require an exact keyword for an open explanation that has several valid answers.

---

## C. Feedback and errors

### 7. Feedback — Strong that it can help; effects vary widely

Useful formative feedback answers: where am I going (feed up), how am I doing (feedback), and what next (feed
forward). It can address the task, the process, self-regulation, or the person; specific information about the
task or process is more useful than judgments about the person (Hattie & Timperley, 2007; Shute, 2008). Some
feedback interventions harm performance (Kluger & DeNisi, 1996); the average educational effect is positive but
heterogeneous (Wisniewski et al., 2020).

Rules for exercises:

1. State the expected outcome before the learner acts (the activity's confirmation cue).
2. On failure, name the specific check that failed and one next action:
   "`docs/plan.md` was not found on the `plan` branch. Create it there, commit, and push again."
3. Distinguish "checking", "passed", "check failed", and "workflow did not run".
4. Praise the action or strategy; never label the learner.
5. Grade only when the check gives actionable feedback or protects later steps.

### 12. Error management and productive failure — Moderate, task-dependent

Errors help when learners can recognize and correct them safely. Error-management training pairs exploration
with encouragement to learn from errors; productive failure means an attempt followed by instruction and
consolidation, not failure alone (Keith & Frese, 2008; Kapur, 2008, 2016; Metcalfe, 2017; Sinha & Kapur, 2021).

Rules for exercises:

1. Experiments happen in the learner's disposable copy and are reversible.
2. Failure messages are neutral, specific, and retryable. Never require secrets or touching a real project.
3. Each `Having trouble? 🤷` item states symptom, likely cause, and safe recovery.
4. If a step opens with a challenge, explain the solution explicitly afterwards.
5. Never manufacture errors just to add difficulty.

### 13. Mindset and attribution — Mixed evidence

Intelligence-focused praise sometimes produced worse responses to difficulty than process-focused feedback in
child studies; broader growth-mindset effects are small and context-dependent (Mueller & Dweck, 1998; Sisk et
al., 2018; Yeager et al., 2019).

Rules for exercises:

1. Describe the work, not the person: "The workflow file is there; its trigger still needs a branch."
2. Suggest a concrete strategy rather than "try harder".
3. Normalize retries ("This one trips up a lot of people") without promising effort alone solves it.

---

## D. Motivation and engagement

### 8. Self-determination, ARCS, expectancy-value — Moderate (ARCS is a framework)

Self-determination theory emphasizes autonomy, competence, and relatedness; Keller's ARCS model organizes design
around attention, relevance, confidence, and satisfaction; expectancy-value theory asks whether learners expect
to succeed and value the task (Ryan & Deci, 2000; Keller, 1987; Eccles & Wigfield, 2002).

Rules for exercises:

1. Say why the skill matters in the README and in each step's story, in terms of a real task.
2. Make the first meaningful action achievable within minutes and show its result.
3. Offer a meaningful choice (for example, web editor or Codespaces) only when both routes are supported and
   graded fairly.
4. Where possible, give a human support route (discussion, facilitator) in addition to Mona.

### 15. Curiosity and information gaps — Moderate (indirect for story hooks)

A small, meaningful gap between what learners know and want to know can motivate exploration (Loewenstein, 1994;
Gruber et al., 2014).

Rules for exercises:

1. Open a step with one actionable question the activity answers ("Why didn't the check run on that pull
   request?").
2. Resolve the question by the end of the step. Never withhold essential instructions to create suspense.

### 14. Progress visibility and endings — Exploratory for learning

Goal-gradient and peak-end research comes from consumer and affective settings (Kivetz et al., 2006; Kahneman et
al., 1993; Fredrickson & Kahneman, 1993). Treat them as experience-design hypotheses.

Rules for exercises:

1. Show honest progress ("Step 2 of 4") and distinguish a pending check from completion.
2. End with a concise recap, a genuine acknowledgment, and one useful next step.
3. Do not rely on a celebratory ending to compensate for friction earlier.

### 11. Adult learning (andragogy) — Framework; mechanism claims are contested

Relevance, experience, self-direction, and problem-centered tasks are useful design questions for professional
workshops, not traits every adult has (Knowles et al., 2015; Moll, 2024).

Rules for exercises:

1. Use a realistic repository task with stated practical value.
2. List prerequisites without assuming job title predicts competence.
3. Keep a complete novice route even when you add shortcuts for experienced learners.

---

## E. Design frameworks

### 9. Backward design, constructive alignment, Merrill, Gagné, Bloom — Frameworks

Backward design starts from the intended result, then the acceptable evidence, then instruction; constructive
alignment links objective, activity, and assessment. Merrill emphasizes a real problem, activation,
demonstration, application, and integration. Gagné's nine events are a planning checklist. Revised Bloom verbs
help describe observable cognitive work, though a verb alone does not set complexity (Wiggins & McTighe, 2005;
Biggs, 1996; Merrill, 2002; Gagné, 1985; Anderson & Krathwohl, 2001).

Rules for exercises:

1. Write one observable objective per step before writing content.
2. Decide what evidence supports it before choosing a workflow check.
3. Make the activity perform the target behavior, and make the review revisit it.
4. Use the frameworks flexibly; skip events that add nothing.

### 10. Scaffolding and the zone of proximal development — Moderate

Scaffolding is temporary, contingent support that is withdrawn as responsibility transfers (Wood et al., 1976;
Vygotsky, 1978; van de Pol et al., 2010). A collapsible hint approximates scaffolding; it is not adaptive tutoring.

Rules for exercises:

1. Order hints from clue, to targeted instruction, to worked example.
2. Reduce detail on a later, similar activity while keeping a way to reopen help.
3. Keep every hint optional and keyboard accessible.

### 16. Metacognition and reflection — Moderate

Planning, monitoring, and reflecting support self-regulated learning (Zimmerman, 2002).

Rules for exercises:

1. Before a key action, ask the learner to predict the result; afterwards, compare.
2. In `x-review.md`, add one optional prompt such as "Where would you use this in your own repository?"
3. Keep reflection private. Never ask for sensitive workplace details in a public issue.

### 17. Transfer of learning — Moderate, context-dependent

Hugging makes practice resemble real performance; bridging asks learners to connect a principle to new
situations. Transfer is not automatic (Perkins & Salomon, 1992; Barnett & Ceci, 2002).

Rules for exercises:

1. Practice in a real but safe repository with the same concepts learners meet at work.
2. Ask for a small adaptation of the example (different file, branch, or trigger).
3. In the review, separate what generalizes from what is specific to the exercise.

### 22. Assessment validity — Framework with direct practical importance

Validity is about whether evidence supports the interpretation you make from a result (Messick, 1995; Biggs,
1996). A file-exists check proves a file is present, not that the learner understood its purpose.

Rules for exercises:

1. Map every check to an objective and state exactly what it observes.
2. Accept legitimate alternative solutions where feasible (case-insensitive matching, several keyphrases).
3. Test each grader with a correct artifact, an incorrect artifact, and a plausible alternative.
4. Never claim mastery from a proxy check.
5. Provide a fallback when a workflow cannot run (permissions, outages): `workflow_dispatch` plus instructions.

---

## F. Inclusion

### 18. Universal Design for Learning, accessibility, plain language — Requirements and framework

CAST's UDL Guidelines 3.0 encourage multiple means of engagement, representation, and action and expression.
WCAG 2.2 gives testable accessibility criteria; ISO 24495-1 covers plain language (CAST, 2024; W3C, 2023, 2024;
ISO, 2023).

Rules for exercises:

1. Meaningful alt text for informative images; empty alt (`alt=""`) only for decoration.
2. Descriptive link text, logical headings, numbered actions, plain language, acronyms spelled out.
3. Never convey pass or fail by color or emoji alone; the results table already pairs ✅ with "Pass".
4. Text contrast 4.5:1 (3:1 for large text) where you control colors, such as diagrams.
5. Make collapsible hints and any embedded media keyboard operable; caption videos.
6. State account, plan, permission, tool, and cost requirements before the learner starts.

---

## G. Evaluation

### 19. Usability evaluation — Established methods

Cognitive walkthrough asks, at each action: will learners try to achieve the right effect, notice the correct
action, associate it with the effect, and see progress afterwards? Heuristic evaluation finds problems such as
invisible status, inconsistency, and poor error recovery. Think-aloud testing observes real users; SUS measures
perceived overall usability; the Single Ease Question (SEQ) rates one task (Wharton et al., 1994; Nielsen,
1994a, 1994b; Ericsson & Simon, 1993; Brooke, 1996; Sauro, 2012).

Caveat: a walkthrough, including an automated one, does not replace testing with representative learners.

### 20. Training evaluation — Framework

Kirkpatrick's levels separate reaction, learning, behavior, and results. Satisfaction alone does not establish
learning, and the levels are not a guaranteed causal chain (Kirkpatrick & Kirkpatrick, 2006, 2016).

---

## H. Myths to avoid

See [myths-to-avoid.md](myths-to-avoid.md): learning-styles matching, "learning pyramid" retention percentages,
and the universal ten-minute attention span (Pashler et al., 2008; Lalley & Miller, 2007; Bradbury, 2016).

---

## References

Adesope, O. O., Trevisan, D. A., & Sundararajan, N. (2017). Rethinking the use of tests: A meta-analysis of practice testing. *Review of Educational Research, 87*(3), 659–701. https://doi.org/10.3102/0034654316689306

Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. Longman.

Barnett, S. M., & Ceci, S. J. (2002). When and where do we apply what we learn? A taxonomy for far transfer. *Psychological Bulletin, 128*(4), 612–637. https://doi.org/10.1037/0033-2909.128.4.612

Biggs, J. (1996). Enhancing teaching through constructive alignment. *Higher Education, 32*(3), 347–364. https://doi.org/10.1007/BF00138871

Bisra, K., Liu, Q., Nesbit, J. C., Salimi, F., & Winne, P. H. (2018). Inducing self-explanation: A meta-analysis. *Educational Psychology Review, 30*(3), 703–725. https://doi.org/10.1007/s10648-018-9434-x

Bjork, E. L., & Bjork, R. A. (2011). Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning. In M. A. Gernsbacher et al. (Eds.), *Psychology and the real world* (pp. 56–64). Worth.

Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. P. Shimamura (Eds.), *Metacognition: Knowing about knowing*. MIT Press. https://doi.org/10.7551/mitpress/4561.003.0011

Bjork, R. A., & Bjork, E. L. (2020). Desirable difficulties in theory and practice. *Journal of Applied Research in Memory and Cognition, 9*(4), 475–479. https://doi.org/10.1016/j.jarmac.2020.09.003

Bradbury, N. A. (2016). Attention span during lectures: 8 seconds, 10 minutes, or more? *Advances in Physiology Education, 40*(4), 509–513. https://doi.org/10.1152/advan.00109.2016

Brooke, J. (1996). SUS: A "quick and dirty" usability scale. In P. W. Jordan et al. (Eds.), *Usability evaluation in industry*. CRC Press. https://doi.org/10.1201/9781498710411-35

Bruner, J. S. (1960). *The process of education*. Harvard University Press.

Brunmair, M., & Richter, T. (2019). Similarity matters: A meta-analysis of interleaved learning and its moderators. *Psychological Bulletin, 145*(11), 1029–1052. https://doi.org/10.1037/bul0000209

CAST. (2024). *Universal Design for Learning Guidelines version 3.0*. https://udlguidelines.cast.org/

Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin, 132*(3), 354–380. https://doi.org/10.1037/0033-2909.132.3.354

Chi, M. T. H., Bassok, M., Lewis, M. W., Reimann, P., & Glaser, R. (1989). Self-explanations: How students study and use examples in learning to solve problems. *Cognitive Science, 13*(2), 145–182. https://doi.org/10.1207/s15516709cog1302_1

Chi, M. T. H., de Leeuw, N., Chiu, M.-H., & LaVancher, C. (1994). Eliciting self-explanations improves understanding. *Cognitive Science, 18*(3), 439–477. https://doi.org/10.1207/s15516709cog1803_3

Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest, 14*(1), 4–58. https://doi.org/10.1177/1529100612453266

Eccles, J. S., & Wigfield, A. (2002). Motivational beliefs, values, and goals. *Annual Review of Psychology, 53*, 109–132. https://doi.org/10.1146/annurev.psych.53.100901.135153

Ericsson, K. A., & Simon, H. A. (1993). *Protocol analysis: Verbal reports as data* (rev. ed.). MIT Press. https://doi.org/10.7551/mitpress/5657.001.0001

Fredrickson, B. L., & Kahneman, D. (1993). Duration neglect in retrospective evaluations of affective episodes. *Journal of Personality and Social Psychology, 65*(1), 45–55. https://doi.org/10.1037/0022-3514.65.1.45

Gagné, R. M. (1985). *The conditions of learning and theory of instruction* (4th ed.). Holt, Rinehart and Winston.

Gruber, M. J., Gelman, B. D., & Ranganath, C. (2014). States of curiosity modulate hippocampus-dependent learning via the dopaminergic circuit. *Neuron, 84*(2), 486–496. https://doi.org/10.1016/j.neuron.2014.08.060

Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81–112. https://doi.org/10.3102/003465430298487

International Organization for Standardization. (2023). *Plain language — Part 1: Governing principles and guidelines* (ISO 24495-1:2023). https://www.iso.org/standard/78907.html

Kahneman, D., Fredrickson, B. L., Schreiber, C. A., & Redelmeier, D. A. (1993). When more pain is preferred to less: Adding a better end. *Psychological Science, 4*(6), 401–405. https://doi.org/10.1111/j.1467-9280.1993.tb00589.x

Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist, 38*(1), 23–31. https://doi.org/10.1207/S15326985EP3801_4

Kapur, M. (2008). Productive failure. *Cognition and Instruction, 26*(3), 379–424. https://doi.org/10.1080/07370000802212669

Kapur, M. (2016). Examining productive failure, productive success, unproductive failure, and unproductive success in learning. *Educational Psychologist, 51*(2), 289–299. https://doi.org/10.1080/00461520.2016.1155457

Karpicke, J. D., & Blunt, J. R. (2011). Retrieval practice produces more learning than elaborative studying with concept mapping. *Science, 331*(6018), 772–775. https://doi.org/10.1126/science.1199327

Keith, N., & Frese, M. (2008). Effectiveness of error management training: A meta-analysis. *Journal of Applied Psychology, 93*(1), 59–69. https://doi.org/10.1037/0021-9010.93.1.59

Keller, J. M. (1987). Development and use of the ARCS model of instructional design. *Journal of Instructional Development, 10*(3), 2–10. https://doi.org/10.1007/BF02905780

Kirkpatrick, D. L., & Kirkpatrick, J. D. (2006). *Evaluating training programs: The four levels* (3rd ed.). Berrett-Koehler.

Kirkpatrick, J. D., & Kirkpatrick, W. K. (2016). *Kirkpatrick's four levels of training evaluation*. ATD Press.

Kivetz, R., Urminsky, O., & Zheng, Y. (2006). The goal-gradient hypothesis resurrected. *Journal of Marketing Research, 43*(1), 39–58. https://doi.org/10.1509/jmkr.43.1.39

Kluger, A. N., & DeNisi, A. (1996). Effects of feedback intervention on performance. *Psychological Bulletin, 119*(2), 254–284. https://doi.org/10.1037/0033-2909.119.2.254

Knowles, M. S., Holton, E. F., III, & Swanson, R. A. (2015). *The adult learner* (8th ed.). Routledge.

Lalley, J. P., & Miller, R. H. (2007). The learning pyramid: Does it point teachers in the right direction? *Education, 128*(1), 64–79. https://eric.ed.gov/?id=EJ790160

Loewenstein, G. (1994). The psychology of curiosity: A review and reinterpretation. *Psychological Bulletin, 116*(1), 75–98. https://doi.org/10.1037/0033-2909.116.1.75

Mayer, R. E. (2020). *Multimedia learning* (3rd ed.). Cambridge University Press. https://doi.org/10.1017/9781316941355

Mayer, R. E. (2021). Evidence-based principles for how to design effective instructional videos. *Journal of Applied Research in Memory and Cognition, 10*(2), 229–240. https://doi.org/10.1016/j.jarmac.2021.03.007

Mayer, R. E., & Fiorella, L. (2014). Principles for reducing extraneous processing in multimedia learning. In R. E. Mayer (Ed.), *The Cambridge handbook of multimedia learning* (2nd ed., pp. 279–315). Cambridge University Press. https://doi.org/10.1017/CBO9781139547369.015

Merrill, M. D. (2002). First principles of instruction. *Educational Technology Research and Development, 50*(3), 43–59. https://doi.org/10.1007/BF02505024

Messick, S. (1995). Validity of psychological assessment. *American Psychologist, 50*(9), 741–749. https://doi.org/10.1037/0003-066X.50.9.741

Metcalfe, J. (2017). Learning from errors. *Annual Review of Psychology, 68*, 465–489. https://doi.org/10.1146/annurev-psych-010416-044022

Moll, I. (2024). A psychological critique of Knowles' andragogy as a theory of learning. *Studies in Adult Education and Learning, 30*(1), 151–170. https://doi.org/10.4312/as/16396

Mueller, C. M., & Dweck, C. S. (1998). Praise for intelligence can undermine children's motivation and performance. *Journal of Personality and Social Psychology, 75*(1), 33–52. https://doi.org/10.1037/0022-3514.75.1.33

Nielsen, J. (1994a). *10 usability heuristics for user interface design*. Nielsen Norman Group. https://www.nngroup.com/articles/ten-usability-heuristics/

Nielsen, J. (1994b). *Severity ratings for usability problems*. Nielsen Norman Group. https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/

Pashler, H., McDaniel, M., Rohrer, D., & Bjork, R. (2008). Learning styles: Concepts and evidence. *Psychological Science in the Public Interest, 9*(3), 105–119. https://doi.org/10.1111/j.1539-6053.2009.01038.x

Perkins, D. N., & Salomon, G. (1992). Transfer of learning. In *International encyclopedia of education* (2nd ed.). Pergamon Press.

Renkl, A., Atkinson, R. K., Maier, U. H., & Staley, R. (2002). From example study to problem solving: Smooth transitions help learning. *The Journal of Experimental Education, 70*(4), 293–315. https://doi.org/10.1080/00220970209599510

Roediger, H. L., III, & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science, 17*(3), 249–255. https://doi.org/10.1111/j.1467-9280.2006.01693.x

Rohrer, D., & Taylor, K. (2007). The shuffling of mathematics problems improves learning. *Instructional Science, 35*(6), 481–498. https://doi.org/10.1007/s11251-007-9015-8

Rowland, C. A. (2014). The effect of testing versus restudy on retention: A meta-analytic review of the testing effect. *Psychological Bulletin, 140*(6), 1432–1463. https://doi.org/10.1037/a0037559

Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist, 55*(1), 68–78. https://doi.org/10.1037/0003-066X.55.1.68

Sauro, J. (2012). *10 things to know about the Single Ease Question (SEQ)*. MeasuringU. https://measuringu.com/seq10/

Shute, V. J. (2008). Focus on formative feedback. *Review of Educational Research, 78*(1), 153–189. https://doi.org/10.3102/0034654307313795

Sinha, T., & Kapur, M. (2021). When problem solving followed by instruction works: Evidence for productive failure. *Review of Educational Research, 91*(5), 761–798. https://doi.org/10.3102/00346543211019105

Sisk, V. F., Burgoyne, A. P., Sun, J., Butler, J. L., & Macnamara, B. N. (2018). To what extent and under which circumstances are growth mind-sets important to academic achievement? *Psychological Science, 29*(4), 549–571. https://doi.org/10.1177/0956797617739704

Slamecka, N. J., & Graf, P. (1978). The generation effect: Delineation of a phenomenon. *Journal of Experimental Psychology: Human Learning and Memory, 4*(6), 592–604. https://doi.org/10.1037/0278-7393.4.6.592

Sweller, J., van Merriënboer, J. J. G., & Paas, F. G. W. C. (1998). Cognitive architecture and instructional design. *Educational Psychology Review, 10*(3), 251–296. https://doi.org/10.1023/A:1022193728205

Sweller, J., van Merriënboer, J. J. G., & Paas, F. (2019). Cognitive architecture and instructional design: 20 years later. *Educational Psychology Review, 31*(2), 261–292. https://doi.org/10.1007/s10648-019-09465-5

van de Pol, J., Volman, M., & Beishuizen, J. (2010). Scaffolding in teacher–student interaction: A decade of research. *Educational Psychology Review, 22*(3), 271–296. https://doi.org/10.1007/s10648-010-9127-6

Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press.

Wharton, C., Rieman, J., Lewis, C., & Polson, P. (1994). The cognitive walkthrough method: A practitioner's guide. In J. Nielsen & R. L. Mack (Eds.), *Usability inspection methods* (pp. 105–140). Wiley.

Wiggins, G., & McTighe, J. (2005). *Understanding by design* (expanded 2nd ed.). ASCD.

Wisniewski, B., Zierer, K., & Hattie, J. (2020). The power of feedback revisited: A meta-analysis of educational feedback research. *Frontiers in Psychology, 10*, Article 3087. https://doi.org/10.3389/fpsyg.2019.03087

Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry, 17*(2), 89–100. https://doi.org/10.1111/j.1469-7610.1976.tb00381.x

World Wide Web Consortium. (2023, corrected 2024). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

Yeager, D. S., Hanselman, P., Walton, G. M., et al. (2019). A national experiment reveals where a growth mindset improves achievement. *Nature, 573*, 364–369. https://doi.org/10.1038/s41586-019-1466-y

Zimmerman, B. J. (2002). Becoming a self-regulated learner: An overview. *Theory Into Practice, 41*(2), 64–70. https://doi.org/10.1207/s15430421tip4102_2
