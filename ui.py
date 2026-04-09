import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from analytics import PerformanceAnalytics
from reporting import ReportGenerator
import os

class LactateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bike Lactate Test")
        self.geometry("1300x900")
        ctk.set_appearance_mode("dark")
        self.current_data = None
        self._setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """Clean up resources before closing."""
        plt.close('all') 
        
        self.quit()
        self.destroy()

    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Input
        self.sidebar = ctk.CTkFrame(self, width=320)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="Diagnostics Input", font=("Helvetica", 20, "bold")).pack(pady=20)
        self.athlete_name = self._create_input("Athlete Name:", "Max Mustermann")
        self.watt_input = self._create_input("Watt Steps:", "100, 150, 200, 250, 300, 350")
        self.lactate_input = self._create_input("Lactate Values:", "1.1, 1.3, 1.8, 3.2, 5.5, 9.2")
        self.hr_input = self._create_input("Heart Rate Values:", "115, 128, 144, 161, 175, 188")

        self.btn_calc = ctk.CTkButton(self.sidebar, text="Analyze", command=self.run_analysis)
        self.btn_calc.pack(pady=20, padx=20)

        self.btn_pdf = ctk.CTkButton(self.sidebar, text="Save PDF Report", command=self.save_pdf, state="disabled")
        self.btn_pdf.pack(pady=5, padx=20)

        self.result_box = ctk.CTkTextbox(self.sidebar, width=280, height=300)
        self.result_box.pack(pady=20, padx=20)

        # Main Graph Area
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.fig, self.ax_l = plt.subplots(figsize=(7, 5))
        self.ax_hr = self.ax_l.twinx()
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax_l.set_facecolor('#1e1e1e')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_content)
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

    def _create_input(self, label, default):
        ctk.CTkLabel(self.sidebar, text=label).pack(pady=(5, 0))
        e = ctk.CTkEntry(self.sidebar, width=250); e.insert(0, default); e.pack(pady=5)
        return e

    def run_analysis(self):
        try:
            w = [float(x.strip()) for x in self.watt_input.get().split(",")]
            l = [float(x.strip()) for x in self.lactate_input.get().split(",")]
            hr = [float(x.strip()) for x in self.hr_input.get().split(",")]

            engine = PerformanceAnalytics(w, l, hr)
            td_w, td_hr = engine.get_threshold_dmax()
            zones = engine.calculate_training_zones(td_w, td_hr)

            self.current_data = {"td_w": td_w, "td_hr": td_hr, "zones": zones, "engine": engine, "w": w, "l": l, "hr": hr}
            
            self._update_plot(w, l, hr, engine, td_w)
            self._update_results(td_w, td_hr, zones)
            self.btn_pdf.configure(state="normal")
        except Exception as e:
            self.result_box.insert("end", f"Error: {e}")

    def _update_plot(self, w, l, hr, engine, td_w):
        self.ax_l.clear(); self.ax_hr.clear()
        x_smooth = np.linspace(min(w), max(w), 100)
        self.ax_l.plot(w, l, 'co'); self.ax_l.plot(x_smooth, engine.l_poly(x_smooth), 'c-')
        self.ax_hr.plot(x_smooth, engine.hr_poly(x_smooth), 'r--')
        self.ax_l.axvline(td_w, color='lime')
        self.canvas.draw()

    def _update_results(self, w, hr, zones):
        self.result_box.delete("1.0", "end")
        summary = f"D-MAX THRESHOLD:\nPower: {w:.1f}W\nHR:    {hr:.0f}bpm\n\nZONES:\n"
        for z, val in zones.items():
            summary += f"{z}: {val['w'][1]:.0f}W | {val['hr'][1]:.0f}bpm\n"
        self.result_box.insert("end", summary)

    def save_pdf(self):
        if self.current_data:

            if not os.path.exists("Reports"):
                os.makedirs("Reports")
                
            name = self.athlete_name.get().split(" ")
            
            filename = f"Reports/{name[0]}_{name[1]}_report.pdf"
            ReportGenerator.export_pdf(filename, self.athlete_name.get(), 
                                     self.current_data["td_w"], self.current_data["td_hr"], 
                                     self.current_data["zones"], "AI Analysis: tba")