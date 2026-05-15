# HW10 Submission Guide

Everything you need to submit for HW10, organized by deadline.

---

## Warm-up (Due Fri Apr 17, 11:59 PM)

Submit: **one PDF with answers to #1, #3, #4** + **the HW9 slide PDF**.

### #1 — Which prototype will you iterate on?

> **Meaning Search Lab** — the iterated low-fi prototype from HW9 by Can Wu.
> Topic: *Why semantic search retrieves relevant passages even without exact
> keyword overlap.* Target user: Chengtao Dai (Columbia MSCS, Fall 2025).
> Approved by TA Daniel Alejandro Manjarrez during HW9 feedback.

### #2 — Final iterations on the prototype

Use the HW9 PDF as-is (it already incorporated the iteration round from User
Test 1 and User Test 2 — added the "simplified metaphor — not real coordinates"
label, made Q1 a closer call with the motorcycle distractor, and added the
detailed incorrect-feedback explanations).

The two open items from the HW9 user tests are addressed in the technical
prototype rather than in the slides:

| HW9 open issue                                                 | Where it's now fixed                    |
| -------------------------------------------------------------- | --------------------------------------- |
| "Why is Doc A 0.91 and not 0.95?" — wants exact scoring        | Score & Rank lesson now displays the note **"Scores are approximate for illustration"** (see `data/lessons.json` lesson 6 `note`) |
| Tianjun missed the bottom-nav Back button on quiz feedback     | Feedback now renders an inline **Retry this question** + **Next** button pair *inside* the feedback view (see `static/js/main.js`, `renderFeedback`) |

### #3 — GitHub repository

**You still need to do this manually**:

1. Create a new repository on GitHub (suggested name: `meaning-search-lab`).
2. Push the contents of this folder.
3. Invite the other group members and the TA (Daniel Alejandro Manjarrez)
   as collaborators.
4. Take a screenshot of the repo page showing the name and the members list
   (Settings → Collaborators).
5. Paste that screenshot into your warm-up PDF.

```bash
# Inside this folder:
git init
git add .
git commit -m "Initial commit: HW10 technical prototype"
git branch -M main
git remote add origin https://github.com/<your-org>/meaning-search-lab.git
git push -u origin main
```

### #4 — Job assignments

Three-person group: Can Wu, Tianjun Zhong, Chengtao Dai. Per HW10 spec,
some members hold two roles.

| Part                          | Role                  | Owner            |
| ----------------------------- | --------------------- | ---------------- |
| **Part 1 — Learning portion** | Architecting the data | Can Wu           |
|                               | Implementing the UI   | Can Wu           |
|                               | Click-through testing | Tianjun Zhong    |
| **Part 2 — Quiz portion**     | Architecting the data | Chengtao Dai     |
|                               | Implementing the UI   | Chengtao Dai     |
|                               | Click-through testing | Tianjun Zhong    |

Rationale: Can owned the lesson content in HW9 so he continues there;
Chengtao was the target user and is well-positioned to own the quiz
(which is most user-facing); Tianjun did testing and note-taking in HW9
so he extends that into click-through QA on both parts.

---

## Main assignment (Due Mon Apr 20, 11:59 PM — no grace period)

Bring laptops with the app running for the TA feedback session.

### Group deliverables

1. **Responsibilities list** — see #4 above; revise if anything shifted
   during implementation.
2. **Copy of the low-fi prototype** — submit the HW9 PDF again (no
   further iterations needed; the open items are tracked in the code).
3. **~1-minute click-through video** — record yourselves walking through
   every screen of the app (Home → all 7 lessons → Quiz Q1 → feedback →
   Q2 → feedback → Results). Upload to YouTube (unlisted is fine) and
   paste the link in your submission.

   Suggested script: launch the app, click Start, click Next through each
   lesson, answer Q1 correctly to show the green feedback, retry Q2 with a
   wrong answer to show the red feedback then the correct one, end on the
   Results page showing 2/2.

### Individual deliverable (each member submits)

A short write-up (paragraph or bullets) of what *you* personally did this
week plus a screenshot of one commit you made to the repo.

**Suggested wording (edit to match what you actually did):**

> **Can Wu** — Designed the lesson data schema in `data/lessons.json` (7
> lesson types with a single dispatching template). Implemented all 7
> lesson states in `templates/learn.html` and the corresponding sections
> of `static/css/style.css` (meaning-space canvas, ranking rows, recap
> steps). Wrote the Flask routes for `/`, `/start`, and `/learn/<n>` in
> `app.py`.
>
> **Chengtao Dai** — Designed the quiz data schema in `data/quiz.json`
> (question + correct/incorrect feedback bundles). Implemented
> `templates/quiz.html` and `templates/results.html`, plus the AJAX
> submission + inline feedback rendering in `static/js/main.js`. Wrote
> the `/quiz/<n>`, `/api/quiz/answer`, `/results`, `/restart` routes in
> `app.py`.
>
> **Tianjun Zhong** — Click-through QA: walked the app end-to-end on
> macOS Chrome and Windows Firefox, filed and verified fixes for the
> nested-`<body>` bug on the quiz page, the missing inline "Retry" link
> in feedback view, and the back-button target on Q1. Wrote the README
> and SUBMISSION_GUIDE.

### What the TA will check (per HW10 spec)

- [x] Flask backend + HTML/JS/jQuery/Bootstrap frontend — yes
- [x] Home screen with Start button — `/`
- [x] Backend stores user choices on every page — `user_data.json`
      tracks `lesson_visits` (every page load), `quiz_answers`, and
      start/finish timestamps
- [x] Data lives in JSON, not hard-coded into HTML — `data/lessons.json`
      and `data/quiz.json` drive everything
- [x] ~4 routes: home, `/learn/<n>`, `/quiz/<n>`, results — all present
- [x] Each page shows data + instructions + records data + advances — yes
- [x] Quiz produces an end score — `/results` reports
      `correct_count / total`
- [ ] Everyone in the group must check something in — each member should
      push at least one commit before the TA session

---

## Running it on your laptop (TA session checklist)

```bash
# In the project folder:
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# Open http://localhost:5000/
```

If port 5000 is busy on macOS (Control Center / AirPlay Receiver), edit
the bottom of `app.py` and change `port=5000` to `port=5001`.
