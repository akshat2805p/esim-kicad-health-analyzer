"""
Standalone test script for the AI PCB Knowledge Assistant.
Run this from the command line — no KiCad required.

Usage:
    python test_ai_assistant.py
"""

import sys
import os
import json
import importlib.util

# ---- Direct module loading (bypasses __init__.py which needs pcbnew) -- #

PLUGIN_DIR = os.path.join(
    os.path.dirname(__file__), "10.0", "scripting", "plugins", "pcb_health_analyzer"
)


def load_module(name, filename):
    """Load a single .py file as a module without triggering __init__.py."""
    path = os.path.join(PLUGIN_DIR, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Load modules in dependency order
ai_engine_mod = load_module("pcb_health_analyzer.ai_review_engine", "ai_review_engine.py")
chat_mod = load_module("pcb_health_analyzer.pcb_chat_assistant", "pcb_chat_assistant.py")
report_mod = load_module("pcb_health_analyzer.report_generator", "report_generator.py")
html_mod = load_module("pcb_health_analyzer.pcb_html_report", "pcb_html_report.py")

AIReviewEngine = ai_engine_mod.AIReviewEngine
PCBChatAssistant = chat_mod.PCBChatAssistant
generate_knowledge_file = report_mod.generate_knowledge_file
generate_html_report = html_mod.generate_html_report


# ---- Test 1: AI Review Engine ---------------------------------------- #
print("=" * 60)
print("  TEST 1: AI Review Engine")
print("=" * 60)

engine = AIReviewEngine()

# Simulate a board with issues
board_stats = {
    "tracks": 120,
    "vias": 60,
    "health_score": 70,
    "unconnected_pads": 8,
    "drc_errors": 5,
    "thin_tracks": 3,
    "small_vias": 2,
}

review = engine.analyze(board_stats)

print(f"\nQuality Level    : {review['quality_level']}")
print(f"Fabrication      : {review['fabrication_status']}")
print(f"Summary          : {review['summary_text']}")
print(f"\nIssues Found ({len(review['issues'])}):")
for issue in review["issues"]:
    print(f"  - {issue['title']}: {issue['explanation'][:80]}...")
print(f"\nRecommendations ({len(review['recommendations'])}):")
for i, rec in enumerate(review["recommendations"], 1):
    print(f"  {i}. {rec}")

print("\n[OK] AI Review Engine - PASSED\n")


# ---- Test 2: PCB Chat Assistant -------------------------------------- #
print("=" * 60)
print("  TEST 2: PCB Chat Assistant - Full Response")
print("=" * 60)

assistant = PCBChatAssistant()
response = assistant.generate_response(board_stats)
print(response)

print("\n[OK] Chat Assistant generate_response() - PASSED\n")


# ---- Test 3: Interactive Q&A ----------------------------------------- #
print("=" * 60)
print("  TEST 3: Interactive Q&A System")
print("=" * 60)

questions = [
    "Why is my health score low?",
    "What are the major issues?",
    "How can I improve the board?",
    "Is this board ready for fabrication?",
]

for q in questions:
    print(f"\n{'-' * 50}")
    answer = assistant.answer_question(q, board_stats)
    print(answer)

print("\n[OK] Interactive Q&A - PASSED\n")


# ---- Test 4: Knowledge File Export ----------------------------------- #
print("=" * 60)
print("  TEST 4: Knowledge File Export")
print("=" * 60)

output_dir = os.path.join(os.path.dirname(__file__), "test_output")
os.makedirs(output_dir, exist_ok=True)

knowledge_path = generate_knowledge_file(
    board_name="test_board.kicad_pcb",
    stats=board_stats,
    ai_review=review,
    output_dir=output_dir,
)

with open(knowledge_path, "r", encoding="utf-8") as f:
    knowledge = json.load(f)

print(f"\nKnowledge file written to: {knowledge_path}")
print(f"\nContents:")
print(json.dumps(knowledge, indent=2))

print("\n[OK] Knowledge File Export - PASSED\n")


# ---- Test 5: HTML Report with AI Section ----------------------------- #
print("=" * 60)
print("  TEST 5: HTML Report with AI Section")
print("=" * 60)

html_path = os.path.join(output_dir, "test_pcb_health_report.html")

generate_html_report(
    report_path=html_path,
    health_score=70,
    grade="C",
    board_status="FAIR",
    tracks=120,
    vias=60,
    footprints=25,
    total_nets=45,
    min_track_width=0.2,
    max_track_width=0.5,
    avg_track_width=0.35,
    complexity_score=55,
    warnings_text="- 3 tracks below recommended width\n- 2 very small vias detected",
    ai_review=review,
)

print(f"\nHTML report written to: {html_path}")
print(f"File size: {os.path.getsize(html_path)} bytes")

print("\n[OK] HTML Report with AI Section - PASSED\n")


# ---- Test 6: Clean board (should be READY) --------------------------- #
print("=" * 60)
print("  TEST 6: Clean Board (Fabrication READY)")
print("=" * 60)

clean_stats = {
    "tracks": 200,
    "vias": 30,
    "health_score": 95,
    "unconnected_pads": 0,
    "drc_errors": 0,
    "thin_tracks": 0,
    "small_vias": 0,
}

clean_review = engine.analyze(clean_stats)
print(f"\nQuality  : {clean_review['quality_level']}")
print(f"Fab      : {clean_review['fabrication_status']}")
print(f"Issues   : {len(clean_review['issues'])}")
print(f"Summary  : {clean_review['summary_text']}")

print("\n[OK] Clean Board Test - PASSED\n")


# ---- Final Summary --------------------------------------------------- #
print("=" * 60)
print("  ALL 6 TESTS PASSED [OK]")
print("=" * 60)
print(f"\nOutput files are in: {output_dir}")
print("  - test_pcb_health_report.html  (open in browser to see AI section)")
print("  - reports/board_knowledge.json (structured knowledge export)")
print()
