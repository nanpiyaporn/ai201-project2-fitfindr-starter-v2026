# The Unofficial Guide

**Piyaporn Puangprasert(Nan) corpus : city_guides index **

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

 I choose a campus_life corpus:
 - It is about 88 short posts ( 1-3 paragraphs each) covering on student-life,housing, parking permit, dinning, financial aid, etc. 
  Questions can be ask: for example, 
  - when is the add/drop class deadline?
  - How to apply financial aid?
  - How far from dinning hall to some class building?
  - Etc.
  P.S. The answer will come from the material topic (No, Outside sources such as Google search)


## Chunking Strategy

**Chunk size:**
88 chunks
**Overlap:**

What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. 

Answer: I asked "How do I apply for financial aid?" and the system responded
"no information explaining how to apply for financial aid" — the corpus
doesn't cover an application process. Next I changed the question to match
what the corpus actually contains:

```
python app.py ask "What are the graduation requirements?"
```

## Sample Chunks

 Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. 

**Chunk 1** — source: `` admin_add_drop_deadline.txt#0   —  produced by: chunker.py::fallback_split ``

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `` course_biol_160.txt#0   —  produced by: chunker.py::fallback_split ``

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `` course_hist_118_workload.txt#0  — produced by: chunker.py::fallback_split ``

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: ``dining_pellew_dining_hall_followup.txt#0  — produced by: chunker.py::fallback_split``

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `` housing_innisfree_hall.txt#0  — produced by: chunker.py::fallback_split``

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
```

## Sample Answer

One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. 

**Question:** `python app.py ask "What are the graduation requirements?"`

**Answer:**

```
(best distance 0.327, cutoff 0.6)

Based on the provided documents, the graduation requirements are 120 credit
hours, a completed major, the general education requirements, and the
writing-intensive requirement of two courses taken in different departments
(admin_graduation_requirements.txt).
```

**My relevance cutoff:**

The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. 

| Question | In corpus? | Best distance |
|---|---|---|
|What do students say about wait times at Commons during lunch?  | Yes | 0.308 |
|When is the add/drop period for this semester?  | Yes | 0.273 |
|What time does the library close on weekends?  | Yes | 0.414 |
|How do I get a parking permit?  |Yes  | 0.534 |
|What majors are offered in the Computer Science department? | Yes | 0.579 |

| What is the capital of Thailand? | No | 0.897  |
| How do I win the lottery? | No | 0.549 |
| Who won the 2026 World Cup? | No | 0.856 |
| How to get a software engineering job? | No | 0.734 |
| How to finish a master degree in May 2027? | No | 0.568 |


## How I Used AI

 Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. 

**1.**
I asked Claude to write the chunking function from this assignment, but it did not work. Claude do not understand this question.

**2.**

 ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── 

---

# Unit 2

These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. 

## Run Log — Before

 Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.


     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 / 5 | 5/5 | 5/5 | MET|
| 2. Every answer names a source | 5 of 5 | 4 /5 | 4 /5 | 4 /5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 3/5 | 3/5 | 3/5 |  MISSED|



 Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. 


__________________________
## Verdicts

 MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. 

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | What do students say about wait times at Commons during lunch? | MET | AGREE |
| 2 | When is the add/drop period for this semester? | MET | AGREE |
| 3 | What time does the library close on weekends? | MET | AGREE |
| 4 | How do I get a parking permit? | MET | AGREE |
| 5 | What majors are offered in the Computer Science department? | MET |AGREE  |


## Diagnoses

 For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

The in-scope and out-of-score distances overlap.

Foe example the parking question (in scope) is 0.534, but the lottory question ( out-of-scope) is 0.549 and the master degree is 0.568. A cutoff of 0.6 sites above all of them can pass

     Milestone 3. -->

## The Improvement

**What I changed:**
I change the 'THRESHOLD =0.6' to 'THRESHOLD =0.54' that should return *refused*



**Why I picked it:**

Because the 'THRESHOLD  < 0.6'

 Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. 

### Run Log — After

 Same format, same five criteria, three runs each.
     `python run_eval.py --label after` 

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 4/5 |MISSED  |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 |5/5 | 5/5 |  MET|

____________________
 


_____________________________________________
**Did it help?**

 Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. 

## What's Still Broken

Yes, it still broken. Adjust to lower the 'THRESHOLD' to lower than 0.54. But the question about What majors are offered in the Computer Science department? give me the chunk was 0.579 that mean this question should *REFUSE* instead of *PASS* that I can confirm this in results/run_2026-09-29_1844_after.md

For each criterion still missed after your fix: what you'd do about it,
     
 The 'run_eval.py' asked 'scorer.py' that this question should return *REFUSE*. That mean the correct answer is to sya "I don't know" because no document proof.    

     

     Milestone 5.

## What I'd Do Differently

Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. 

check if the txt file has a correct information and clear content. Then, compare the answer with the difference number of'THRESHOLD'.
I confuse myself about 4/5, 5/5 , missed, and met. Because there are 10 questions. The questions are only in-text 5 and out-of-scope 5. I will keep *PASS* or *REFUSE** in each question instead. with chung number because some question pass with 'THRESHOLD' > 0.54 that is something we need to find out, why it happen?
