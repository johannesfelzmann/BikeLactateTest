import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import fsolve, minimize_scalar

class LactateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Laktat-Analyse Tool")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")

        # Layout-Config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Input
        self.input_frame = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.input_frame, text="Messdaten eingeben", font=("Arial", 18, "bold")).pack(pady=15)
        
        # Input Watt and Lactate
        ctk.CTkLabel(self.input_frame, text="Watt (z.B. 100, 150, 200, 250, 300):").pack(pady=(10, 0))
        self.watt_entry = ctk.CTkEntry(self.input_frame, width=200)
        self.watt_entry.insert(0, "100, 150, 200, 250, 300")
        self.watt_entry.pack(pady=5)

        ctk.CTkLabel(self.input_frame, text="Laktat (z.B. 1.2, 1.5, 2.3, 4.1, 7.2):").pack(pady=(10, 0))
        self.lactate_entry = ctk.CTkEntry(self.input_frame, width=200)
        self.lactate_entry.insert(0, "1.2, 1.5, 2.3, 4.1, 7.2")
        self.lactate_entry.pack(pady=5)

        self.calc_button = ctk.CTkButton(self.input_frame, text="Analyse starten", command=self.calculate)
        self.calc_button.pack(pady=20)

        self.result_text = ctk.CTkLabel(self.input_frame, text="", justify="left", font=("Courier New", 13))
        self.result_text.pack(pady=20)

        # Print
        self.graph_frame = ctk.CTkFrame(self, corner_radius=10)
        self.graph_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.ax.set_facecolor('#2b2b2b')
        self.fig.patch.set_facecolor('#2b2b2b')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

    def calculate(self):
        try:
            w = np.array([float(x.strip()) for x in self.watt_entry.get().split(",")])
            l = np.array([float(x.strip()) for x in self.lactate_entry.get().split(",")])

            if len(w) < 4:
                self.result_text.configure(text="Fehler: Mind. 4 Punkte nötig!")
                return

            # Polynom-Fit (Degree 3)
            coeffs = np.polyfit(w, l, 3)
            poly = np.poly1d(coeffs)
            x_range = np.linspace(min(w), max(w), 100)

            func_4mmol = lambda x: poly(x) - 4.0
            watt_4mmol = fsolve(func_4mmol, x0=np.mean(w))[0]

            x_start, x_end = w[0], w[-1]
            y_start, y_end = poly(x_start), poly(x_end)

            def distance_to_line(x):
                num = abs((y_end - y_start) * x - (x_end - x_start) * poly(x) + x_end * y_start - y_end * x_start)
                den = np.sqrt((y_end - y_start)**2 + (x_end - x_start)**2)
                return - (num / den)

            res_dmax = minimize_scalar(distance_to_line, bounds=(x_start, x_end), method='bounded')
            watt_dmax = res_dmax.x

            self.ax.clear()
            self.ax.plot(w, l, 'ro', label="Messpunkte")
            self.ax.plot(x_range, poly(x_range), 'b-', label="Laktatkurve")
            
            self.ax.axvline(watt_4mmol, color='orange', linestyle='--', label=f'4mmol: {watt_4mmol:.1f}W')
            self.ax.axvline(watt_dmax, color='lime', linestyle='--', label=f'D-Max: {watt_dmax:.1f}W')
            
            self.ax.plot([x_start, x_end], [y_start, y_end], 'g:', alpha=0.5)

            self.ax.set_xlabel("Leistung (Watt)", color="white")
            self.ax.set_ylabel("Laktat (mmol/l)", color="white")
            self.ax.tick_params(colors="white")
            self.ax.legend()
            self.ax.grid(True, alpha=0.2)
            self.canvas.draw()

            self.result_text.configure(text=(
                f"ERGEBNISSE:\n"
                f"-------------------\n"
                f"4-mmol Schwelle: {watt_4mmol:.1f} W\n"
                f"D-Max Schwelle:  {watt_dmax:.1f} W\n"
                f"Differenz:       {abs(watt_4mmol-watt_dmax):.1f} W"
            ))

        except Exception as e:
            self.result_text.configure(text=f"Fehler: {str(e)}")

if __name__ == "__main__":
    app = LactateApp()
    app.mainloop()