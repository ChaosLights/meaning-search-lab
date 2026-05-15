# Meaning Search Lab — Technical Prototype (HW10)

COMS W4170 — Group project (Can Wu, Tianjun Zhong, Chengtao Dai)
TA: Daniel Alejandro Manjarrez

A clickable web app teaching **why semantic search matches meaning, not just shared
words**. Implements the iterated low-fi prototype from HW9 as a working Flask
application.

## Quick start

```bash
# 1. Clone & enter
git clone <repo-url>
cd meaning-search-lab

# 2. (Optional) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Then open <http://localhost:5000/>.

To reset all stored user data, click **Restart lesson** on the results page, or
just delete `user_data.json`.

## What the app does

- **Home** (`/`) — welcome screen with the example query and a Start button.
- **Lessons** (`/learn/1` … `/learn/7`) — seven lesson states matching the
  HW9 slides (Two Ways to Search → Keyword Ranking → Synonym demo → Embed
  query → Embed documents → Score & rank → Recap).
- **Quiz** (`/quiz/1`, `/quiz/2`) — two multiple-choice questions.
  Answers are submitted via AJAX; correct/incorrect feedback renders inline.
- **Results** (`/results`) — final score with per-question summary.

## How HW10 requirements are met

| Requirement                                              | Where                                  |
| -------------------------------------------------------- | -------------------------------------- |
| Flask backend + HTML/JS/jQuery/Bootstrap frontend        | `app.py` + `templates/` + `static/`    |
| Home screen with start button                            | `templates/home.html` → `POST /start`  |
| Backend stores user choices on every page                | `user_data.json` (lesson visits, quiz answers, timestamps) |
| Data driven by JSON, **not** hard-coded into HTML        | `data/lessons.json`, `data/quiz.json`  |
| ~4 routes: home, `/learn/<n>`, `/quiz/<n>`, results      | All present in `app.py`                |
| Each page shows data + instructions + records data + advances | every template has nav + JSON-driven content |
| Quiz returns a score at the end                          | `/results` computes from `user_data.json` |
| Single user at a time (simple file storage OK)           | Yes — single `user_data.json`          |

## Project structure

```
meaning-search-lab/
├── app.py                  # Flask backend (all routes)
├── data/
│   ├── lessons.json        # 7 lessons, content + layout hints
│   └── quiz.json           # 2 questions + correct/incorrect feedback
├── static/
│   ├── css/style.css       # Navy + teal palette inherited from HW9
│   └── js/main.js          # jQuery: option selection, AJAX submit, feedback
├── templates/
│   ├── base.html           # Bootstrap 5 + jQuery layout
│   ├── home.html
│   ├── learn.html          # dispatches by lesson type
│   ├── quiz.html
│   └── results.html
├── requirements.txt
└── README.md
```

## Data architecture

Two JSON files drive the entire app:

### `data/lessons.json`
Each lesson has an `id`, a `type` (e.g. `two_ways`, `keyword_ranking`,
`synonym_demo`, `embed_query`, `embed_documents`, `score_rank`, `recap`)
and the content specific to that type. The single `learn.html` template
dispatches on `lesson.type` to render the right layout. Add a lesson by
appending a new object and bumping `total_lessons`.

### `data/quiz.json`
Each question has `options`, the `correct` choice, and feedback bundles
for both correct and incorrect answers. Add a question by appending and
bumping `total_questions`.

### `user_data.json` (auto-generated)
Created on first Start. Tracks:
- `started_at` — ISO timestamp when the user pressed Start
- `lesson_visits` — list of `{lesson_num, ts}` rows, one per page load
- `quiz_answers` — list of `{q_num, choice, correct, ts}` rows
- `finished_at` — ISO timestamp when the results page first loaded

You can inspect it live at <http://localhost:5000/api/debug/user_data>.

## Roles (HW10 warm-up #4)

| Role                                  | Owner            |
| ------------------------------------- | ---------------- |
| Learning portion — data architecture  | Can Wu           |
| Learning portion — UI implementation  | Can Wu           |
| Learning portion — click-through test | Tianjun Zhong    |
| Quiz portion — data architecture      | Chengtao Dai     |
| Quiz portion — UI implementation      | Chengtao Dai     |
| Quiz portion — click-through test     | Tianjun Zhong    |

(Three-person group, so some members hold two roles per the HW10 spec.)
