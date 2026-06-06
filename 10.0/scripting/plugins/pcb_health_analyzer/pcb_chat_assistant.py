"""
PCB Chat Assistant for KiCad / eSim

Provides an interactive question-and-answer interface that generates
human-readable analysis summaries and answers predefined questions
about PCB design quality, health score breakdowns, and fabrication
readiness.

Uses AIReviewEngine internally for all reasoning.
"""

# pyrefly: ignore [missing-import]
from .ai_review_engine import AIReviewEngine


class PCBChatAssistant:
    """
    High-level assistant that transforms raw board statistics into
    natural-language reports and answers common PCB review questions.
    """

    # Predefined questions the assistant can answer
    SUPPORTED_QUESTIONS = [
        "Why is my health score low?",
        "What are the major issues?",
        "How can I improve the board?",
        "Is this board ready for fabrication?",
    ]

    def __init__(self):
        self._engine = AIReviewEngine()

    # ------------------------------------------------------------------ #
    #  Task 1 — Full analysis response                                    #
    # ------------------------------------------------------------------ #

    def generate_response(self, board_stats):
        """
        Generate a complete natural-language PCB analysis summary.

        Parameters
        ----------
        board_stats : dict
            Board statistics (tracks, vias, health_score,
            unconnected_pads, drc_errors, …).

        Returns
        -------
        str   Multi-line human-readable report.
        """

        review = self._engine.analyze(board_stats)

        lines = []
        lines.append("=" * 50)
        lines.append("         PCB ANALYSIS SUMMARY")
        lines.append("=" * 50)
        lines.append("")
        lines.append(review["summary_text"])
        lines.append("")

        # Issues section
        if review["issues"]:
            lines.append("ISSUES FOUND:")
            lines.append("-" * 40)
            for issue in review["issues"]:
                lines.append(f"  * {issue['title']}")
                lines.append(f"    {issue['explanation']}")
                lines.append("")
        else:
            lines.append("ISSUES FOUND:")
            lines.append("-" * 40)
            lines.append("  No significant issues detected.")
            lines.append("")

        # Recommendations section
        lines.append("RECOMMENDATIONS:")
        lines.append("-" * 40)
        for idx, rec in enumerate(review["recommendations"], 1):
            lines.append(f"  {idx}. {rec}")
        lines.append("")

        # Fabrication readiness
        lines.append("FABRICATION STATUS:")
        lines.append("-" * 40)
        lines.append(f"  Status  : {review['fabrication_status']}")
        lines.append(f"  Details : {review['fabrication_details']}")
        lines.append("")
        lines.append("=" * 50)

        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  Task 3 — Interactive question system                               #
    # ------------------------------------------------------------------ #

    def answer_question(self, question, board_stats):
        """
        Answer a predefined question about the PCB design.

        Parameters
        ----------
        question : str
            One of the SUPPORTED_QUESTIONS (matched case-insensitively).
        board_stats : dict
            Board statistics dict.

        Returns
        -------
        str   Human-readable answer.
        """

        review = self._engine.analyze(board_stats)
        q = question.strip().lower().rstrip("?")

        if q == "why is my health score low":
            return self._answer_health_score(board_stats, review)
        elif q == "what are the major issues":
            return self._answer_major_issues(review)
        elif q == "how can i improve the board":
            return self._answer_improvements(review)
        elif q == "is this board ready for fabrication":
            return self._answer_fabrication(review)
        else:
            return (
                "Sorry, I can only answer the following questions:\n"
                + "\n".join(f"  - {q}" for q in self.SUPPORTED_QUESTIONS)
            )

    # ------------------------------------------------------------------ #
    #  Question handlers                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _answer_health_score(stats, review):
        lines = []
        lines.append("QUESTION: Why is my health score low?")
        lines.append("")

        score = stats.get("health_score", 0)
        lines.append(f"Your current health score is {score}/100.")
        lines.append("")

        if not review["issues"]:
            lines.append("No specific issues are reducing your score.")
            return "\n".join(lines)

        lines.append("The score is reduced due to:")
        for issue in review["issues"]:
            lines.append(f"  * {issue['title']}")
        lines.append("")
        lines.append(
            "Addressing the issues listed above will improve your health score."
        )
        return "\n".join(lines)

    @staticmethod
    def _answer_major_issues(review):
        lines = []
        lines.append("QUESTION: What are the major issues?")
        lines.append("")

        if not review["issues"]:
            lines.append("No major issues were detected. Your board looks good!")
            return "\n".join(lines)

        lines.append(f"{len(review['issues'])} issue(s) detected:")
        lines.append("")
        for issue in review["issues"]:
            lines.append(f"  * {issue['title']}")
            lines.append(f"    {issue['explanation']}")
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _answer_improvements(review):
        lines = []
        lines.append("QUESTION: How can I improve the board?")
        lines.append("")

        if not review["recommendations"]:
            lines.append("No specific improvements needed — great work!")
            return "\n".join(lines)

        lines.append("Recommended improvements:")
        lines.append("")
        for idx, rec in enumerate(review["recommendations"], 1):
            lines.append(f"  {idx}. {rec}")
        return "\n".join(lines)

    @staticmethod
    def _answer_fabrication(review):
        lines = []
        lines.append("QUESTION: Is this board ready for fabrication?")
        lines.append("")
        lines.append(f"Fabrication Status: {review['fabrication_status']}")
        lines.append("")
        lines.append(review["fabrication_details"])
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  Utility                                                             #
    # ------------------------------------------------------------------ #

    def get_ai_review(self, board_stats):
        """
        Return the raw AI review dict for use by other modules
        (e.g. HTML report, knowledge file export).
        """
        return self._engine.analyze(board_stats)
