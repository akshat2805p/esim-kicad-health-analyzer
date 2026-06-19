<div align="center">
  <h1>eSim KiCad Health Analyzer & AI PCB Knowledge Assistant</h1>
  <p><strong>Transforming KiCad into an intelligent, AI-assisted EDA environment.</strong></p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
  [![KiCad: 6.0 - 10.0](https://img.shields.io/badge/KiCad-6.0%20%E2%86%92%2010.0-red.svg)](https://www.kicad.org/)
  [![AI Assisted](https://img.shields.io/badge/AI--Assisted%20Analysis-blueviolet)](.)
</div>

---

A comprehensive suite of advanced Python-based KiCad automation plugins developed for **FOSSEE eSim**. This repository empowers hardware engineers to rapidly identify, analyze, and correct PCB layout issues using a fully integrated AI Copilot. 

From visual Design Rule Checking (DRC) to component dependency graphing, this toolkit acts as an expert pair of eyes reviewing your board before fabrication.

**Repository Owner:** [akshat2805p](https://github.com/akshat2805p)  
**Developed For:** FOSSEE eSim Open Source Contributions

---

## 📋 Table of Contents
- [🚀 Overview](#overview)
- [✨ Key Features](#key-features)
- [🧩 Plugin Suite](#plugin-suite)
- [🤖 AI PCB Knowledge Assistant](#ai-pcb-knowledge-assistant)
- [⚙️ Installation & Setup](#installation--setup)
- [💡 Usage Guide](#usage-guide)
- [📂 Project Architecture](#project-architecture)
- [🤝 Contributing](#contributing)
- [📄 License](#license)

---

## 🚀 Overview

Modern PCB design requires more than just checking logical connections. Our ecosystem of plugins automates health scoring, visual inspections, and reporting. We bridge the gap between traditional DRC and intelligent contextual feedback, highlighting issues like congestion, thin tracks, and floating vias *before* you send your board to manufacturing.

---

## ✨ Key Features

- ✅ **Automated PCB Health Grading:** Dynamic A-F health scores based on layout complexity, DRC errors, congestion, and estimated fabrication cost.  
- ✅ **AI PCB Copilot:** Actionable, natural-language explanations of layout issues with precise recommendations.  
- ✅ **Visual DRC Highlighting:** Issues are drawn interactively onto your PCB canvas using custom shapes and warning markers.  
- ✅ **Interactive Dependency Graphs:** High-level HTML-based bipartite graphs mapping the relationships between nets and components.  
- ✅ **Cross-Version Compatibility:** Fully backwards and forwards compatible across KiCad 6.0, 7.0, 8.0, and 10.0 (nightly) architectures.  
- ✅ **Extensive Reporting:** Automated exports to HTML, TXT, and structured JSON for LLM integration.  

---

## 🧩 Plugin Suite

This repository contains multiple specialized KiCad Action Plugins, each serving a unique stage of the PCB review pipeline:

### 1. `pcb_health_analyzer` — The AI Design Copilot
The flagship plugin offering an interactive wxPython GUI Copilot. 
- Scans tracks, vias, unrouted pads, and component overlaps.
- Computes complexity and congestion scores.
- **Outputs:** `pcb_health_report.html`, `pcb_health_report.txt`, and structured `board_knowledge.json`.

### 2. `smart_design_assistant` — Intelligent Rules Assistant
Automatically analyzes the PCB and provides intelligent design suggestions.
- Dynamically checks `GetUnconnectedEdges()` and `GetUnconnectedCount()` using modern KiCad API fallbacks.
- Calculates dynamic **PCB Warning Scores** (Excellent, Good, Needs Improvement, Critical).
- Warns against traces (<0.2mm), clearance violations, and excessive via nets.

### 3. `visual_drc_inspector.py` — Canvas-Level Visual DRC
Instead of scrolling through a list of text errors, see them right on the board!
- Detects short trace fragments, floating vias, and objects outside the board outline.
- Classifies issues into severity levels (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
- Draws `⚠` labels and graphical rings around problem areas.

### 4. `dependency_visualizer` — Node-Edge Net Graphing
Exports an interactive dependency graph of your schematic mapping on the layout.
- Uses `NetworkX` to construct component nodes and net edges.
- Perfect for identifying highly connected hub components (like dense microcontrollers or bulk decoupling caps).

### 5. `advanced_pcb_checker` & `opcb_drc_checker`
Lightweight, rapid inspection tools for baseline validation of track widths, via drill constraints, and footprint boundaries.

---

## 🤖 AI PCB Knowledge Assistant

Unlike standard DRC tools, our **AI PCB Knowledge Assistant** translates raw numeric statistics into contextual hardware advice. 

**Workflow Pipeline:**
1. The **Health Analyzer** extracts board constraints, component density, and error counts.
2. The **AI Review Engine** parses this data through specialized hardware-design heuristics.
3. The **PCB Chat Assistant** wraps the findings in natural language, prioritizing critical fixes (e.g., *“Increase track width near power net to reduce impedance”*).

You can test the AI logic natively from the command line without opening KiCad via the included standalone test script:
```bash
python test_ai_assistant.py
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.7+**
- **KiCad 6.0 / 8.0 / 10.0** (Cross-compatible API wrappers implemented)
- **wxPython >= 4.1.0** (Included with KiCad's Python environment)

### 1. Clone the Repository
```bash
git clone https://github.com/akshat2805p/FOSSEE-eSim-Tasks.git
cd FOSSEE-eSim-Tasks
```

### 2. Install Plugins
Copy the plugin folders into KiCad's scripting directory based on your KiCad version (e.g., `8.0`, `9.0`, or `10.0`):

**Windows:**
```cmd
xcopy 10.0\scripting\plugins\* %USERPROFILE%\Documents\KiCad\8.0\scripting\plugins\ /E /H /C /I
xcopy dependency_visualizer %USERPROFILE%\Documents\KiCad\8.0\scripting\plugins\dependency_visualizer\ /E /H /C /I
```
*(Note: Change `8.0` to your specific KiCad version folder).*

**Linux / macOS:**
```bash
cp -r 10.0/scripting/plugins/* ~/.local/share/kicad/8.0/scripting/plugins/
cp -r dependency_visualizer/ ~/.local/share/kicad/8.0/scripting/plugins/
```

### 3. Refresh Plugins
1. Open the KiCad PCB Editor.
2. Navigate to **Tools → External Plugins → Refresh Plugins**.
3. The plugins will now be available in the plugin toolbar and menu!

---

## 💡 Usage Guide

### Running the Copilot
1. Open your `.kicad_pcb` file.
2. Click **Tools → External Plugins → Smart PCB Design Assistant**.
3. Review the popup metrics and recommendations. Check your project folder for the comprehensive HTML report.

### Running Visual DRC
1. Click **Tools → External Plugins → OPCB Visual DRC Inspector**.
2. Notice the `⚠` markers and circular highlights drawn dynamically onto the board layout.
3. Open the generated `visual_inspection_report.txt` for exact spatial coordinates of the violations.

---

## 📂 Project Architecture

```text
FOSSEE-eSim-Tasks/
├── 10.0/scripting/plugins/
│   ├── pcb_health_analyzer/      # AI Copilot & Core grading logic
│   ├── smart_design_assistant/   # Automated rule analysis GUI
│   ├── advanced_pcb_checker/     # Boundary & drill checks
│   ├── opcb_drc_checker/         # Track/via threshold analysis
│   ├── visual_drc_inspector.py   # Visual canvas drawing logic
│   └── pcb_report_generator/     # HTML/Text layout reporters
├── dependency_visualizer/        # NetworkX graph exporter
├── test_ai_assistant.py          # Standalone headless AI test suite
└── README.md                     # Project Documentation
```

---

## 🤝 Contributing

Contributions from the FOSSEE community and open-source hardware enthusiasts are highly encouraged!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome-feature`
3. Commit your changes: `git commit -m 'feat: Add awesome feature'`
4. Push to the branch: `git push origin feature/awesome-feature`
5. Open a Pull Request

### Upcoming Roadmap
- [ ] Local Ollama API integration for conversational Q&A routing advice.
- [ ] Real-time impedance calculations based on stack-up properties.
- [x] Web-based HTML dependency graphing.
- [x] Automated board cost estimations.
- [x] Full KiCad 8.0+ API compliance (`ToMM` and `GetUnconnectedCount` fallbacks).

---

