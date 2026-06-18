# eSim KiCad Health Analyzer & AI PCB Knowledge Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![KiCad: 6.0+ / 10.0](https://img.shields.io/badge/KiCad-6.0%2B%20%7C%2010.0-red.svg)](https://www.kicad.org/)
[![AI Assisted](https://img.shields.io/badge/AI--Assisted%20Analysis-blueviolet)](.)

A comprehensive suite of advanced Python-based KiCad automation plugins developed for **FOSSEE eSim**. This repository transforms standard KiCad into an intelligent, AI-assisted EDA environment. It features tools for comprehensive PCB health analysis, visual Design Rule Checking (DRC), component dependency graphing, and a state-of-the-art **AI-powered Knowledge Assistant** that intelligently explains layout issues and recommends optimal fixes.

**Repository Owner:** [akshat2805p](https://github.com/akshat2805p)  
**For:** FOSSEE eSim Open Source Contributions

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Plugin Modules & Tools](#-plugin-modules--tools)
- [AI PCB Knowledge Assistant](#-ai-pcb-knowledge-assistant)
- [Installation & Setup](#-installation--setup)
- [Usage Examples](#-usage-examples)
- [Project Architecture](#-project-architecture)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

Modern PCB design requires more than just checking connections. This ecosystem of plugins is built to empower engineers to rapidly identify, analyze, and correct layout issues using an integrated AI Copilot. By automating health scoring, visual inspections, and reporting, this toolkit acts as an expert pair of eyes reviewing your board before fabrication.

### Key Features
✅ **Automated PCB Health Grading:** Dynamic A-F health scores based on layout complexity, DRC errors, congestion, and cost estimation.  
✅ **AI PCB Copilot:** Natural language explanations of layout issues with actionable recommendations.  
✅ **Visual DRC Highlighting:** Issues are highlighted interactively with custom shapes directly on the PCB layout.  
✅ **Interactive Dependency Graphs:** Generates rich HTML-based graphs mapping connections between nets and components.  
✅ **Extensive Reporting:** Automated exports of analysis data to HTML, TXT, and structured JSON files for LLM integration.  

---

## 🛠️ Plugin Modules & Tools

This repository contains multiple specialized KiCad action plugins:

### 1. `pcb_health_analyzer` — The AI Design Copilot
The flagship plugin offering an interactive wxPython Copilot GUI. 
- Analyzes tracks, vias, layers, unrouted pads, and component overlaps.
- Computes complexity and congestion scores, and estimates fabrication costs.
- Fully integrated with an **AI Review Engine** to generate natural language insights.
- **Outputs:** `pcb_health_report.html`, `pcb_health_report.txt`, and structured `board_knowledge.json`.

### 2. `visual_drc_inspector.py` — Visual DRC Highlighting
Instead of just listing errors, this plugin dynamically draws visual warning markers (circles and labels) directly onto the PCB canvas.
- Detects thin tracks (<0.2mm), short trace fragments, floating vias, and copper outside the board outline.
- Classifies issues into `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL` severity levels.
- Generates embedded AI recommendations in a `visual_inspection_report.html` report.

### 3. `dependency_visualizer` — Component & Net Graphing
Generates an interactive dependency graph mapping how components are interconnected across the board.
- Uses `NetworkX` to construct nodes (components) and edges (nets).
- Identifies the most highly connected components (useful for decoupling capacitor placement and power routing).
- **Outputs:** Interactive HTML graph and JSON analytics.

### 4. `advanced_pcb_checker` & `opcb_drc_checker`
Lightweight, rapid inspection tools for baseline design validation.
- Checks minimum track widths, via drill sizes, and verifies footprint placements are within board boundaries.
- Generates quick `.txt` and `.html` summary logs.

### 5. `pcb_report_generator` & `pcb_reader.py`
Utilities to read `.kicad_pcb` metadata programmatically and generate detailed component, footprint, and layer composition summaries.

### 6. `smart_design_assistant` — Smart PCB Design Rule Assistant (AI-Based)
An advanced plugin that automatically analyzes the PCB and provides intelligent design suggestions before running DRC.
- Scans for thin tracks, components placed too close together, unconnected nets, excessive vias on signal paths, and silkscreen overlapping pads.
- Computes a dynamic **PCB Warning Score** (Excellent, Good, Needs Improvement, Critical).
- Provides an interactive GUI panel showing total warnings, health score, and top 5 recommendations.
- Generates an **Intelligent PCB Design Recommendation Report** in HTML.

---

## 🤖 AI PCB Knowledge Assistant

Unlike standard DRC tools, the **AI PCB Knowledge Assistant** translates raw numeric statistics into contextual advice. 

**How it works:**
1. The **Health Analyzer** extracts board constraints, component density, and error counts.
2. The **AI Review Engine** parses this data through specialized hardware-design rule engines.
3. The **PCB Chat Assistant** module wraps the findings in natural language, offering conversational feedback, prioritizing critical fixes (e.g., *“Increase track width near power net to reduce impedance”*), and determining fabrication readiness.

You can test the AI logic natively from the command line without opening KiCad via the included test script:
```bash
python test_ai_assistant.py
```

---

## 📦 Installation & Setup

### Requirements
- **Python 3.7+**
- **KiCad 6.0+** (Fully compatible with KiCad 10.0 nightly)
- **wxPython >= 4.1.0** (Bundled with KiCad's Python environment)

### 1. Clone the repository
```bash
git clone https://github.com/akshat2805p/FOSSEE-eSim-Tasks.git
cd FOSSEE-eSim-Tasks
```

### 2. Install Plugins to KiCad Directory
Copy the plugin folders into KiCad's scripting directory:

**Linux / macOS:**
```bash
cp -r 10.0/scripting/plugins/* ~/.local/share/kicad/6.0/scripting/plugins/
cp -r dependency_visualizer/ ~/.local/share/kicad/6.0/scripting/plugins/
```

**Windows:**
```cmd
xcopy 10.0\scripting\plugins\* %APPDATA%\kicad\6.0\scripting\plugins\ /E /H /C /I
xcopy dependency_visualizer %APPDATA%\kicad\6.0\scripting\plugins\dependency_visualizer\ /E /H /C /I
```

### 3. Refresh Plugins
1. Open the KiCad PCB Editor.
2. Navigate to **Tools → External Plugins → Refresh Plugins**.
3. You will now see the suite of plugins (e.g., *PCB Design Copilot*, *OPCB Visual DRC Inspector*, *Dependency Visualizer*) available in the menu and toolbar.

---

## 📚 Usage Examples

### Running the AI Health Analyzer
1. Open your layout in the PCB Editor.
2. Click **Tools → External Plugins → PCB Design Copilot**.
3. Review the popup metrics, and check your project folder for the comprehensive HTML AI report and `board_knowledge.json`.

### Running Visual DRC
1. Click **Tools → External Plugins → OPCB Visual DRC Inspector**.
2. Notice the `⚠` markers and circular highlights drawn dynamically onto the board layout indicating critical and moderate layout issues.
3. Check the generated `visual_inspection_report.txt` for exact coordinates and suggested fixes.

---

## 🏗️ Project Architecture

```text
FOSSEE-eSim-Tasks/
├── 10.0/scripting/plugins/
│   ├── pcb_health_analyzer/      # AI Copilot & Core grading logic
│   ├── advanced_pcb_checker/     # Strict boundary & drill checks
│   ├── opcb_drc_checker/         # Track/via threshold analysis
│   ├── visual_drc_inspector.py   # Visual canvas drawing logic
│   └── pcb_report_generator/     # Text/HTML report generators
├── dependency_visualizer/        # NetworkX graph exporter
├── test_ai_assistant.py          # Standalone headless AI test suite
└── README.md                     # Documentation
```

---

## 🤝 Contributing

Contributions from the FOSSEE community and open-source hardware enthusiasts are highly encouraged!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Upcoming Roadmap
- [ ] Direct OpenAI / Local Ollama API integration for conversational Q&A routing advice.
- [ ] Real-time impedance calculations based on stack-up properties.
- [x] Web-based HTML dependency graphing.
- [x] Automated board cost estimations.

---

