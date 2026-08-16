import math
import re

def parse_station(sta_str):
    """Parses station string in '120+20' or '12020.0' format into total feet."""
    if sta_str is None:
        raise ValueError("Station cannot be empty")
    s = str(sta_str).strip()
    if not s:
        raise ValueError("Station cannot be empty")
    if '+' in s:
        parts = s.split('+')
        if len(parts) != 2:
            raise ValueError(f"Invalid station format: '{s}'. Use format like 120+20")
        return float(parts[0]) * 100.0 + float(parts[1])
    return float(s)

def format_station(sta_val):
    """Formats total feet into standard civil station format with 4 decimals (e.g. 120+20.0000)."""
    if sta_val is None:
        return "0+00.0000"
    hund = int(sta_val // 100)
    rem = sta_val % 100
    return f"{hund}+{rem:07.4f}"

def parse_bearing_or_azimuth(text):
    if text is None:
        return 0.0
    s = str(text).strip().upper()
    if not s:
        return 0.0
    
    try:
        val = float(s)
        return val % 360.0
    except ValueError:
        pass

    match = re.match(r'^([NS])\s*([\d\.\s°\'"]+)\s*([EW])$', s)
    if match:
        ns = match.group(1)
        deg_part = match.group(2).replace('°', ' ').replace("'", ' ').replace('"', ' ')
        ew = match.group(3)
        
        nums = [float(x) for x in deg_part.split() if x.strip()]
        if not nums:
            raise ValueError(f"Invalid bearing angle format: {text}")
        
        deg = nums[0]
        if len(nums) > 1:
            deg += nums[1] / 60.0
        if len(nums) > 2:
            deg += nums[2] / 3600.0
            
        if ns == 'N' and ew == 'E':
            az = deg
        elif ns == 'S' and ew == 'E':
            az = 180.0 - deg
        elif ns == 'S' and ew == 'W':
            az = 180.0 + deg
        elif ns == 'N' and ew == 'W':
            az = 360.0 - deg
        return az % 360.0
        
    raise ValueError(f"Cannot parse bearing or azimuth format: '{text}'")

def format_bearing(azimuth_deg):
    az = azimuth_deg % 360.0
    if az < 0:
        az += 360.0
        
    if 0 <= az < 90:
        quad, deg, ew = "N", az, "E"
    elif 90 <= az < 180:
        quad, deg, ew = "S", 180.0 - az, "E"
    elif 180 <= az < 270:
        quad, deg, ew = "S", az - 180.0, "W"
    else:
        quad, deg, ew = "N", 360.0 - az, "W"
        
    d = int(deg)
    m_full = (deg - d) * 60.0
    m = int(m_full)
    s = (m_full - m) * 60.0
    return f"{quad} {d}°{m:02d}'{s:05.2f}\" {ew}"

def evaluate_horizontal_alignment(speed, start_sta_str, start_north_str, start_east_str, start_bearing_str, h_data):
    results = []
    elements = []
    
    try:
        cur_sta = parse_station(start_sta_str)
        cur_north = float(start_north_str)
        cur_east = float(start_east_str)
        cur_azimuth = parse_bearing_or_azimuth(start_bearing_str)
    except Exception as ex:
        return [{"status": "FAIL", "msg": f"Global Horizontal Input Error: {str(ex)}"}], []

    for i, data in enumerate(h_data):
        idx = i + 1
        try:
            pi_sta = parse_station(data['pi_sta'])
            delta = float(data['delta'])
            turn = data.get('turn', 'Right')
            val = float(data['value'])
            input_type = data['input_type']
            
            if delta <= 0 or delta >= 180:
                results.append({"status": "FAIL", "msg": f"PI {idx}: Delta must be between 0° and 180°"})
                continue
                
            delta_rad = math.radians(delta)
            
            if input_type == "Radius":
                radius = val
                length = radius * delta_rad
            else: # Length
                length = val
                radius = length / delta_rad if delta_rad > 0 else 0
                
            tangent = radius * math.tan(delta_rad / 2.0)
            pc_sta = pi_sta - tangent
            pt_sta = pc_sta + length
            
            if pc_sta < cur_sta:
                results.append({"status": "FAIL", "msg": f"PI {idx} Error: PC ({format_station(pc_sta)}) is prior to current point ({format_station(cur_sta)})"})
                continue

            tan_length = pc_sta - cur_sta
            az_rad = math.radians(cur_azimuth)
            
            pc_north = cur_north + tan_length * math.cos(az_rad)
            pc_east = cur_east + tan_length * math.sin(az_rad)
            
            elements.append({
                "element_index": len(elements) + 1,
                "type": "Linear",
                "start_sta": format_station(cur_sta),
                "end_sta": format_station(pc_sta),
                "pc_northing": f"{pc_north:.4f}",
                "pc_easting": f"{pc_east:.4f}",
                "bearing": format_bearing(cur_azimuth),
                "length": f"{tan_length:.4f}"
            })
            
            pi_north = pc_north + tangent * math.cos(az_rad)
            pi_east = pc_east + tangent * math.sin(az_rad)
            
            if turn == "Right":
                ahead_azimuth = (cur_azimuth + delta) % 360.0
            else:
                ahead_azimuth = (cur_azimuth - delta) % 360.0
                
            chord_azimuth = (cur_azimuth + ahead_azimuth) / 2.0 if turn == "Right" else (cur_azimuth + ahead_azimuth) / 2.0
            chord_length = 2.0 * radius * math.sin(delta_rad / 2.0)
            
            # Recalculate accurately using vector from PC
            pt_north = pi_north + tangent * math.cos(math.radians(ahead_azimuth))
            pt_east = pi_east + tangent * math.sin(math.radians(ahead_azimuth))
            
            elements.append({
                "element_index": len(elements) + 1,
                "type": "Circular",
                "pc_sta": format_station(pc_sta),
                "pc_northing": f"{pc_north:.4f}",
                "pc_easting": f"{pc_east:.4f}",
                "pi_sta": format_station(pi_sta),
                "pi_northing": f"{pi_north:.4f}",
                "pi_easting": f"{pi_east:.4f}",
                "pt_sta": format_station(pt_sta),
                "pt_northing": f"{pt_north:.4f}",
                "pt_easting": f"{pt_east:.4f}",
                "radius": f"{radius:.4f}",
                "delta": f"{delta:.4f}°",
                "turn": turn,
                "back_bearing": format_bearing(cur_azimuth),
                "ahead_bearing": format_bearing(ahead_azimuth),
                "length": f"{length:.4f}"
            })
            
            cur_sta = pt_sta
            cur_north = pt_north
            cur_east = pt_east
            cur_azimuth = ahead_azimuth
            
            msg = f"PC: {format_station(pc_sta)} | HPI: {format_station(pi_sta)} | PT: {format_station(pt_sta)} | R: {radius:.4f}' | L: {length:.4f}'"
            results.append({"status": "PASS", "msg": msg})
            
        except Exception as ex:
            results.append({"status": "FAIL", "msg": f"PI {idx} Error: {str(ex)}"})
            
    return results, elements

def merge_labels(old_lbl, new_lbl):
    """Prioritizes and merges conflicting labels on exact same stations."""
    if old_lbl == new_lbl: return old_lbl
    if "Start Profile" in old_lbl: return old_lbl
    
    generics = ["Tangent", "Curve"]
    o_gen = old_lbl in generics
    n_gen = new_lbl in generics
    
    if o_gen and not n_gen: return new_lbl
    if n_gen and not o_gen: return old_lbl
    if o_gen and n_gen: return "Curve" 
    
    if new_lbl not in old_lbl:
        return f"{old_lbl} / {new_lbl}"
    return old_lbl

def evaluate_vertical_alignment(speed, start_sta_str, start_elev_str, interval_str, v_data):
    results = []
    points_dict = {}  # Using a dictionary to squash duplicates by round(Station, 4)
    
    try:
        current_sta = parse_station(start_sta_str)
        current_elev = float(start_elev_str)
        interval = float(interval_str)
        if interval <= 0:
            interval = 50.0
    except Exception as ex:
        return [{"status": "FAIL", "msg": f"Global Vertical Input Error: {str(ex)}"}], []

    last_sta = current_sta
    last_elev = current_elev
    last_g = 0.0

    for i, data in enumerate(v_data):
        idx = i + 1
        try:
            pvi_sta = parse_station(data['sta'])
            g1 = float(data['g1'])
            g2 = float(data['g2'])
            length = float(data['length'])
            
            if i == 0:
                pvi_elev = last_elev + (g1 / 100.0) * (pvi_sta - last_sta)
            else:
                pvi_elev = last_elev + (last_g / 100.0) * (pvi_sta - last_sta)
                
            pvc_sta = pvi_sta - (length / 2.0)
            pvt_sta = pvi_sta + (length / 2.0)
            
            high_sag_sta = None
            high_sag_type = None
            if length > 0 and abs(g1 - g2) > 0.0001:
                x_m = (g1 / (g1 - g2)) * length
                if 0 <= x_m <= length:
                    high_sag_sta = pvc_sta + x_m
                    high_sag_type = "High Point" if g1 > g2 else "Low Point"

            msg = f"PVI Elev: {pvi_elev:.4f}' | PVC: {format_station(pvc_sta)} | PVT: {format_station(pvt_sta)}"
            results.append({"status": "PASS", "msg": msg, "calculated_elev": f"{pvi_elev:.4f}"})
            
            seg_stations = set()
            seg_stations.add(last_sta)
            seg_stations.add(pvi_sta)
            if length > 0:
                seg_stations.add(pvc_sta)
                seg_stations.add(pvt_sta)
                if high_sag_sta is not None:
                    seg_stations.add(high_sag_sta)
            
            s_iter = math.ceil(last_sta / interval) * interval
            max_bound = pvt_sta if length > 0 else pvi_sta
            while s_iter <= max_bound:
                if s_iter >= last_sta:
                    seg_stations.add(s_iter)
                s_iter += interval

            sorted_stas = sorted(list(seg_stations))
            pvc_elev = pvi_elev - (g1 / 100.0) * (length / 2.0) if length > 0 else pvi_elev
            
            for s in sorted_stas:
                if length > 0 and pvc_sta <= s <= pvt_sta:
                    x = s - pvc_sta
                    elev = pvc_elev + (g1 / 100.0) * x + ((g2 - g1) / (200.0 * length)) * (x ** 2)
                elif length > 0 and s < pvc_sta:
                    elev = last_elev + (g1 / 100.0) * (s - last_sta)
                elif length > 0 and s > pvt_sta:
                    pvt_elev = pvi_elev + (g2 / 100.0) * (length / 2.0)
                    elev = pvt_elev + (g2 / 100.0) * (s - pvt_sta)
                else:
                    elev = last_elev + (g1 / 100.0) * (s - last_sta)

                # Prioritize Labels
                if abs(s - current_sta) < 0.0001 and i == 0:
                    pt_type = "Start Profile"
                elif length > 0 and abs(s - pvc_sta) < 0.0001:
                    pt_type = f"Start of Curve {idx} (PVC {idx})"
                elif length > 0 and abs(s - pvt_sta) < 0.0001:
                    pt_type = f"End of Curve {idx} (PVT {idx})"
                elif high_sag_sta and abs(s - high_sag_sta) < 0.0001:
                    pt_type = high_sag_type
                elif abs(s - pvi_sta) < 0.0001:
                    pt_type = f"PVI {idx}"
                elif length > 0 and pvc_sta < s < pvt_sta:
                    pt_type = "Curve"
                else:
                    pt_type = "Tangent"

                # Dictionary merge to prevent any duplicates
                sta_key = round(s, 4)
                if sta_key in points_dict:
                    existing_type = points_dict[sta_key]["Point_Type"]
                    points_dict[sta_key]["Point_Type"] = merge_labels(existing_type, pt_type)
                else:
                    points_dict[sta_key] = {
                        "Station": format_station(s),
                        "Station_Value": s,
                        "Elevation": f"{elev:.4f}",
                        "Point_Type": pt_type
                    }

            last_sta = pvi_sta
            last_elev = pvi_elev
            last_g = g2
            
        except Exception as ex:
            results.append({"status": "FAIL", "msg": f"PVI {idx} Error: {str(ex)}", "calculated_elev": "0.0000"})
            
    # Extract unique sorted points
    unique_points = list(points_dict.values())
    unique_points.sort(key=lambda x: x["Station_Value"])
    return results, unique_points