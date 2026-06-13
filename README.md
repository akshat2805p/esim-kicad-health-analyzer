# eSim KiCad Health Analyzer — AI PCB Knowledge Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![KiCad: 6.0+](https://img.shields.io/badge/KiCad-6.0%2B%20%7C%2010.0-red.svg)](https://www.kicad.org/)
[![AI Assisted](https://img.shields.io/badge/AI--Assisted%20Analysis-blueviolet)](.)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A comprehensive suite of Python-based KiCad automation plugins and utilities developed for the **FOSSEE eSim** project. This repository contains production-ready tools for PCB analysis, design validation, visual DRC inspection, dependency graph generation, report generation, and an **AI-powered Knowledge Assistant** that explains issues, recommends fixes, answers questions, and assesses fabrication readiness — all seamlessly integrated with KiCad's Python API ecosystem.

**Repository Owner:** [akshat2805p](https://github.com/akshat2805p)  
**For:** FOSSEE eSim Open Source Contributions

---

## 📋 Table of Contents

- [Overview](#-overview)
- [What Makes This Different](#-what-makes-this-different)
- [Quick Start](#-quick-start)
- [Modules & Tools](#-modules--tools)
- [AI PCB Knowledge Assistant](#-ai-pcb-knowledge-assistant)
- [Dependency Visualizer](#-dependency-visualizer-new)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This repository provides a complete ecosystem of KiCad plugins and Python utilities for automating PCB design workflows. The tools empower engineers to:

✅ **Analyze PCB health** and design quality automatically  
✅ **Generate comprehensive inspection reports** (TXT, HTML, JSON)  
✅ **Detect design rule violations** visually directly on the board  
✅ **Create interactive dependency graphs** of components and nets  
✅ **Get AI-assisted explanations** of complex PCB issues  
✅ **Receive intelligent design recommendations**  
✅ **Assess fabrication readiness** before sending to manufacturing  
✅ **Export structured board knowledge** for future LLM integration  

All modules are designed to integrate seamlessly with KiCad and leverage the `pcbnew` Python API for native board manipulation.

---

## 🚀 What Makes This Different

Most standard internship projects stop at:

```
Analyze → Generate Report
```

This project implements a full **AI-Assisted and Visual pipeline**:

```
Analyze → Visually Highlight Issues → Explain (AI) → Recommend Fixes → Graph Dependencies → Assess Fabrication Readiness
```

The **AI PCB Knowledge Assistant** transforms raw board statistics into actionable intelligence, making this suite feel much closer to a professional enterprise AI EDA tool than a traditional PCB analyzer.

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/akshat2805p/FOSSEE-eSim-Tasks.git
cd FOSSEE-eSim-Tasks
```

### 2. Install Plugins to KiCad
```bash
# Linux/macOS
cp -r 10.0/scripting/plugins/* ~/.local/share/kicad/6.0/scripting/plugins/
cp -r dependency_visualizer/ ~/.local/share/kicad/6.0/scripting/plugins/

# Windows
xcopy 10.0\scripting\plugins\* %APPDATA%\kicad\6.0\scripting\plugins\ /E /H /C /I
xcopy dependency_visualizer %APPDATA%\kicad\6.0\scripting\plugins\dependency_visualizer\ /E /H /C /I
```

### 3. Refresh Plugins in KiCad
- Open KiCad PCB Editor
- Navigate to: `Tools → External Plugins → Refresh Plugins`
- The new tools will appear in the `Tools` menu.

---

## 🛠️ Modules & Tools

### 1. **visual_drc_inspector.py** — Visual DRC Inspector ⭐ *(Mentor-Attention Feature)*
A KiCad Action Plugin that visually highlights potential PCB issues directly on the board instead of only generating reports. Acts as an **AI-like PCB Assistant** to guide routing decisions interactively.
- **Visual Annotations:** Draws temporary circles, warning markers, and labels near problem areas on the layout.
- **Advanced Detection:** Finds thin tracks (<0.2mm), isolated/floating vias, unconnected track segments, very short tracks, and copper objects outside the board outline.
- **Severity Levels:** Classifies issues into `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
- **Multi-Format Reports:** `visual_inspection_report.txt` and `visual_inspection_report.html`.

### 2. **dependency_visualizer/** — Interactive Dependency Graph ⭐ *(NEW)*
Generates a highly interactive HTML dependency graph of components and nets on your PCB.
- **Graph Construction:** Maps out components as nodes and nets as edges.
- **Interactive UI:** View the graph in the browser with zoom and pan support.
- **Detailed Analytics:** Identifies the most connected components, total nets, and components.
- **Output:** `dependency_graph.html` and `dependency_report.json`.

### 3. **pcb_health_analyzer/** — Comprehensive Health Analysis Tool
Production-ready plugin for comprehensive PCB design quality assessment with an **integrated AI Knowledge Assistant**.
- **Multi-Metric Analysis:** PCB statistics, layer distribution, component placement validation, and copper coverage.
- **Health Scoring System:** Automated health score (0-100) and board status classification (`EXCELLENT` to `CRITICAL`).
- **AI PCB Knowledge Assistant:** Natural-language explanations, prioritized design recommendations, interactive Q&A.
- **Board Knowledge Export:** JSON export for future integration with Local LLMs (Ollama) or Cloud APIs.

### 4. **advanced_pcb_checker/** & **opcb_drc_checker/** — Automated PCB Inspection
Plugins for detecting design rule violations, small via drills (<0.3mm), thin tracks, and generating automated HTML/TXT inspection reports.

### 5. **pcb_report_generator/** & **pcb_reader.py** — Component & Metadata Analysis
Utilities for analyzing component datasets, counting/classifying components, finding duplicate footprints, and extracting `.kicad_pcb` metadata programmatically.

### 6. **test_ai_assistant.py** — Standalone AI Test Script *(NEW)*
Run the AI Review Engine directly from the command line without needing to launch KiCad.
```bash
python test_ai_assistant.py
```
Performs 6 comprehensive tests on the AI logic, chat assistant, HTML generation, and knowledge file export.

---

## 🤖 AI PCB Knowledge Assistant

The AI PCB Knowledge Assistant is the flagship feature that transforms the Health Analyzer from a simple metrics tool into an intelligent design advisor.

### Module Architecture

```text
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
```

### Knowledge File Export
Generates `reports/board_knowledge.json` containing structured analysis data, ready to be ingested by advanced LLM workflows.
```json
{
  "board_name": "test.kicad_pcb",
  "health_score": 72,
  "fabrication_status": "NEEDS IMPROVEMENT",
  "issues": ["drc_violations", "unconnected_pads"],
  "ai_review": { ... }
}
```

---

## 📦 Installation & Setup

### System Requirements
- **Python:** 3.7+
- **KiCad:** 6.0+ or 10.0
- **Dependencies:** `wxPython >= 4.1.0` (for GUI components)

### Development Setup
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

pip install -r 10.0/scripting/plugins/pcb_health_analyzer/requirements.txt
```

---

## 📚 Usage Examples

### Example 1: Run Full AI-Assisted Analysis (via KiCad)
1. Open your PCB in KiCad PCB Editor.
2. Go to `Tools → External Plugins → OPCB Health Analyzer`.
3. Check your project directory for `pcb_health_report.html` and `board_knowledge.json`.

### Example 2: Use the AI Chat Assistant Programmatically
```python
from pcb_health_analyzer.pcb_chat_assistant import PCBChatAssistant

board_stats = {
    "tracks": 120, "vias": 60, "health_score": 70,
    "unconnected_pads": 8, "drc_errors": 5
}
assistant = PCBChatAssistant()

print(assistant.generate_response(board_stats))
print(assistant.answer_question("Is this board ready for fabrication?", board_stats))
```

### Example 3: Generate Dependency Graph
1. In KiCad, run `Tools → External Plugins → Dependency Visualizer`.
2. A popup will show the number of components and nets analyzed.
3. Your default web browser will automatically open `reports/dependency_graph.html`.

---

## 🤝 Contributing

Contributions are welcome!

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature`
3. **Commit your changes:** `git commit -m "feat: add new feature"`
4. **Push to the branch:** `git push origin feature/your-feature`
5. **Submit a Pull Request**

### Planned Features 📋
- [ ] Integration with local LLMs (Ollama)
- [ ] OpenAI API integration for conversational analysis
- [x] Visual DRC Highlighting directly on PCB
- [x] Interactive Dependency Graphs
- [ ] Web-based interactive dashboard
- [ ] Machine learning-based quality prediction

---

## 📞 Support & Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/akshat2805p/FOSSEE-eSim-Tasks/issues)
- **Author:** Akshat ([akshat2805p](https://github.com/akshat2805p))

---
*Last Updated: June 2026*
