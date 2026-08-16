import math

def solve_normal_depth_ditch(q, n, s, shape, b, z_left, z_right):
    """Bisection solver for open channel normal depth (y) given discharge (Q) with distinct left and right side slopes."""
    y_low, y_high = 0.001, 100.0
    for _ in range(100):
        y_mid = (y_low + y_high) / 2.0
        if shape == "Triangular":
            area = 0.5 * (z_left + z_right) * (y_mid ** 2)
            perimeter = y_mid * (math.sqrt(1 + z_left**2) + math.sqrt(1 + z_right**2))
        else:
            area = (b + 0.5 * (z_left + z_right) * y_mid) * y_mid
            perimeter = b + y_mid * (math.sqrt(1 + z_left**2) + math.sqrt(1 + z_right**2))
        
        if perimeter == 0:
            q_calc = 0.0
        else:
            r = area / perimeter
            q_calc = (1.486 / n) * area * (r ** (2/3)) * (s ** 0.5)
        
        if q_calc < q:
            y_low = y_mid
        else:
            y_high = y_mid
    return (y_low + y_high) / 2.0

def solve_normal_depth_pipe(q, n, s, diameter):
    """Bisection solver for circular pipe normal depth (y) given discharge (Q)."""
    y_low, y_high = 0.001, diameter
    for _ in range(100):
        y_mid = (y_low + y_high) / 2.0
        y_effective = min(max(y_mid, 0.0001), diameter)
        ratio = 1.0 - (2.0 * y_effective / diameter)
        ratio = max(min(ratio, 1.0), -1.0)
        theta = 2.0 * math.acos(ratio)
        area = (diameter ** 2 / 8.0) * (theta - math.sin(theta))
        perimeter = (diameter / 2.0) * theta
        
        if perimeter == 0:
            q_calc = 0.0
        else:
            r = area / perimeter
            q_calc = (1.486 / n) * area * (r ** (2/3)) * (s ** 0.5)
        
        if q_calc < q:
            y_low = y_mid
        else:
            y_high = y_mid
    return (y_low + y_high) / 2.0

def calculate_ditch_hydraulics(n, s, shape, b, z_left, z_right, mode_is_calc_q, y_val, q_val):
    """Executes ditch flow analysis based on TxDOT Manning's Equation formulas with distinct left and right side slopes."""
    if mode_is_calc_q:
        y = float(y_val)
        if shape == "Triangular":
            area = 0.5 * (z_left + z_right) * (y ** 2)
            perimeter = y * (math.sqrt(1 + z_left**2) + math.sqrt(1 + z_right**2))
        else:
            area = (b + 0.5 * (z_left + z_right) * y) * y
            perimeter = b + y * (math.sqrt(1 + z_left**2) + math.sqrt(1 + z_right**2))
        
        r = area / perimeter if perimeter > 0 else 0.0
        q = (1.486 / n) * area * (r ** (2/3)) * (s ** 0.5)
        v = q / area if area > 0 else 0.0
        return {"mode": "Q", "val": q, "area": area, "velocity": v, "radius": r}
    else:
        q_target = float(q_val)
        y_calc = solve_normal_depth_ditch(q_target, n, s, shape, b, z_left, z_right)
        if shape == "Triangular":
            area = 0.5 * (z_left + z_right) * (y_calc ** 2)
            perimeter = y_calc * (math.sqrt(1 + z_left**2) + math.sqrt(1 + z_right**2))
        else:
            area = (b + 0.5 * (z_left + z_right) * y_calc) * y_calc
            perimeter = b + y_calc * (math.sqrt(1 + z_left**2) + math.sqrt(1 + z_right**2))
        
        r = area / perimeter if perimeter > 0 else 0.0
        v = q_target / area if area > 0 else 0.0
        return {"mode": "y", "val": y_calc, "area": area, "velocity": v, "radius": r}

def calculate_pipe_hydraulics(n, s, diameter, mode_is_calc_q, y_val, q_val):
    """Executes circular pipe flow analysis based on TxDOT Manning's Equation formulas."""
    if mode_is_calc_q:
        y = float(y_val)
        y_effective = min(max(y, 0.0001), diameter)
        ratio = 1.0 - (2.0 * y_effective / diameter)
        ratio = max(min(ratio, 1.0), -1.0)
        theta = 2.0 * math.acos(ratio)
        area = (diameter ** 2 / 8.0) * (theta - math.sin(theta))
        perimeter = (diameter / 2.0) * theta
        
        r = area / perimeter if perimeter > 0 else 0.0
        q = (1.486 / n) * area * (r ** (2/3)) * (s ** 0.5)
        v = q / area if area > 0 else 0.0
        filling_pct = (y_effective / diameter) * 100.0
        return {"mode": "Q", "val": q, "area": area, "velocity": v, "filling": filling_pct}
    else:
        q_target = float(q_val)
        y_calc = solve_normal_depth_pipe(q_target, n, s, diameter)
        y_effective = min(max(y_calc, 0.0001), diameter)
        ratio = 1.0 - (2.0 * y_effective / diameter)
        ratio = max(min(ratio, 1.0), -1.0)
        theta = 2.0 * math.acos(ratio)
        area = (diameter ** 2 / 8.0) * (theta - math.sin(theta))
        perimeter = (diameter / 2.0) * theta
        v = q_target / area if area > 0 else 0.0
        filling_pct = (y_effective / diameter) * 100.0
        return {"mode": "y", "val": y_calc, "area": area, "velocity": v, "filling": filling_pct}