import numpy as np
from scipy.optimize import fsolve, minimize_scalar

class PerformanceAnalytics:
    """Handles physiological calculations for Lactate and Heart Rate (HR)."""
    def __init__(self, watt_data, lactate_data, hr_data):
        self.w = np.array(watt_data)
        self.l = np.array(lactate_data)
        self.hr = np.array(hr_data)
        
        # Polynomial fit for Lactate (3rd degree)
        self.l_coeffs = np.polyfit(self.w, self.l, 3)
        self.l_poly = np.poly1d(self.l_coeffs)
        
        # Linear fit for Heart Rate
        self.hr_coeffs = np.polyfit(self.w, self.hr, 1)
        self.hr_poly = np.poly1d(self.hr_coeffs)

    def get_threshold_4mmol(self):
        func = lambda x: self.l_poly(x) - 4.0
        w_4 = fsolve(func, x0=np.mean(self.w))[0]
        return w_4, self.hr_poly(w_4)

    def get_threshold_dmax(self):
        x_start, x_end = self.w[0], self.w[-1]
        y_start, y_end = self.l_poly(x_start), self.l_poly(x_end)
        def distance(x):
            num = abs((y_end - y_start) * x - (x_end - x_start) * self.l_poly(x) + x_end * y_start - y_end * x_start)
            den = np.sqrt((y_end - y_start)**2 + (x_end - x_start)**2)
            return -(num / den)
        res = minimize_scalar(distance, bounds=(x_start, x_end), method='bounded')
        return res.x, self.hr_poly(res.x)

    def calculate_training_zones(self, w_threshold, hr_threshold):
        zone_map = [
            ("Z1 Recovery", 0.55),
            ("Z2 Base GA1", 0.75),
            ("Z3 Tempo GA2", 0.90),
            ("Z4 Threshold", 1.05),
            ("Z5 VO2max", 1.20)
        ]
        zones = {}
        last_w, last_hr = 0, 0
        for name, factor in zone_map:
            zones[name] = {
                "w": (last_w, w_threshold * factor),
                "hr": (last_hr, hr_threshold * factor)
            }
            last_w, last_hr = w_threshold * factor, hr_threshold * factor
        return zones