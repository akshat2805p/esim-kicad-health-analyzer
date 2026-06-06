"""
AI Review Engine for PCB Health Analyzer

Provides rule-based reasoning to analyze PCB board statistics,
detect design issues, generate natural-language explanations,
produce prioritized recommendations, and assess fabrication readiness.

This module forms the intelligence layer of the AI PCB Knowledge Assistant.
"""


class AIReviewEngine:
    """
    Rule-based AI engine that analyzes PCB statistics and produces
    structured insights including issues, explanations, recommendations,
    quality assessment, and fabrication readiness verdict.
    """

    # ------------------------------------------------------------------ #
    #  Quality thresholds                                                  #
    # ------------------------------------------------------------------ #

    QUALITY_THRESHOLDS = {
        "excellent": 90,
        "good": 75,
        "moderate": 60,
        "poor": 0,
    }

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def analyze(self, board_stats):
        """
        Run the full AI review pipeline on the given board statistics.

        Parameters
        ----------
        board_stats : dict
            Expected keys (all optional — missing keys default to 0):
                tracks            – int
                vias              – int
                health_score      – int (0-100)
                unconnected_pads  – int
                drc_errors        – int   (overlaps / violations)
                thin_tracks       – int
                small_vias        – int
                footprints        – int
                total_nets        – int
                copper_layers     – int
                complexity_score  – int

        Returns
        -------
        dict with keys:
            quality_level        – str   ("Excellent" / "Good" / …)
            issues               – list[dict]  each with 'title' & 'explanation'
            recommendations      – list[str]
            fabrication_status   – str   ("READY" / "NEEDS IMPROVEMENT")
            fabrication_details  – str   (human-readable reason)
            summary_text         – str   (one-line overall assessment)
        """

        stats = self._normalise(board_stats)

        issues = self._detect_issues(stats)
        recommendations = self._build_recommendations(stats, issues)
        quality = self._assess_quality(stats["health_score"])
        fab_status, fab_details = self._check_fabrication(stats)
        summary = self._build_summary(stats, quality, issues)

        return {
            "quality_level": quality,
            "issues": issues,
            "recommendations": recommendations,
            "fabrication_status": fab_status,
            "fabrication_details": fab_details,
            "summary_text": summary,
        }

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _normalise(raw):
        """Return a copy with guaranteed integer keys."""
        defaults = {
            "tracks": 0,
            "vias": 0,
            "health_score": 0,
            "unconnected_pads": 0,
            "drc_errors": 0,
            "thin_tracks": 0,
            "small_vias": 0,
            "footprints": 0,
            "total_nets": 0,
            "copper_layers": 0,
            "complexity_score": 0,
        }
        out = dict(defaults)
        out.update({k: v for k, v in raw.items() if k in defaults})
        return out

    # ---- Issue detection (Task 2) ------------------------------------ #

    def _detect_issues(self, stats):
        """Apply rule-based checks and return a list of issue dicts."""

        issues = []

        # Rule 1 – Unconnected pads
        if stats["unconnected_pads"] > 0:
            issues.append({
                "title": "Unconnected Pads",
                "explanation": (
                    f"{stats['unconnected_pads']} unconnected pad(s) detected. "
                    "Unconnected pads may result in open circuits and board "
                    "malfunction. Every pad should be connected to its "
                    "intended net before fabrication."
                ),
            })

        # Rule 2 – DRC violations (overlaps)
        if stats["drc_errors"] > 0:
            issues.append({
                "title": "DRC Violations",
                "explanation": (
                    f"{stats['drc_errors']} DRC violation(s) detected. "
                    "DRC violations indicate that the design may fail "
                    "manufacturing constraints such as minimum clearance, "
                    "minimum annular ring, or track spacing rules."
                ),
            })

        # Rule 3 – High via-to-track ratio
        if stats["tracks"] > 0 and stats["vias"] > stats["tracks"] * 0.4:
            issues.append({
                "title": "High Via Density",
                "explanation": (
                    f"Via count ({stats['vias']}) exceeds 40% of track count "
                    f"({stats['tracks']}). High via density may increase "
                    "manufacturing complexity, raise production costs, and "
                    "degrade signal integrity due to additional layer transitions."
                ),
            })

        # Rule 4 – Thin tracks
        if stats["thin_tracks"] > 0:
            issues.append({
                "title": "Thin Tracks Detected",
                "explanation": (
                    f"{stats['thin_tracks']} track(s) below recommended minimum "
                    "width (< 0.25 mm). Thin tracks can cause signal integrity "
                    "issues and may not survive the etching process during "
                    "manufacturing."
                ),
            })

        # Rule 5 – Small vias
        if stats["small_vias"] > 0:
            issues.append({
                "title": "Small Via Drill Sizes",
                "explanation": (
                    f"{stats['small_vias']} via(s) with drill size below 0.4 mm. "
                    "Very small vias increase drilling difficulty and may lead "
                    "to unreliable barrel plating."
                ),
            })

        # Rule 6 – Extremely low track count (possible incomplete routing)
        if 0 < stats["tracks"] < 20:
            issues.append({
                "title": "Low Track Count",
                "explanation": (
                    f"Only {stats['tracks']} tracks found. This may indicate "
                    "incomplete routing. Verify that all nets are fully routed "
                    "before proceeding."
                ),
            })

        return issues

    # ---- Recommendations --------------------------------------------- #

    def _build_recommendations(self, stats, issues):
        """Generate prioritised list of actionable recommendations."""

        recs = []
        issue_titles = {i["title"] for i in issues}

        # Always recommend DRC if there are any violations or unconnected pads
        if "DRC Violations" in issue_titles or "Unconnected Pads" in issue_titles:
            recs.append("Run DRC (Design Rule Check) and fix all violations before fabrication.")

        if "Unconnected Pads" in issue_titles:
            recs.append(
                "Review the netlist and ensure every pad is connected to "
                "its intended net. Use the ratsnest display to locate open connections."
            )

        if "High Via Density" in issue_titles:
            recs.append(
                "Reduce unnecessary layer transitions by optimising trace routing. "
                "Consider re-routing critical nets on fewer layers."
            )

        if "Thin Tracks Detected" in issue_titles:
            recs.append(
                "Increase track widths to at least 0.25 mm (10 mil). "
                "Use wider tracks for power nets to improve current-carrying capacity."
            )

        if "Small Via Drill Sizes" in issue_titles:
            recs.append(
                "Increase via drill sizes to at least 0.4 mm to improve "
                "manufacturing yield and reliability."
            )

        if "Low Track Count" in issue_titles:
            recs.append(
                "Complete the routing of all nets. Use the DRC to identify "
                "any remaining unrouted connections."
            )

        # General best-practice recommendations
        recs.append("Review power and ground routing for adequate copper width.")
        recs.append("Perform a final visual inspection of the board layout before generating Gerber files.")

        return recs

    # ---- Quality assessment ------------------------------------------ #

    def _assess_quality(self, score):
        """Map health score to a human-readable quality level."""
        if score >= self.QUALITY_THRESHOLDS["excellent"]:
            return "Excellent Quality"
        if score >= self.QUALITY_THRESHOLDS["good"]:
            return "Good Quality"
        if score >= self.QUALITY_THRESHOLDS["moderate"]:
            return "Moderate Quality"
        return "Poor Quality"

    # ---- Fabrication readiness (Task 4) ------------------------------ #

    @staticmethod
    def _check_fabrication(stats):
        """
        Determine fabrication readiness.

        READY  – only when drc_errors == 0 AND unconnected_pads == 0
        NEEDS IMPROVEMENT – otherwise
        """

        if stats["drc_errors"] == 0 and stats["unconnected_pads"] == 0:
            return (
                "READY",
                "No DRC violations and no unconnected pads detected. "
                "The board meets minimum fabrication criteria.",
            )

        reasons = []
        if stats["drc_errors"] > 0:
            reasons.append(f"{stats['drc_errors']} DRC violation(s)")
        if stats["unconnected_pads"] > 0:
            reasons.append(f"{stats['unconnected_pads']} unconnected pad(s)")

        return (
            "NEEDS IMPROVEMENT",
            "The board is not ready for fabrication due to: "
            + "; ".join(reasons) + ". Fix these issues and re-run the analysis.",
        )

    # ---- Summary builder --------------------------------------------- #

    @staticmethod
    def _build_summary(stats, quality, issues):
        """One-line human-readable summary."""
        n = len(issues)
        if n == 0:
            return (
                f"The board scores {stats['health_score']}/100 — {quality}. "
                "No significant issues were detected."
            )
        return (
            f"The board scores {stats['health_score']}/100 — {quality}. "
            f"{n} issue(s) require attention before fabrication."
        )
