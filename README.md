# eSim KiCad Health Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![KiCad: 6.0+](https://img.shields.io/badge/KiCad-6.0+-red.svg)](https://www.kicad.org/)

A comprehensive suite of Python-based KiCad automation plugins and utilities developed for the **FOSSEE eSim** project. This repository contains production-ready tools for PCB analysis, design validation, and report generation integrated with KiCad 10.0's Python API ecosystem.

**Repository Owner:** [akshat2805p](https://github.com/akshat2805p)  
**For:** FOSSEE eSim Open Source Contributions

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Modules & Tools](#modules--tools)
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
✅ Generate comprehensive inspection reports  
✅ Detect design rule violations  
✅ Automate component verification  
✅ Create formatted design documentation  

All modules are designed to integrate seamlessly with KiCad 6.0+ and leverage the `pcbnew` Python API for native board manipulation.

---

## ⚡ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/akshat2805p/esim-kicad-health-analyzer.git
cd esim-kicad-health-analyzer

# Navigate to KiCad plugins directory
cd 10.0/scripting/plugins/

# Run any module directly or import for KiCad integration
```

### Using as KiCad Plugins

1. **Copy plugins to KiCad directory:**
   ```bash
   # Linux/macOS
   cp -r advanced_pcb_checker/ ~/.local/share/kicad/6.0/scripting/plugins/
   cp -r pcb_health_analyzer/ ~/.local/share/kicad/6.0/scripting/plugins/
   
   # Windows
   xcopy advanced_pcb_checker\ %APPDATA%\kicad\6.0\scripting\plugins\
   xcopy pcb_health_analyzer\ %APPDATA%\kicad\6.0\scripting\plugins\
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

**Quick Start:**
```python
from advanced_pcb_checker import advanced_checker
report = advanced_checker.analyze_board(pcb_board)
```

---

### 4. **pcb_health_analyzer/** — Comprehensive Health Analysis Tool ⭐ (Recommended)
The most advanced and feature-rich module. Production-ready plugin for comprehensive PCB design quality assessment.

**Key Features:**
- 📊 **Multi-Metric Analysis**
  - PCB statistics (tracks, vias, footprints, nets)
  - Layer distribution analysis
  - Component placement validation
  - Copper coverage metrics

- 🎯 **Design Quality Inspection**
  - Unconnected pad detection
  - Track overlap analysis
  - Component density assessment
  - Design rule compliance checks

- 📈 **Health Scoring System**
  - Automated health score (0-100)
  - Board status classification:
    - EXCELLENT (90-100)
    - GOOD (70-90)
    - NEEDS REVIEW (50-70)
    - CRITICAL (<50)

- 📄 **Multi-Format Report Generation**
  - Formatted text reports
  - JSON data export (`pcb_health_report.json`)
  - HTML visualization (`pcb_html_report.py`)
  - Automatic file generation

**Output Examples:**
- `pcb_health_report.json` — Structured analysis data
- `pcb_health_report.txt` — Human-readable summary
- HTML dashboard — Visual health overview

**Directory Structure:**
```
pcb_health_analyzer/
├── __init__.py
├── health_analyzer.py       # Main plugin entry point
├── analyzer_core.py         # Core analysis algorithms
├── drc_summary.py          # Design Rule Checker
├── gui.py                  # GUI components
├── report_generator.py     # Report creation logic
├── pcb_html_report.py      # HTML export functionality
├── requirements.txt        # Dependencies
├── Readme.md              # Full documentation
├── docs/
│   └── architecture.md     # Technical architecture
└── pcb_health_report.json  # Sample output
```

**Dependencies:**
```txt
wxPython >= 4.1.0
```

**Usage in KiCad:**
1. Install plugin (see Installation section)
2. Open PCB in KiCad Editor
3. Navigate to: `Tools → External Plugins → PCB Health Analyzer`
4. Review generated reports in project directory

**Programmatic Usage:**
```python
from pcb_health_analyzer import health_analyzer

# Initialize analyzer
analyzer = health_analyzer.HealthAnalyzer(board)

# Run analysis
results = analyzer.analyze()

# Generate reports
analyzer.generate_reports(output_dir="./reports/")
```

---

### 5. **pcb_report_generator/** — Component Report Generator
Utility for analyzing component datasets and generating design validation reports.

**Features:**
- Component counting and classification
- Duplicate component detection
- Missing value identification
- Formatted report generation
- Data validation

**Supported Component Types:**
- Resistors (R)
- Capacitors (C)
- Inductors (L)
- Integrated Circuits (U)
- Diodes (D)
- Custom types

**Input Format:**
```csv
designator,type,value
R1,Resistor,10k
C1,Capacitor,100nF
U1,IC,ATmega328
```

**Output Example:**
```
╔════════════════════════════════════════╗
║        PCB DESIGN VERIFICATION         ║
╚════════════════════════════════════════╝

Total Components: 25
├─ Resistors: 10
├─ Capacitors: 8
├─ ICs: 4
└─ Others: 3

Quality Issues:
  ✗ Duplicate Components: 2
  ✗ Missing Values: 1

Status: REVIEW REQUIRED
```

**Directory Structure:**
```
pcb_report_generator/
├── __init__.py
├── main.py              # CLI entry point
├── analyzer.py          # Component analysis logic
├── report_writer.py     # Report formatting
├── sample_data.txt      # Example input
├── report.txt          # Example output
└── Readme.md           # Documentation
```

**Quick Start:**
```bash
cd pcb_report_generator
python main.py --input sample_data.txt --output report.txt
```

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
git clone https://github.com/akshat2805p/esim-kicad-health-analyzer.git
cd esim-kicad-health-analyzer

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
git clone https://github.com/akshat2805p/esim-kicad-health-analyzer.git
cd esim-kicad-health-analyzer

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

### Example 1: Analyze PCB Health

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, './10.0/scripting/plugins/')

