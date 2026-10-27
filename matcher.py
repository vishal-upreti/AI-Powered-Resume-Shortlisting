
import re
import math
from collections import Counter
from typing import Any


SKILL_BANK = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql",
    "mysql", "postgresql", "sqlite", "html", "css", "react", "angular",
    "vue", "node.js", "flask", "django", "fastapi", "spring boot",
    "rest api", "api development", "git", "github", "linux", "docker",
    "kubernetes", "aws", "azure", "google cloud", "machine learning",
    "deep learning", "natural language processing", "nlp", "data analysis",
    "data visualization", "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "excel", "power bi", "tableau", "statistics",
    "problem solving", "communication", "teamwork", "project management",
    "agile", "scrum", "software testing", "unit testing", "selenium",
    "computer networks", "operating systems", "data structures",
    "algorithms", "object-oriented programming", "oop", "cybersecurity",
    "network security", "cloud computing", "salesforce", "figma", "ui/ux",
]


def _normalise_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _contains_phrase(text: str, phrase: str) -> bool:
    phrase = _normalise_text(phrase)
    if not phrase:
        return False

    escaped = re.escape(phrase).replace(r"\ ", r"\s+")
    pattern = r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _extract_skills(text: str, skill_list: list[str]) -> list[str]:
    normalized = _normalise_text(text)
    found = [
        skill for skill in skill_list
        if _contains_phrase(normalized, skill)
    ]
    return sorted(set(found), key=str.lower)


def _parse_required_skills(raw_skills: str) -> list[str]:
    supplied = [
        item.strip().lower()
        for item in re.split(r"[,;\n]+", raw_skills)
        if item.strip()
    ]
    return list(dict.fromkeys(supplied))


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[+#.][a-z0-9+#.]*)*", text.lower())


def _make_terms(tokens: list[str]) -> list[str]:
    terms = list(tokens)
    terms.extend(
        tokens[i] + " " + tokens[i + 1]
        for i in range(len(tokens) - 1)
    )
    return terms


def _similarity_scores(documents: list[str]) -> list[float]:
    """Calculate TF-IDF cosine similarity using Python's standard library."""
    tokenized = [_make_terms(_tokenize(doc)) for doc in documents]
    document_count = len(tokenized)

    document_frequency = Counter()
    for terms in tokenized:
        document_frequency.update(set(terms))

    vectors = []
    for terms in tokenized:
        frequencies = Counter(terms)
        vector = {}

        for term, count in frequencies.items():
            tf = count / len(terms) if terms else 0.0
            idf = math.log(
                (1 + document_count) /
                (1 + document_frequency[term])
            ) + 1
            vector[term] = tf * idf

        magnitude = math.sqrt(sum(value ** 2 for value in vector.values()))
        if magnitude:
            vector = {
                term: value / magnitude
                for term, value in vector.items()
            }

        vectors.append(vector)

    job_vector = vectors[0]
    scores = []

    for candidate_vector in vectors[1:]:
        score = sum(
            value * candidate_vector.get(term, 0.0)
            for term, value in job_vector.items()
        )
        scores.append(max(0.0, min(1.0, score)))

    return scores


def analyze_candidates(
    job_text: str,
    candidates: list[dict[str, Any]],
    raw_required_skills: str,
) -> list[dict[str, Any]]:
    """Rank resumes using text similarity and required-skill coverage."""
    required_skills = _parse_required_skills(raw_required_skills)
    skill_reference = list(dict.fromkeys(SKILL_BANK + required_skills))

    documents = [job_text] + [
        candidate["text"] for candidate in candidates
    ]
    text_scores = _similarity_scores(documents)

    results = []

    for candidate, similarity in zip(candidates, text_scores):
        resume_text = candidate["text"]
        normalized_resume = _normalise_text(resume_text)
        detected_skills = _extract_skills(
            resume_text, skill_reference
        )

        if required_skills:
            matched_required = [
                skill for skill in required_skills
                if _contains_phrase(normalized_resume, skill)
            ]
            missing_required = [
                skill for skill in required_skills
                if skill not in matched_required
            ]
            coverage = len(matched_required) / len(required_skills)
            score = (0.65 * similarity) + (0.35 * coverage)
        else:
            matched_required = []
            missing_required = []
            coverage = None
            score = similarity

        results.append({
            "name": candidate["name"],
            "filename": candidate["filename"],
            "match_score": round(score * 100),
            "text_similarity": round(similarity * 100),
            "skill_coverage": (
                round(coverage * 100)
                if coverage is not None else None
            ),
            "matched_skills": (
                matched_required if required_skills else detected_skills
            ),
            "detected_skills": detected_skills,
            "missing_skills": missing_required,
            "resume_characters": len(resume_text),
        })

    return results
