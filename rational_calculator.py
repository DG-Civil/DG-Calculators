import csv
import os

# Dictionary to store county data loaded from CSV
COUNTY_INTENSITIES = {}

RUNOFF_COEFFICIENTS = {
    "Pavement / Asphalt / Concrete": 0.90,
    "Roofs": 0.95,
    "Gravel / Packed Soil": 0.75,
    "Lawns / Sandy Soil (Flat 0-2%)": 0.10,
    "Lawns / Average Soil (2-7%)": 0.15,
    "Lawns / Steep Soil (>7%)": 0.25,
    "Agricultural / Cultivated": 0.30,
    "Woods / Forested": 0.15,
    "Custom": 0.50,
}

def load_county_data(csv_path="edblkup-2019.csv"):
    global COUNTY_INTENSITIES
    COUNTY_INTENSITIES.clear()
    
    if not os.path.exists(csv_path):
        return
    
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Identify the county column header dynamically
            county_key = next((k for k in row.keys() if k and k.strip().lower() in ['county', 'name', 'municipality']), None)
            if not county_key:
                county_key = list(row.keys())[0]
            
            county_name = row[county_key].strip()
            if not county_name:
                continue
            
            COUNTY_INTENSITIES[county_name] = {}
            
            # Extract e, b, d coefficients for each return period (e.g., e-2, b-2, d-2)
            for tr in [2, 5, 10, 25, 50, 100]:
                e_val = row.get(f"e-{tr}") or row.get(f"E-{tr}") or row.get(f"e_{tr}")
                b_val = row.get(f"b-{tr}") or row.get(f"B-{tr}") or row.get(f"b_{tr}")
                d_val = row.get(f"d-{tr}") or row.get(f"D-{tr}") or row.get(f"d_{tr}")
                
                if e_val and b_val and d_val:
                    try:
                        COUNTY_INTENSITIES[county_name][tr] = {
                            "e": float(e_val),
                            "b": float(b_val),
                            "d": float(d_val)
                        }
                    except ValueError:
                        pass

# Load data on startup
load_county_data()

def calculate_rational_peak_discharge(county_name, tr, tc, areas_and_surfaces):
    county_data = COUNTY_INTENSITIES.get(county_name, {})
    tr_params = county_data.get(int(tr))
    
    if tr_params:
        e = tr_params["e"]
        b = tr_params["b"]
        d = tr_params["d"]
        # Correct EBDLKUP-2019 IDF Intensity formula: I = b / (tc + d)^e
        intensity = b / ((tc + d) ** e)
    else:
        intensity = 0.0

    total_area = 0.0
    weighted_sum = 0.0

    for item in areas_and_surfaces:
        if len(item) == 3:
            area_val, surf_type, custom_c_val = item
        else:
            area_val, surf_type = item
            custom_c_val = 0.5

        if surf_type == "Custom":
            c_val = custom_c_val
        else:
            c_val = RUNOFF_COEFFICIENTS.get(surf_type, 0.5)

        total_area += area_val
        weighted_sum += area_val * c_val

    composite_c = (weighted_sum / total_area) if total_area > 0 else 0.0
    peak_q = composite_c * intensity * total_area if total_area > 0 else 0.0

    return intensity, total_area, composite_c, peak_q