from pcb_health_analyzer import health_analyzer
import pcbnew

# Load PCB file
board = pcbnew.LoadBoard("design.kicad_pcb")

# Create analyzer instance
analyzer = health_analyzer.HealthAnalyzer(board)

# Run comprehensive analysis
results = analyzer.analyze()

# Print health score
print(f"Health Score: {results['health_score']}/100")
print(f"Status: {results['status']}")

# Generate formatted reports
analyzer.generate_reports(output_dir="./analysis_reports/")
```

### Example 2: Detect Design Rule Violations

```python
from advanced_pcb_checker import advanced_checker
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

# Run design checks
violations = advanced_checker.check_tracks(board, min_width=0.2)
violations += advanced_checker.check_vias(board, min_drill=0.3)
violations += advanced_checker.check_boundaries(board)

# Generate report
advanced_checker.write_report(violations, "inspection_report.txt")
```

### Example 3: Validate Component Dataset

```python
from pcb_report_generator import analyzer, report_writer

# Load component data
components = analyzer.parse_components("bom.txt")

# Analyze
stats = analyzer.analyze_components(components)
issues = analyzer.detect_issues(components)

# Generate report
report_writer.write_report(stats, issues, "component_report.txt")
```

---

## 🏗️ Architecture

### Plugin Execution Flow

```
KiCad PCB Editor
    ↓
Tools → External Plugins
    ↓
Plugin Manager (pcbnew)
    ↓
┌─────────────────────────────────────┐
│   Action Plugin Instance            │
│  (inherits ActionPlugin)            │
│  ├─ defaults()    [metadata]        │
│  ├─ Run()         [main logic]      │
│  └─ Show Dialog() [UI interaction]  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Core Analysis Modules             │
│  ├─ analyzer_core.py                │
│  ├─ drc_summary.py                  │
│  └─ report_generator.py             │
└─────────────────────────────────────┘
    ↓
Output Files (JSON, TXT, HTML)
```

### Module Dependencies

```
pcbnew (KiCad Python API)
    ↓
pcb_health_analyzer/
    ├─ health_analyzer.py ← Main entry point
    ├─ analyzer_core.py   ← Analysis logic
    ├─ report_generator.py ← Report formatting
    └─ gui.py ← UI components
```

### Data Flow

```
.kicad_pcb File
    ↓
[Parser/Analyzer]
    ↓
Analysis Results (JSON)
    ↓
[Report Generator]
    ├─ Text Report
    ├─ JSON Export
    └─ HTML Dashboard
```

---

## 🛠️ Technologies

- **Language:** Python 3.7+
- **KiCad:** 6.0+ / 10.0
- **APIs:** pcbnew (KiCad Python API), wxPython
- **Data Formats:** JSON, CSV, TXT, HTML
- **Version Control:** Git
- **CI/CD:** GitHub Actions (optional)

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
git clone https://github.com/your-username/esim-kicad-health-analyzer.git
cd esim-kicad-health-analyzer

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

- **GitHub Issues:** [Report bugs or request features](https://github.com/akshat2805p/esim-kicad-health-analyzer/issues)
- **Discussions:** [Ask questions and share ideas](https://github.com/akshat2805p/esim-kicad-health-analyzer/discussions)
- **Email:** Open an issue for direct contact

---

## 🚀 Roadmap

### Current Release ✅
- ✅ Multi-format report generation
- ✅ Health scoring system
- ✅ Design rule checking
- ✅ Component analysis

### Planned Features 📋
- [ ] Real-time PCB monitoring
- [ ] Advanced DRC with custom rules
- [ ] Integration with CI/CD pipelines
- [ ] Web-based dashboard
- [ ] Machine learning-based quality prediction
- [ ] Multi-language support

---

**Last Updated:** June 2026  
