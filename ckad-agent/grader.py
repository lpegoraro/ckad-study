import re
import json
import string
from typing import List, Dict, Tuple

STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "with", "on", "for",
    "is", "use", "should", "be", "that", "by", "as", "it"
}


def normalize_text(s: str) -> str:
    s = s.lower()
    s = s.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_keywords(text: str) -> List[str]:
    norm = normalize_text(text)
    terms = [t for t in norm.split() if t and t not in STOPWORDS]
    return terms


def parse_quiz_markdown(path: str) -> List[Dict]:
    """Parse a simple quiz markdown into questions with expected answer bullets.

    Expected format (like `quizzes/mock-quiz-1.md`):
    1. Question text

    Answer:
    - hint 1
    - hint 2
    """
    with open(path, "r") as f:
        lines = f.read().splitlines()

    questions = []
    q_num = 0
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m:
            q_num += 1
            prompt = m.group(2).strip()
            expected = []
            # advance to find 'Answer:'
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i < len(lines) and lines[i].strip().lower().startswith("answer"):
                i += 1
                # collect bullets
                while i < len(lines):
                    ln = lines[i].strip()
                    if re.match(r"^-\s+", ln):
                        expected.append(ln[1:].strip())
                        i += 1
                        continue
                    # stop on next question or blank line followed by digit.
                    if re.match(r"^(\d+)\.\s+", ln):
                        break
                    if ln == "":
                        i += 1
                        # lookahead for next question
                        if i < len(lines) and re.match(r"^(\d+)\.\s+", lines[i].strip()):
                            break
                        continue
                    i += 1
            questions.append({"id": f"q{q_num}", "prompt": prompt, "expected": expected})
            continue
        i += 1

    return questions


def grade_expected_bullets(expected: List[str], user_answer: str) -> Tuple[float, List[str]]:
    """Score a list of expected bullets against the user's answer.

    Returns (score_fraction, missing_bullets).
    Each expected bullet is considered 1 point; a bullet is matched if at least one
    significant keyword from it appears in the user answer.
    """
    if not expected:
        return 1.0, []

    user_norm = normalize_text(user_answer)
    user_terms = set(user_norm.split())

    missing = []
    matched = 0
    for bullet in expected:
        keys = extract_keywords(bullet)
        if not keys:
            # if no keywords, treat as matched
            matched += 1
            continue
        found = any(k in user_terms for k in keys)
        if found:
            matched += 1
        else:
            missing.append(bullet)

    score = matched / len(expected)
    return score, missing


def grade_quiz(quiz_path: str, answers: Dict[str, str]) -> Dict:
    quiz = parse_quiz_markdown(quiz_path)
    results = {"per_question": [], "total": {}}
    total_points = 0
    total_scored = 0.0
    for q in quiz:
        qid = q["id"]
        expected = q.get("expected", [])
        user_ans = answers.get(qid, "")
        score_frac, missing = grade_expected_bullets(expected, user_ans)
        points = len(expected)
        total_points += points
        total_scored += score_frac * points
        results["per_question"].append({
            "id": qid,
            "prompt": q["prompt"],
            "score_fraction": score_frac,
            "points": points,
            "missing": missing,
            "user_answer": user_ans,
        })

    overall = (total_scored / total_points) if total_points else 1.0
    results["total"] = {"points": total_points, "scored": total_scored, "fraction": overall}
    return results


def pretty_feedback(results: Dict) -> str:
    lines = []
    for q in results["per_question"]:
        lines.append(f"{q['id']}: {q['prompt']}")
        lines.append(f"  Score: {q['score_fraction']*100:.0f}% ({q['points']} pts)")
        if q['missing']:
            lines.append("  Missing key points:")
            for b in q['missing']:
                lines.append(f"   - {b}")
        lines.append("")
    t = results["total"]
    lines.append(f"Overall: {t['fraction']*100:.0f}% ({t['scored']:.1f}/{t['points']})")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python grader.py <quiz.md> <answers.json>")
        sys.exit(2)
    quiz = sys.argv[1]
    ansf = sys.argv[2]
    with open(ansf) as fh:
        answers = json.load(fh)
    res = grade_quiz(quiz, answers)
    print(pretty_feedback(res))
