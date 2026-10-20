import unittest

from llm_eval_security.evaluator import evaluate_case, evaluate_suite


class EvaluatorTests(unittest.TestCase):
    def test_valid_citation_and_evidence_pass(self):
        case = {"id": "a", "context": [{"id": "s1", "text": "Logs expire after 30 days."}],
                "answer": "Logs expire after 30 days. [s1]", "expect": {"must_cite": True}}
        result = evaluate_case(case)
        self.assertTrue(result.passed)

    def test_unknown_citation_fails(self):
        result = evaluate_case({"id": "b", "context": [{"id": "s1", "text": "A document."}],
                                "answer": "It says hello. [wrong]"})
        self.assertFalse(result.checks["citations_valid"])

    def test_expected_refusal_is_explicit(self):
        case = {"id": "c", "context": [], "answer": "No.", "expect": {"must_refuse": True}}
        self.assertFalse(evaluate_case(case).passed)
        case["response_meta"] = {"refused": True}
        self.assertTrue(evaluate_case(case).passed)

    def test_suite_reports_rates(self):
        report = evaluate_suite([{"id": "x", "context": [], "answer": "ok"}])
        self.assertEqual(report["total"], 1)
        self.assertEqual(report["pass_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
