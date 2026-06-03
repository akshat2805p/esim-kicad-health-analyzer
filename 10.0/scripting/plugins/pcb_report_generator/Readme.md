# PCB Design Rule Report Generator

A Python-based PCB analysis utility developed as part of open-source internship contribution work.

## Features

- Reads PCB component data
- Counts components automatically
- Detects duplicate component references
- Detects missing component values
- Generates automated PCB design reports
- Modular Python architecture

---

## Project Structure

```bash
pcb_report_generator/
│
├── main.py
├── analyzer.py
├── report_writer.py
├── sample_data.txt
├── report.txt
└── README.md
```

---

## Technologies Used

- Python
- File Handling
- Data Processing
- Report Automation

---

## How to Run

### Step 1

Clone the repository

```bash
git clone <your-repo-link>
```

### Step 2

Move into the project folder

```bash
cd pcb_report_generator
```

### Step 3

Run the project

```bash
python main.py
```

---

## Output

The program generates:

- PCB statistics
- Duplicate component detection
- Missing value analysis
- Final design status report

Generated output is stored in:

```bash
report.txt
```

---

## Sample Input

```txt
R1,Resistor,10k
R2,Resistor,1k
R1,Resistor,10k
C1,Capacitor,100nF
C2,Capacitor,10uF
C3,Capacitor,
U1,IC,ATmega328
U2,IC,NE555
```

---

## Future Improvements

- GUI support
- CSV export
- KiCad PCB file integration
- Design Rule Checking (DRC)
- Real-time PCB analysis

---

## Internship Contribution

Developed as part of open-source contribution and PCB automation workflow practice.