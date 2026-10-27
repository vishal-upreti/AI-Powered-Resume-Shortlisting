import unittest

from matcher import analyze_candidates, _contains_phrase


class MatcherTests(unittest.TestCase):
    def setUp(self):
        self.candidates = [
            {
                "name": "Python Candidate",
                "filename": "python_candidate.pdf",
                "text": "Python developer experienced with SQL, Flask, Git, and REST API development.",
            },
            {
                "name": "Design Candidate",
                "filename": "design_candidate.docx",
                "text": "Designer experienced in Figma, UI/UX, branding, and visual design.",
            },
        ]

    def test_required_skill_candidate_scores_higher(self):
        results = analyze_candidates(
            "Junior Python developer building REST APIs with SQL and Flask.",
            self.candidates,
            "Python, SQL, Flask, Git",
        )
        self.assertEqual(len(results), 2)
        self.assertGreater(results[0]["match_score"], results[1]["match_score"])
        self.assertEqual(results[0]["skill_coverage"], 100)
        self.assertEqual(results[1]["missing_skills"], ["python", "sql", "flask", "git"])

    def test_score_is_between_zero_and_one_hundred(self):
        results = analyze_candidates("A role with Python and SQL.", self.candidates, "Python, SQL")
        for result in results:
            self.assertGreaterEqual(result["match_score"], 0)
            self.assertLessEqual(result["match_score"], 100)

    def test_without_skill_list_text_similarity_is_used(self):
        results = analyze_candidates("Python developer using Flask and SQL.", self.candidates, "")
        python_candidate = next(item for item in results if item["name"] == "Python Candidate")
        self.assertIsNone(python_candidate["skill_coverage"])
        self.assertEqual(python_candidate["match_score"], python_candidate["text_similarity"])

    def test_skill_phrase_matching_avoids_substring_accidents(self):
        self.assertTrue(_contains_phrase("Experience in C++ development", "c++"))
        self.assertFalse(_contains_phrase("strong communication skills", "c"))


if __name__ == "__main__":
    unittest.main()
