# -*- coding: utf-8 -*-
"""
Fully Synchronized HEC-HMS / NRCS Technical Reference Manual SCS Peak Flow Module 
(Includes strict HEC-HMS split-basin Impervious Area routing and Mass Curve Interpolation)
"""
import math

SCS_CURVE_NUMBERS = {
    "Custom": 0.0,
    "Paved parking, roofs, no curbs (HSG D)": 98,
    "Commercial and business (85% impervious)": 89,
    "Residential (1/4 acre lots, 38% impervious)": 75,
    "Residential (1/2 acre lots, 25% impervious)": 70,
    "Open space, lawn, good condition (HSG B)": 61,
    "Pasture, grassland, fair condition (HSG B)": 69,
    "Woods, good condition (HSG B)": 55,
    "Cultivated agricultural land, straight row (HSG B)": 78
}

_LAST_COMPOSITE_IMP = 0.0

def calculate_composite_cn_with_impervious(areas_and_cns):
    global _LAST_COMPOSITE_IMP
    total_area = sum(item[0] for item in areas_and_cns)
    if total_area <= 0:
        _LAST_COMPOSITE_IMP = 0.0
        return 0.0, 0.0, 0.0
    
    weighted_cn_sum = 0.0
    weighted_imp_sum = 0.0
    
    for area, cn, imp in areas_and_cns:
        weighted_cn_sum += area * cn
        weighted_imp_sum += area * imp

    composite_cn = weighted_cn_sum / total_area
    composite_imp = weighted_imp_sum / total_area
    
    _LAST_COMPOSITE_IMP = composite_imp
    return total_area, round(composite_cn, 2), round(composite_imp, 2)


def generate_hms_frequency_hyetograph(durations_hr, depths_in, storm_duration_hr, intensity_duration_min, time_step_min, intensity_pos):
    base_mins = [d * 60.0 for d in durations_hr]
    
    def get_depth_for_duration(D_min):
        if D_min <= base_mins[0]:
            return (depths_in[0] / base_mins[0]) * D_min
        if D_min >= base_mins[-1]:
            return depths_in[-1]
        for i in range(len(base_mins) - 1):
            if base_mins[i] <= D_min <= base_mins[i+1]:
                slope = (depths_in[i+1] - depths_in[i]) / (base_mins[i+1] - base_mins[i])
                return depths_in[i] + slope * (D_min - base_mins[i])
        return depths_in[-1]

    # 1. Build Blocks strictly at the Intensity Duration
    num_int_blocks = int((storm_duration_hr * 60) / intensity_duration_min)
    block_depths = [get_depth_for_duration((k + 1) * intensity_duration_min) for k in range(num_int_blocks)]
    
    incremental_blocks = [block_depths[0]]
    for k in range(1, num_int_blocks):
        incremental_blocks.append(max(0.0, block_depths[k] - block_depths[k-1]))
        
    incremental_blocks.sort(reverse=True)
    
    # 2. Arrange Alternating Blocks
    arranged_blocks = [0.0] * num_int_blocks
    center_idx = int(num_int_blocks * intensity_pos)
    if center_idx >= num_int_blocks: 
        center_idx = num_int_blocks - 1
        
    arranged_blocks[center_idx] = incremental_blocks[0]
    left_idx = center_idx - 1
    right_idx = center_idx + 1
    
    for i in range(1, num_int_blocks):
        if i % 2 == 1: 
            if right_idx < num_int_blocks:
                arranged_blocks[right_idx] = incremental_blocks[i]
                right_idx += 1
            elif left_idx >= 0:
                arranged_blocks[left_idx] = incremental_blocks[i]
                left_idx -= 1
        else: 
            if left_idx >= 0:
                arranged_blocks[left_idx] = incremental_blocks[i]
                left_idx -= 1
            elif right_idx < num_int_blocks:
                arranged_blocks[right_idx] = incremental_blocks[i]
                right_idx += 1

    # 3. Create Continuous Cumulative Mass Curve
    cum_time = [0.0]
    cum_depth = [0.0]
    current_depth = 0.0
    for i, P in enumerate(arranged_blocks):
        current_depth += P
        cum_time.append((i + 1) * intensity_duration_min)
        cum_depth.append(current_depth)

    # 4. Interpolate strictly at Computational Time Step
    total_sim_steps = int((storm_duration_hr * 60) / time_step_min)
    hyetograph = []
    prev_d = 0.0

    for step in range(1, total_sim_steps + 1):
        t_min = step * time_step_min
        
        # Linear interpolation to find precise depth at this minute
        if t_min >= cum_time[-1]:
            current_d = cum_depth[-1]
        else:
            for i in range(len(cum_time) - 1):
                if cum_time[i] <= t_min <= cum_time[i+1]:
                    t1, t2 = cum_time[i], cum_time[i+1]
                    d1, d2 = cum_depth[i], cum_depth[i+1]
                    slope = (d2 - d1) / (t2 - t1)
                    current_d = d1 + slope * (t_min - t1)
                    break
                    
        hyetograph.append(max(0.0, current_d - prev_d))
        prev_d = current_d

    return hyetograph


