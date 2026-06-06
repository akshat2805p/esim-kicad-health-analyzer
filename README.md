# eSim KiCad Health Analyzer — AI PCB Knowledge Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![KiCad: 6.0+](https://img.shields.io/badge/KiCad-6.0+-red.svg)](https://www.kicad.org/)
[![AI Assisted](https://img.shields.io/badge/AI-Assisted%20Analysis-blueviolet)](.)

A comprehensive suite of Python-based KiCad automation plugins and utilities developed for the **FOSSEE eSim** project. This repository contains production-ready tools for PCB analysis, design validation, report generation, and an **AI-powered Knowledge Assistant** that explains issues, recommends fixes, answers questions, and assesses fabrication readiness — all integrated with KiCad 10.0's Python API ecosystem.

**Repository Owner:** [akshat2805p](https://github.com/akshat2805p)  
**For:** FOSSEE eSim Open Source Contributions

---

## 📋 Table of Contents

- [Overview](#overview)
- [What Makes This Different](#what-makes-this-different)
- [Quick Start](#quick-start)
- [Modules & Tools](#modules--tools)
- [AI PCB Knowledge Assistant (Day 12)](#-ai-pcb-knowledge-assistant-day-12)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This repository provides a complete ecosystem of KiCad plugins and Python utilities for automating PCB design workflows. The tools enable engineers to:

✅ Analyze PCB health and design quality  
✅ Generate comprehensive inspection reports (TXT, HTML, JSON)  
✅ Detect design rule violations  
✅ Automate component verification  
✅ Create formatted design documentation  
✅ **Get AI-assisted explanations of PCB issues**  
✅ **Receive intelligent design recommendations**  
✅ **Ask questions about board quality interactively**  
✅ **Check fabrication readiness automatically**  
✅ **Export structured knowledge files for future LLM integration**

All modules are designed to integrate seamlessly with KiCad 6.0+ and leverage the `pcbnew` Python API for native board manipulation.

---

## 🚀 What Makes This Different

Most internship projects stop at:

```
Analyze → Generate Report
```

This project goes further with a full AI-assisted pipeline:

```
Analyze → Explain → Recommend → Answer Questions → Assess Fabrication
```

The AI PCB Knowledge Assistant transforms raw board statistics into actionable intelligence, making this tool feel much closer to a professional AI-assisted EDA tool than a traditional PCB analyser.

---

## ⚡ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/akshat2805p/FOSSEE-eSim-Tasks.git
cd FOSSEE-eSim-Tasks

# Navigate to KiCad plugins directory
cd 10.0/scripting/plugins/
```

### Using as KiCad Plugins

1. **Copy plugins to KiCad directory:**
   ```bash
   # Linux/macOS
   cp -r pcb_health_analyzer/ ~/.local/share/kicad/6.0/scripting/plugins/
   cp -r advanced_pcb_checker/ ~/.local/share/kicad/6.0/scripting/plugins/

   # Windows
   xcopy pcb_health_analyzer\ %APPDATA%\kicad\6.0\scripting\plugins\
   xcopy advanced_pcb_checker\ %APPDATA%\kicad\6.0\scripting\plugins\
   ```

2. **Refresh plugins in KiCad:**
   - Open KiCad PCB Editor
   - Navigate to: `Tools → External Plugins → Refresh Plugins`
   - Plugins will appear in the `Tools` menu

---

## 🛠️ Modules & Tools

### 1. **hello_plugin.py** — Basic Plugin Template
A starter plugin demonstrating KiCad Action Plugin architecture.

**Features:**
- Simple action registration
- Menu integration
- Dialog callback system
- wxPython GUI integration

**Use Case:** Learning KiCad plugin development fundamentals

**Related Documentation:** [Plugin Architecture Guide](./10.0/scripting/plugins/pcb_health_analyzer/docs/architecture.md)

---

### 2. **pcb_reader.py** — PCB File Analyzer
Lightweight utility for parsing and analyzing `.kicad_pcb` files.

**Features:**
- PCB file parsing
- Layer information extraction
- Track and via analysis
- Component mapping

**Use Case:** Programmatic PCB metadata extraction for custom analysis pipelines

---

### 3. **advanced_pcb_checker/** — Automated PCB Inspection Plugin
Advanced plugin for detecting design rule violations and manufacturing issues.

**Key Features:**
- ✓ Thin track detection (< 0.2mm)
- ✓ Small via drill detection (< 0.3mm)
- ✓ Footprints outside board boundary detection
- ✓ Automatic report generation (TXT format)
- ✓ Design rule compliance validation

**Output:** `pcb_report.txt` with detailed inspection results

**Directory Structure:**
```
advanced_pcb_checker/
├── __init__.py
├── advanced_checker.py      # Core inspection logic
└── Readme.md               # Detailed documentation
```

---

### 4. **pcb_health_analyzer/** — Comprehensive Health Analysis Tool ⭐ (Recommended)
The most advanced and feature-rich module. Production-ready plugin for comprehensive PCB design quality assessment with **integrated AI Knowledge Assistant**.

**Key Features:**
- 📊 **Multi-Metric Analysis**
  - PCB statistics (tracks, vias, footprints, nets)
  - Layer distribution analysis
  - Component placement validation
  - Copper coverage metrics

- 🎯 **Design Quality Inspection (DRC Summary Module)**
  - Track Width Analysis (Min/Max/Avg, flags extremely thin tracks)
  - Via Statistics (Counts by type, identifies unusually small vias)
  - Board Complexity Score based on tracks, vias, nets, and layers
  - Copper Layer Utilization & Track Distribution
  - Unconnected pad detection
  - Track overlap analysis
  - Component density assessment

- 📈 **Health Scoring System**
  - Automated health score (0-100)
  - Board status classification:
    - EXCELLENT (90-100)
    - GOOD (80-89)
    - FAIR (70-79)
    - NEEDS REVIEW (60-69)
    - CRITICAL (<60)

- 🤖 **AI PCB Knowledge Assistant** *(NEW — Day 12)*
  - Natural-language issue explanations
  - Prioritised design recommendations
  - Interactive Q&A system (4 predefined questions)
  - Fabrication readiness assessment (READY / NEEDS IMPROVEMENT)
  - Structured knowledge file export for future LLM integration

- 📄 **Multi-Format Report Generation**
  - Formatted text reports
  - JSON data export (`pcb_health_report.json`)
  - HTML dashboard with AI Assistant section (`pcb_health_report.html`)
  - Board knowledge export (`reports/board_knowledge.json`)

**Output Files:**
| File | Description |
|------|-------------|
| `pcb_health_report.txt` | Human-readable summary with AI analysis |
| `pcb_health_report.html` | Visual HTML dashboard with AI section |
| `pcb_health_report.json` | Structured analysis data |
| `reports/board_knowledge.json` | Knowledge export for LLM integration |

**Directory Structure:**
```
pcb_health_analyzer/
├── __init__.py               # Plugin registration
├── health_analyzer.py        # Main plugin entry point
├── analyzer_core.py          # Core analysis algorithms
├── drc_summary.py            # Design Rule Checker
├── ai_review_engine.py       # AI rule-based reasoning engine (NEW)
├── pcb_chat_assistant.py     # Interactive Q&A assistant (NEW)
├── pcb_html_report.py        # HTML report with AI section (UPDATED)
├── report_generator.py       # JSON + knowledge file export (UPDATED)
├── gui.py                    # GUI components (future scope)
├── requirements.txt          # Dependencies
├── Readme.md                 # Module documentation
├── docs/
│   └── architecture.md       # Technical architecture
└── pcb_health_report.json    # Sample output
```

**Dependencies:**
```txt
wxPython >= 4.1.0
```

**Usage in KiCad:**
1. Install plugin (see Installation section)
2. Open PCB in KiCad Editor
3. Navigate to: `Tools → External Plugins → OPCB Health Analyzer`
4. Review generated reports in project directory

---

### 5. **pcb_report_generator/** — Component Report Generator
Utility for analyzing component datasets and generating design validation reports.

**Features:**
- Component counting and classification
- Duplicate component detection
- Missing value identification
- Formatted report generation

**Directory Structure:**
```
pcb_report_generator/
├── __init__.py
├── main.py              # CLI entry point
├── analyzer.py          # Component analysis logic
├── report_writer.py     # Report formatting
├── sample_data.txt      # Example input
├── report.txt           # Example output
└── Readme.md            # Documentation
```

---

### 6. **opcb_drc_checker/** — OPCB Design Rule Checker Plugin
A KiCad Action Plugin that automatically detects common PCB design issues and generates detailed HTML and TXT reports.

**Key Features:**
- Minimum Track Width Checker (< 0.2mm default)
- Via Size Analyzer (< 0.4mm default)
- Board Dimension Analyzer (width, height, area)
- Layer Usage Statistics (tracks/vias per copper layer)
- Automated Multi-Format Report Generator (HTML/TXT)

**Directory Structure:**
```
opcb_drc_checker/
├── __init__.py
├── opcb_drc_checker.py      # Main plugin logic
├── report_generator.py      # Text report generator
└── html_generator.py        # HTML report generator
```

---

## 🤖 AI PCB Knowledge Assistant (Day 12)

The AI PCB Knowledge Assistant is the flagship feature that transforms the OPCB Health Analyzer from a simple metrics tool into an intelligent design advisor.

### Workflow Comparison

**Before (Traditional):**
```
Analyze Board → Health Score = 72 → Done
```

**After (AI-Assisted):**
```
Analyze Board → AI Review → Explain Problems → Suggest Fixes → Answer Questions → Assess Fabrication
```

### Module Architecture

```
ai_review_engine.py          pcb_chat_assistant.py
     │                              │
     │  Rule-based reasoning        │  Natural-language generation
     │  Issue detection             │  Q&A system
     │  Recommendations             │  Full summary reports
     │  Fabrication check           │  Wraps AI Review Engine
     │                              │
     └──────────┬───────────────────┘
                │
    ┌───────────┴───────────┐
    │   health_analyzer.py  │  ← Main plugin (orchestrator)
    └───────────┬───────────┘
                │
    ┌───────────┴───────────────────────────────┐
    │                                           │
    ▼                                           ▼
pcb_html_report.py                  report_generator.py
    │                                           │
    │  HTML with AI section                     │  JSON + knowledge export
    │  Interactive Q&A                          │  board_knowledge.json
    │  Fabrication banner                       │
    │                                           │
    ▼                                           ▼
pcb_health_report.html              reports/board_knowledge.json
```

### Task Breakdown

#### Task 1: PCB Chat Assistant (`pcb_chat_assistant.py`)

The `PCBChatAssistant` class generates complete natural-language analysis summaries from raw board statistics.

**Input:**
```python
{
    "tracks": 120,
    "vias": 60,
    "health_score": 70,
    "unconnected_pads": 8,
    "drc_errors": 5
}
```

**Output:**
```
==================================================
         PCB ANALYSIS SUMMARY
==================================================

The board scores 70/100 — Moderate Quality. 3 issue(s) require attention.

ISSUES FOUND:
----------------------------------------
  • Unconnected Pads
    8 unconnected pad(s) detected. Unconnected pads may result in open
    circuits and board malfunction.

  • DRC Violations
    5 DRC violation(s) detected. DRC violations indicate that the design
    may fail manufacturing constraints.

  • High Via Density
    Via count (60) exceeds 40% of track count (120).

RECOMMENDATIONS:
----------------------------------------
  1. Run DRC and fix all violations before fabrication.
  2. Review the netlist and ensure every pad is connected.
  3. Reduce unnecessary layer transitions.
  4. Review power and ground routing.
  5. Perform a final visual inspection.

FABRICATION STATUS:
----------------------------------------
  Status  : NEEDS IMPROVEMENT
  Details : Fix 5 DRC violations and 8 unconnected pads.
==================================================
```

---

#### Task 2: AI Explanation Engine (`ai_review_engine.py`)

Rule-based reasoning engine with 6 detection rules:

| Rule | Condition | Explanation |
|------|-----------|-------------|
| Unconnected Pads | `unconnected_pads > 0` | May result in open circuits and board malfunction |
| DRC Violations | `drc_errors > 0` | Design may fail manufacturing constraints |
| High Via Density | `vias > tracks * 0.4` | Increases manufacturing complexity |
| Thin Tracks | `thin_tracks > 0` | Signal integrity and manufacturing risk |
| Small Vias | `small_vias > 0` | Drilling difficulty and unreliable plating |
| Low Track Count | `tracks < 20` | Possible incomplete routing |

---

#### Task 3: Interactive Question System

Four predefined questions with intelligent answers:

| Question | What It Answers |
|----------|-----------------|
| "Why is my health score low?" | Lists specific factors reducing the score |
| "What are the major issues?" | Detailed explanations of all detected issues |
| "How can I improve the board?" | Prioritised actionable recommendations |
| "Is this board ready for fabrication?" | READY / NEEDS IMPROVEMENT with reasons |

---

#### Task 4: Fabrication Readiness Check

```python
if drc_errors == 0 and unconnected_pads == 0:
    # → READY
else:
    # → NEEDS IMPROVEMENT (with specific reasons)
```

---

#### Task 5: AI Section in HTML Report

The HTML report now includes a dedicated **AI PCB Assistant** card featuring:
- Overall quality assessment badge
- Issue cards with explanations
- Numbered recommendation list
- Fabrication readiness banner (colour-coded)
- Collapsible interactive Q&A section

---

#### Task 6: JSON Knowledge File Export (Bonus)

Generates `reports/board_knowledge.json` for future LLM integration:

```json
{
  "board_name": "test.kicad_pcb",
  "health_score": 72,
  "grade": "C",
  "board_status": "FAIR",
  "quality_level": "Moderate Quality",
  "fabrication_status": "NEEDS IMPROVEMENT",
  "issues": ["drc_violations", "unconnected_pads"],
  "recommendations": ["run_drc", "fix_unconnected_nets", "reduce_vias"],
  "statistics": { ... },
  "ai_review": {
    "summary": "...",
    "issues_detail": [ ... ],
    "recommendations_detail": [ ... ],
    "fabrication_details": "..."
  }
}
```

This creates a foundation for future integration with:
- Local LLMs via [Ollama](https://ollama.com)
- Cloud APIs from [OpenAI](https://platform.openai.com)
- Custom conversational PCB analysis pipelines

---

## 📦 Installation

### System Requirements

- **Python:** 3.7+
- **KiCad:** 6.0+ (for plugin functionality)
- **OS:** Linux, macOS, Windows
- **Dependencies:** See individual module `requirements.txt`

### Setup Options

#### Option 1: Direct Module Usage (Recommended for Development)

```bash
# Clone repository
git clone https://github.com/akshat2805p/FOSSEE-eSim-Tasks.git
cd FOSSEE-eSim-Tasks

# Install dependencies (if any)
pip install -r 10.0/scripting/plugins/pcb_health_analyzer/requirements.txt

# Import modules in your Python code
import sys
sys.path.insert(0, './10.0/scripting/plugins/')
from pcb_health_analyzer import health_analyzer
```

#### Option 2: KiCad Integration

```bash
# Copy plugins to KiCad scripting directory
# Location varies by OS (see Quick Start section)

# Restart KiCad and refresh plugins
```

#### Option 3: Development Setup

```bash
# Clone and create development environment
git clone https://github.com/akshat2805p/FOSSEE-eSim-Tasks.git
cd FOSSEE-eSim-Tasks

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install all dependencies
pip install -r 10.0/scripting/plugins/pcb_health_analyzer/requirements.txt
```

---

## 📚 Usage Examples

### Example 1: Run Full AI-Assisted Analysis (via KiCad Plugin)

1. Open your PCB design in KiCad PCB Editor
2. Go to `Tools → External Plugins → OPCB Health Analyzer`
3. The plugin will generate:
   - `pcb_health_report.txt` — Text report with AI summary
   - `pcb_health_report.html` — Visual dashboard with AI Assistant card
   - `reports/board_knowledge.json` — Structured knowledge export

### Example 2: Use the AI Chat Assistant Programmatically

```python
from pcb_health_analyzer.pcb_chat_assistant import PCBChatAssistant

# Board statistics (from analysis or manually constructed)
board_stats = {
    "tracks": 120,
    "vias": 60,
    "health_score": 70,
    "unconnected_pads": 8,
    "drc_errors": 5,
}

assistant = PCBChatAssistant()

# Generate full analysis summary
print(assistant.generate_response(board_stats))

# Ask specific questions
questions = [
    "Why is my health score low?",
    "What are the major issues?",
    "How can I improve the board?",
    "Is this board ready for fabrication?",
]

for q in questions:
    print(assistant.answer_question(q, board_stats))
    print()
```

### Example 3: Use the AI Review Engine Directly

```python
from pcb_health_analyzer.ai_review_engine import AIReviewEngine

engine = AIReviewEngine()
review = engine.analyze({
    "tracks": 120,
    "vias": 60,
    "health_score": 70,
    "unconnected_pads": 8,
    "drc_errors": 5,
})

print(f"Quality: {review['quality_level']}")
print(f"Fabrication: {review['fabrication_status']}")
print(f"Issues: {len(review['issues'])}")
for issue in review["issues"]:
    print(f"  - {issue['title']}: {issue['explanation']}")
```

### Example 4: Generate Knowledge File

```python
from pcb_health_analyzer.report_generator import generate_knowledge_file
from pcb_health_analyzer.ai_review_engine import AIReviewEngine

stats = {"tracks": 120, "vias": 60, "health_score": 70, "unconnected_pads": 8, "drc_errors": 5}
engine = AIReviewEngine()
review = engine.analyze(stats)

generate_knowledge_file(
    board_name="my_board.kicad_pcb",
    stats=stats,
    ai_review=review,
    output_dir="./output",
)
# → creates ./output/reports/board_knowledge.json
```

---

## 🏗️ Architecture

### Plugin Execution Flow (with AI Assistant)

```
KiCad PCB Editor
    ↓
Tools → External Plugins
    ↓
Plugin Manager (pcbnew)
    ↓
┌──────────────────────────────────────────┐
│   OPCBHealthAnalyzer (ActionPlugin)      │
│  ├─ defaults()         [metadata]        │
│  ├─ Run()              [main logic]      │
│  │   ├─ Collect board statistics         │
│  │   ├─ Compute health score             │
│  │   ├─ AI Review Engine                 │
│  │   │   ├─ Detect issues                │
│  │   │   ├─ Generate explanations        │
│  │   │   ├─ Build recommendations        │
│  │   │   └─ Assess fabrication           │
│  │   ├─ PCB Chat Assistant               │
│  │   │   ├─ Generate full summary        │
│  │   │   └─ Answer questions             │
│  │   └─ Generate all reports             │
│  └─ Show Completion Dialog               │
└──────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────┐
│   Output Files                           │
│  ├─ pcb_health_report.txt                │
│  ├─ pcb_health_report.html (+ AI card)   │
│  ├─ pcb_health_report.json               │
│  └─ reports/board_knowledge.json         │
└──────────────────────────────────────────┘
```

### Module Dependencies

```
pcbnew (KiCad Python API)
    ↓
health_analyzer.py ← Main orchestrator
    ├── analyzer_core.py      ← Core statistics
    ├── drc_summary.py        ← DRC checks
    ├── ai_review_engine.py   ← AI rule-based reasoning
    ├── pcb_chat_assistant.py ← Q&A + summary generation
    ├── pcb_html_report.py    ← HTML dashboard + AI section
    ├── report_generator.py   ← JSON + knowledge export
    └── gui.py                ← UI components (future)
```

### Data Flow

```
.kicad_pcb File
    ↓
[Board Statistics Collector]
    ↓
Raw Statistics (dict)
    ↓
┌─────────────┐     ┌───────────────────┐
│ AI Review   │────▸│ PCB Chat          │
│ Engine      │     │ Assistant         │
│             │     │                   │
│ • Issues    │     │ • Full summary    │
│ • Recs      │     │ • Q&A answers     │
│ • Fab check │     │                   │
└──────┬──────┘     └────────┬──────────┘
       │                     │
       ▼                     ▼
┌─────────────────────────────────────────┐
│          Report Generation              │
│  ├─ Text Report (with AI summary)       │
│  ├─ HTML Dashboard (with AI card)       │
│  ├─ JSON Data Export                    │
│  └─ Knowledge File (for LLM)           │
└─────────────────────────────────────────┘
```

---

## 🛠️ Technologies

- **Language:** Python 3.7+
- **KiCad:** 6.0+ / 10.0
- **APIs:** pcbnew (KiCad Python API), wxPython
- **Data Formats:** JSON, CSV, TXT, HTML
- **AI Approach:** Rule-based reasoning engine (extensible to LLMs)
- **Version Control:** Git

---

## 📖 Detailed Module Documentation

Each module includes comprehensive documentation:

- [PCB Health Analyzer Documentation](./10.0/scripting/plugins/pcb_health_analyzer/Readme.md)
- [Advanced PCB Checker Documentation](./10.0/scripting/plugins/advanced_pcb_checker/Readme.md)
- [PCB Report Generator Documentation](./10.0/scripting/plugins/pcb_report_generator/Readme.md)
- [Architecture Reference](./10.0/scripting/plugins/pcb_health_analyzer/docs/architecture.md)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** on GitHub
2. **Create a feature branch:** `git checkout -b feature/your-feature`
3. **Make your changes** with clear commit messages
4. **Test thoroughly** on KiCad 6.0+ versions
5. **Submit a Pull Request** with a detailed description

### Development Workflow

```bash
# Clone your fork
git clone https://github.com/your-username/FOSSEE-eSim-Tasks.git
cd FOSSEE-eSim-Tasks

# Create feature branch
git checkout -b feature/add-new-analysis

# Make changes and test
# ... edit files ...

# Commit with clear messages
git add .
git commit -m "feat: add new PCB analysis feature"

# Push and create PR
git push origin feature/add-new-analysis
```

---

## 📞 Support & Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/akshat2805p/FOSSEE-eSim-Tasks/issues)
- **Discussions:** [Ask questions and share ideas](https://github.com/akshat2805p/FOSSEE-eSim-Tasks/discussions)

---


### Planned Features 📋
- [ ] Integration with local LLMs (Ollama)
- [ ] OpenAI API integration for conversational analysis
- [ ] Real-time PCB monitoring
- [ ] Advanced DRC with custom rules
- [ ] Web-based interactive dashboard
- [ ] Machine learning-based quality prediction
- [ ] Multi-language support
- [ ] CI/CD pipeline integration

---
**Last Updated:** June 2026
