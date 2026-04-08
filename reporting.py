from fpdf import FPDF
import datetime

class ReportGenerator:
    """Handles professional data export to PDF."""
    @staticmethod
    def export_pdf(filename, tdmax_w, tdmax_hr, zones, ai_text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Performance Diagnostics Report", ln=True, align='C')
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 10, f"Date: {datetime.date.today()}", ln=True, align='C')
        pdf.ln(10)
        
        # Results
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Threshold Results (D-Max):", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f"Power: {tdmax_w:.1f} W | Heart Rate: {tdmax_hr:.0f} bpm", ln=True)
        pdf.ln(5)

        # Zones
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Training Zones:", ln=True)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 8, "Zone", 1); pdf.cell(50, 8, "Power (W)", 1); pdf.cell(50, 8, "HR (bpm)", 1, ln=True)
        
        pdf.set_font("Helvetica", "", 10)
        for zone, r in zones.items():
            pdf.cell(40, 8, zone, 1)
            pdf.cell(50, 8, f"{r['w'][0]:.0f}-{r['w'][1]:.0f}", 1)
            pdf.cell(50, 8, f"{r['hr'][0]:.0f}-{r['hr'][1]:.0f}", 1, ln=True)
        
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "AI Analysis:", ln=True)
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 7, ai_text)
        pdf.output(filename)