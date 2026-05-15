import json
import os
from datetime import datetime
from pathlib import Path

from flask import (
    Flask, render_template, request, redirect, url_for, jsonify, abort
)

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
USER_DATA_PATH = BASE_DIR / "user_data.json"

app = Flask(__name__)


# ---------- Data loading ----------

def load_lessons():
    """Reload from disk each call so editing JSON doesn't require restart."""
    with open(DATA_DIR / "lessons.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_quiz():
    with open(DATA_DIR / "quiz.json", "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- User-data persistence ----------

def _empty_session():
    return {
        "started_at": None,
        "lesson_visits": [],   # [{lesson_num, ts}]
        "quiz_answers": [],    # [{q_num, choice, correct, ts}]
        "finished_at": None,
    }


def load_user_data():
    if not USER_DATA_PATH.exists():
        return _empty_session()
    try:
        with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return _empty_session()


def save_user_data(data):
    with open(USER_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def reset_user_data():
    save_user_data(_empty_session())


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


# ---------- Routes ----------

@app.route("/")
def home():
    """Home / welcome page with Start button."""
    lessons = load_lessons()
    return render_template(
        "home.html",
        topic=lessons["topic"],
    )


@app.route("/start", methods=["POST"])
def start():
    """User clicked Start: reset the session and record start time."""
    data = _empty_session()
    data["started_at"] = now_iso()
    save_user_data(data)
    return redirect(url_for("learn", lesson_num=1))


@app.route("/learn/<int:lesson_num>")
def learn(lesson_num):
    """Render lesson page N. Records the visit on the backend."""
    lessons = load_lessons()
    total = lessons["total_lessons"]

    if lesson_num < 1 or lesson_num > total:
        abort(404)

    lesson = next(
        (l for l in lessons["lessons"] if l["id"] == lesson_num),
        None,
    )
    if lesson is None:
        abort(404)

    # Record the visit
    data = load_user_data()
    data["lesson_visits"].append({
        "lesson_num": lesson_num,
        "ts": now_iso(),
    })
    save_user_data(data)

    # Build pagination dots
    dots_total = total
    return render_template(
        "learn.html",
        lesson=lesson,
        lesson_num=lesson_num,
        total_lessons=total,
        dots_total=dots_total,
        topic=lessons["topic"],
        prev_url=(url_for("learn", lesson_num=lesson_num - 1)
                  if lesson_num > 1 else url_for("home")),
        next_url=(url_for("learn", lesson_num=lesson_num + 1)
                  if lesson_num < total else url_for("quiz", q_num=1)),
        is_last=(lesson_num == total),
        is_first=(lesson_num == 1),
    )


@app.route("/quiz/<int:q_num>")
def quiz(q_num):
    """Render quiz question N."""
    quiz_data = load_quiz()
    total = quiz_data["total_questions"]

    if q_num < 1 or q_num > total:
        abort(404)

    question = next(
        (q for q in quiz_data["questions"] if q["id"] == q_num),
        None,
    )
    if question is None:
        abort(404)

    return render_template(
        "quiz.html",
        question=question,
        q_num=q_num,
        total_questions=total,
        is_last=(q_num == total),
    )


@app.route("/api/quiz/answer", methods=["POST"])
def quiz_answer():
    """Receive a quiz answer, record it, return feedback payload."""
    payload = request.get_json(silent=True) or {}
    q_num = payload.get("q_num")
    choice = payload.get("choice")

    if q_num is None or choice is None:
        return jsonify({"error": "missing q_num or choice"}), 400

    quiz_data = load_quiz()
    question = next(
        (q for q in quiz_data["questions"] if q["id"] == int(q_num)),
        None,
    )
    if question is None:
        return jsonify({"error": "unknown question"}), 404

    correct = (choice == question["correct"])
    fb_key = "correct" if correct else "incorrect"

    # Persist the answer
    data = load_user_data()
    data["quiz_answers"].append({
        "q_num": int(q_num),
        "choice": choice,
        "correct": correct,
        "ts": now_iso(),
    })
    save_user_data(data)

    return jsonify({
        "correct": correct,
        "correct_choice": question["correct"],
        "feedback": question["feedback"][fb_key],
        "next_url": (
            url_for("quiz", q_num=int(q_num) + 1)
            if int(q_num) < quiz_data["total_questions"]
            else url_for("results")
        ),
        "is_last": int(q_num) == quiz_data["total_questions"],
    })


@app.route("/results")
def results():
    """Final quiz result page. Scores reflect FINAL attempts per question."""
    data = load_user_data()

    # mark session finished
    if data["finished_at"] is None:
        data["finished_at"] = now_iso()
        save_user_data(data)

    quiz_data = load_quiz()
    total = quiz_data["total_questions"]

    # Use the LAST answer per question as the final answer
    final_by_q = {}
    for ans in data["quiz_answers"]:
        final_by_q[ans["q_num"]] = ans

    correct_count = sum(1 for a in final_by_q.values() if a["correct"])

    # Build a per-question summary in question order
    summary = []
    for q in quiz_data["questions"]:
        ans = final_by_q.get(q["id"])
        summary.append({
            "q_num": q["id"],
            "question": q["question"],
            "user_choice": ans["choice"] if ans else None,
            "correct_choice": q["correct"],
            "correct": ans["correct"] if ans else False,
            "answered": ans is not None,
        })

    return render_template(
        "results.html",
        correct_count=correct_count,
        total=total,
        summary=summary,
        started_at=data.get("started_at"),
        finished_at=data.get("finished_at"),
    )


@app.route("/restart", methods=["POST"])
def restart():
    """Reset everything and go home."""
    reset_user_data()
    return redirect(url_for("home"))


# ---------- Dev helpers ----------

@app.route("/api/debug/user_data")
def debug_user_data():
    """Inspect what's currently stored. Handy for testing."""
    return jsonify(load_user_data())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
