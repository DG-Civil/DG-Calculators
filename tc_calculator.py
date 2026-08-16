# -*- coding: utf-8 -*-
"""
Core calculation module for TxDOT Time of Concentration (tc).
References TxDOT Hydraulic Design Manual, Chapter 4, Section 11.
"""

def calculate_kerby_kirpich_tc(L1, E_up1, E_down1, N, L2, E_up2, E_down2):
    """
    Calculates tc using Kerby Method (Equation 4-14) for overland flow
    and Kirpich Method (Equation 4-15) for channel flow.
    """
    if L1 <= 0 or L2 <= 0:
        raise ValueError("Lengths must be greater than zero.")
    
    # Overland slope S1 from elevations
    S1 = (E_up1 - E_down1) / L1
    if S1 <= 0:
        raise ValueError("Overland Upstream Elevation must be greater than Downstream Elevation (positive slope required).")
    
    # Channel slope S2 from elevations
    S2 = (E_up2 - E_down2) / L2
    if S2 <= 0:
        raise ValueError("Channel Upstream Elevation must be greater than Downstream Elevation (positive slope required).")

    # Kerby Equation (Equation 4-14)
    K_kerby = 0.828
    tc1_minutes = K_kerby * ((L1 * N)** 0.467 )*(S1 ** -0.235)
    tc1_hours = tc1_minutes / 60.0

    # Kirpich Equation (Equation 4-15)
    tc2_minutes = 0.0078 * (L2 ** 0.770) * (S2 ** -0.385)
    tc2_hours = tc2_minutes / 60.0

    total_tc_hours = tc1_hours + tc2_hours
    total_tc_minutes = total_tc_hours * 60.0

    return {
        "tc1_minutes": tc1_minutes,
        "tc1_hours": tc1_hours,
        "tc2_minutes": tc2_minutes,
        "tc2_hours": tc2_hours,
        "total_tc_hours": total_tc_hours,
        "total_tc_minutes": total_tc_minutes,
        "S1": S1,
        "S2": S2
    }


def calculate_nrcs_tc(
    L_sh, E_up_sh, E_down_sh, P2, n_ol,
    L_sc, E_up_sc, E_down_sc, surface_type_sc,
    L_ch, E_up_ch, E_down_ch, n_ch, R_ch
):
    """
    Calculates tc using NRCS Method (Equation 4-16), combining:
    - Sheet Flow (Equation 4-17)
    - Shallow Concentrated Flow (Equation 4-18)
    - Channel Flow (Equation 4-19)
    """
    # 1. Sheet Flow (Equation 4-17)
    if L_sh > 100:
        raise ValueError("Sheet flow length (L_sh) typically cannot exceed 100 feet per TxDOT HDM.")
    S_sh = (E_up_sh - E_down_sh) / L_sh
    if S_sh <= 0:
        raise ValueError("Sheet Flow Upstream Elevation must be greater than Downstream Elevation.")
    if P2 <= 0:
        raise ValueError("2-year 24-hour rainfall P2 must be greater than zero.")
    
    t_sh = (0.007 * ((n_ol * L_sh) ** 0.8)) / ((P2 ** 0.5) * (S_sh ** 0.4))

    # 2. Shallow Concentrated Flow (Equation 4-18)
    S_sc = (E_up_sc - E_down_sc) / L_sc
    if S_sc <= 0:
        raise ValueError("Shallow Concentrated Flow Upstream Elevation must be greater than Downstream Elevation.")
    K_factor = 20.32 if surface_type_sc == "Paved" else 16.13
    t_sc = L_sc / (3600.0 * K_factor * (S_sc ** 0.5))

    # 3. Channel Flow (Equation 4-19)
    S_ch = (E_up_ch - E_down_ch) / L_ch
    if S_ch <= 0:
        raise ValueError("Channel Flow Upstream Elevation must be greater than Downstream Elevation.")
    if n_ch <= 0:
        raise ValueError("Manning's n for channel must be greater than zero.")
    if R_ch <= 0:
        raise ValueError("Hydraulic radius R must be greater than zero.")
    
    V_ch = (1.49 / n_ch) * (R_ch ** (2.0 / 3.0)) * (S_ch ** 0.5)
    if V_ch <= 0:
        raise ValueError("Calculated channel velocity is zero or negative.")
    t_ch = L_ch / (3600.0 * V_ch)

    # Total tc (Equation 4-16)
    tc_hours = t_sh + t_sc + t_ch
    tc_minutes = tc_hours * 60.0

    return {
        "t_sh_hours": t_sh,
        "t_sh_minutes": t_sh * 60.0,
        "S_sh": S_sh,
        "t_sc_hours": t_sc,
        "t_sc_minutes": t_sc * 60.0,
        "S_sc": S_sc,
        "t_ch_hours": t_ch,
        "t_ch_minutes": t_ch * 60.0,
        "S_ch": S_ch,
        "V_ch": V_ch,
        "tc_hours": tc_hours,
        "tc_minutes": tc_minutes
    }