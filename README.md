# Pro Lactate Analyzer

A professional-grade performance diagnostics tool for cyclists, designed to analyze lactate step-tests. This application calculates physiological thresholds using established sports science models and generates automated training zones.

## Table of Contents
* [Features](#features)
* [Scientific Background](#scientific-background)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Mathematical Models](#mathematical-models)
* [License](#license)

---

## Features
* **Dual-Axis Visualization:** Real-time plotting of Lactate (mmol/l) and Heart Rate (bpm) against Power (Watts).
* **Threshold Calculation:** * **Fixed 4.0 mmol/l Threshold:** The classic reference point for OBLA.
    * **Modified D-Max Method:** An individualized approach based on the maximum curvature of the lactate profile.
* **Automated Training Zones:** Generates 5 distinct zones (Z1-Z5) based on the calculated D-Max threshold.
* **PDF Export:** Generates a professional diagnostic report including AI-ready interpretation placeholders.
* **Modern UI:** Built with a responsive Dark Mode interface using CustomTkinter.

---

## Scientific Background
The methodology of this software is based on the following key references in exercise physiology:

1.  **Modified D-Max Method:** Based on *Cheng et al. (1992)*, this method identifies the point on the lactate curve that yields the maximal perpendicular distance to a line connecting the first and last data points. It is considered a highly sensitive marker for the Individual Anaerobic Threshold (IAT). 
    * *Ref: Cheng, B., Kuipers, H., Snyder, A. C., Keizer, H. A., Jeukendrup, A., & Hesselink, M. (1992). A new approach for determining the lactate threshold. International Journal of Sports Medicine, 13(07), 518-522.*
2.  **4.0 mmol/l Threshold:** Popularized by *Heck et al. (1985)*, this fixed value serves as a universal baseline for the Onset of Blood Lactate Accumulation (OBLA).
    * *Ref: Heck, H., Mader, A., Hess, G., Mücke, S., Müller, R., & Hollmann, W. (1985). Justification of the 4-mmol/l Lactate Threshold. International Journal of Sports Medicine, 6(03), 117-130.*
3.  **Step-Test Protocol:** The analysis assumes a standard incremental protocol (e.g., 3 to 5-minute steps) to allow for metabolic steady-state at each stage.

---

## Project Structure
The project follows a modular **Separation of Concerns** architecture:

```text
BikeLactateTest/
├── main.py              # Entry point to launch the application
├── analytics.py         # Business logic: Curve fitting and threshold math
├── reporting.py         # Export module: PDF and CSV generation
└── ui.py                # View module: GUI layout and plot rendering
```

## Installation

1. Clone the repository:
```text
git clone [https://github.com/johannesfelzmann/BikeLactateTest.git](https://github.com/johannesfelzmann/BikeLactateTest.git)
cd BikeLactateTest
```

2. Install dependencies:
The project requires Python 3.8+ and the following libraries:
```text
pip install customtkinter matplotlib numpy scipy fpdf2
```

## Usage

1. Run the application:
```text
python main.py
```

2. Enter your test data (comma-separated values) in the sidebar:
    - Power Steps: *e.g., 100, 150, 200, 250, 300, 350*
    - Lactate Values: *e.g., 0.9, 1.1, 1.6, 2.8, 5.1, 9.4*
    - Heart Rate: *e.g., 115, 128, 144, 161, 175, 188*

4. Click **Analyze** to generate the curves and zones.

5. Export the results as a **PDF Report** for your coaching records.

## Mathematical Models

### Lactate Curve Fitting

The software utilizes a **3rd-degree Polynomial Regression** to model the lactate kinetics: 

$$f(x)=ax3+bx2+cx+d$$

This provides a smooth transition between discrete data points, allowing for precise calculation of the point of inflection.

### Heart Rate Modeling

Heart rate is modeled using a **Linear Regression**, as HR typically shows a linear correlation with power output during submaximal intensity ranges: 

$$HR(P)=mP+n$$

## License

This project is licensed under the MIT License - see the LICENSE file for details.

**Disclaimer:** *This tool is for educational and training purposes only. Always consult a physician before performing high-intensity exercise tests.*