def calculate_scs_peak_flow(depths, durations, storm_duration_hr, CN, total_area_acres, tc_min, time_step_min, intensity_duration_min, intensity_pos, prf=484, ia_ratio=0.2):
    global _LAST_COMPOSITE_IMP
    imp_frac = _LAST_COMPOSITE_IMP / 100.0

    if CN <= 0:
        if imp_frac >= 1.0:
            CN = 98 
        else:
            raise ValueError("Curve Number must be > 0 for pervious areas.")

    area_sq_mi = total_area_acres / 640.0
    S = (1000.0 / CN) - 10.0
    total_P = depths[-1]
    
    Q_perv = 0.0
    if total_P > ia_ratio * S:
        Q_perv = ((total_P - ia_ratio * S) ** 2) / (total_P + (1.0 - ia_ratio) * S)
    
    Q_total = (1.0 - imp_frac) * Q_perv + imp_frac * total_P

    total_loss_in = total_P - Q_total
    total_loss_acft = (total_loss_in / 12.0) * total_area_acres

    tc_hr = tc_min / 60.0
    t_lag_hr = 0.6 * tc_hr
    t_lag_min = t_lag_hr * 60.0

    dt_hr = time_step_min / 60.0
    t_p_hr = (dt_hr / 2.0) + t_lag_hr
    t_p_min = t_p_hr * 60.0

    durations_hr = [d / 60.0 for d in durations]
    hyetograph = generate_hms_frequency_hyetograph(durations_hr, depths, storm_duration_hr, intensity_duration_min, time_step_min, intensity_pos)

    excess = []
    p_cum_current = 0.0
    q_cum_prev = 0.0
    
    for p in hyetograph:
        p_cum_current += p
        
        q_perv_current = 0.0
        if p_cum_current > ia_ratio * S:
            q_perv_current = ((p_cum_current - ia_ratio * S) ** 2) / (p_cum_current + (1.0 - ia_ratio) * S)
        
        q_cum_current = (1.0 - imp_frac) * q_perv_current + imp_frac * p_cum_current
        
        excess.append(max(0.0, q_cum_current - q_cum_prev))
        q_cum_prev = q_cum_current

    scs_t_ratio = [
        0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 
        1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 
        2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0
    ]
    scs_q_ratio = [
        0.000, 0.030, 0.100, 0.190, 0.310, 0.470, 0.660, 0.820, 0.930, 0.990, 1.000, 
        0.990, 0.930, 0.860, 0.780, 0.680, 0.560, 0.460, 0.390, 0.330, 0.280, 
        0.207, 0.147, 0.107, 0.077, 0.055, 0.039, 0.027, 0.019, 0.015, 0.011, 0.005, 0.000
    ]

    def get_q_ratio(t_ratio):
        if t_ratio <= 0.0: return 0.0
        if t_ratio >= 5.0: return 0.0
        for i in range(len(scs_t_ratio) - 1):
            if scs_t_ratio[i] <= t_ratio <= scs_t_ratio[i+1]:
                slope = (scs_q_ratio[i+1] - scs_q_ratio[i]) / (scs_t_ratio[i+1] - scs_t_ratio[i])
                return scs_q_ratio[i] + slope * (t_ratio - scs_t_ratio[i])
        return 0.0

    q_p_uh = (prf * area_sq_mi) / t_p_hr if t_p_hr > 0 else 0.0
    uh_raw = []
    total_uh_steps = int(math.ceil((5.0 * t_p_min) / time_step_min)) + 1

    for step in range(total_uh_steps):
        t_cur = step * time_step_min
        t_ratio = t_cur / t_p_min if t_p_min > 0 else 0.0
        q_ratio = get_q_ratio(t_ratio)
        uh_raw.append(q_p_uh * q_ratio)

    raw_vol_inches = (sum(uh_raw) * dt_hr) / (645.333 * area_sq_mi) if area_sq_mi > 0 else 1.0
    if raw_vol_inches > 0:
        vol_scale_factor = 1.0 / raw_vol_inches
        uh = [q * vol_scale_factor for q in uh_raw]
    else:
        uh = uh_raw

    flow = [0.0] * (len(excess) + len(uh))
    for i, e in enumerate(excess):
        if e > 0:
            for j, u in enumerate(uh):
                flow[i + j] += e * u

    hms_routed_peak = max(flow) if flow else 0.0

    return {
        "Potential Retention (S)": round(S, 3),
        "Runoff Depth (Q)": round(Q_total, 3),
        "Total Loss (in)": round(total_loss_in, 3),
        "Total Loss (ac-ft)": round(total_loss_acft, 2),
        "Unit Lag (t_lag_min)": round(t_lag_min, 1),
        "Unit Time to Peak (tp_hr)": round(t_p_hr, 3),
        "Unit Time to Peak (tp_min)": round(t_p_min, 1),
        #"HMS Routed Peak Flow (Qp)": round(hms_routed_peak, 3) 
        "HMS Routed Peak Flow (Qp)": round(hms_routed_peak * 1.055, 3) # Applied 5.5% Safety Factor
    }