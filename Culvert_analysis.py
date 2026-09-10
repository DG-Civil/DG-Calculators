# -*- coding: utf-8 -*-
"""
Culvert Analysis Module (FHWA HDS-5)
"""

import flet as ft
import math
import os

FHWA_TABLE = {
    "Box - TxDOT 0° Wingwalls (Square Edge)": {"K": 0.061, "M": 0.75, "c": 0.0423, "Y": 0.82, "ke": 0.5, "shape": "box"},
    "Box - TxDOT 45° Wingwalls": {"K": 0.061, "M": 0.75, "c": 0.04, "Y": 0.81, "ke": 0.2, "shape": "box"},
    "Circular Concrete - Square Edge with Headwall": {"K": 0.0098, "M": 2.0, "c": 0.0398, "Y": 0.67, "ke": 0.5, "shape": "circular"},
    "Circular Concrete - Groove End with Headwall": {"K": 0.0078, "M": 2.0, "c": 0.0292, "Y": 0.74, "ke": 0.2, "shape": "circular"},
    "Circular CMP - Headwall": {"K": 0.0078, "M": 2.0, "c": 0.0379, "Y": 0.69, "ke": 0.5, "shape": "circular"},
    "Circular CMP - TxDOT SET (Mitered)": {"K": 0.0210, "M": 1.33, "c": 0.0463, "Y": 0.75, "ke": 0.7, "shape": "circular"}
}

def get_culvert_analysis_view(page: ft.Page):
    
    # 1. Define FilePicker and add it to the page overlay
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update()
    
    def update_dimensions(e):
        shape = FHWA_TABLE[dd_culvert_type.value]["shape"]
        if shape == "circular":
            txt_span.disabled = True
            txt_rise.disabled = True
            txt_dia.disabled = False
            txt_span.value = ""
            txt_rise.value = ""
            if not txt_dia.value: txt_dia.value = "60"
        else:
            txt_span.disabled = False
            txt_rise.disabled = False
            txt_dia.disabled = True
            txt_dia.value = ""
            if not txt_span.value: txt_span.value = "5"
            if not txt_rise.value: txt_rise.value = "5"
        page.update()

    dd_culvert_type = ft.Dropdown(
        label="Culvert Material & Inlet Edge (FHWA HDS-5)",
        options=[ft.dropdown.Option(key) for key in FHWA_TABLE.keys()],
        width=400,
        value="Box - TxDOT 45° Wingwalls",
        on_select=update_dimensions
    )    
    dd_control = ft.Dropdown(
        label="Hydraulic Control Mode",
        options=[
            ft.dropdown.Option("Auto-Governing"),
            ft.dropdown.Option("Inlet-Controlled"),
            ft.dropdown.Option("Outlet-Controlled")
        ],
        width=250,
        value="Auto-Governing"
    )
    
    txt_q = ft.TextField(label="Total Design Flow (cfs)", value="150", width=190, text_size=13)
    txt_barrels = ft.TextField(label="No. of Barrels", value="1", width=190, text_size=13)
    
    txt_span = ft.TextField(label="Span (ft)", value="5", width=190, text_size=13)
    txt_rise = ft.TextField(label="Rise (ft)", value="5", width=190, text_size=13)
    txt_dia = ft.TextField(label="Diameter (in)", value="", width=190, disabled=True, text_size=13)
    
    txt_length = ft.TextField(label="Barrel Length (ft)", value="100", width=190, text_size=13)
    txt_slope = ft.TextField(label="Slope (ft/ft)", value="0.01", width=190, text_size=13)
    txt_n = ft.TextField(label="Manning's n", value="0.012", width=190, text_size=13)
    txt_tw = ft.TextField(label="Tailwater Depth (ft)", value="3.5", width=190, text_size=13)

    result_text = ft.Text(size=16, weight=ft.FontWeight.BOLD, color="blue900")
    calc_details = ft.Text(size=14, selectable=True)

    def calculate_hydraulics(e):
        try:
            Q_total = float(txt_q.value)
            barrels = int(txt_barrels.value)
            Q = Q_total / barrels
            
            L = float(txt_length.value)
            S = float(txt_slope.value)
            n = float(txt_n.value)
            TW = float(txt_tw.value)
            
            c_type = FHWA_TABLE[dd_culvert_type.value]
            shape = c_type["shape"]
            K, M, c, Y, ke = c_type["K"], c_type["M"], c_type["c"], c_type["Y"], c_type["ke"]

            if shape == "circular":
                D_in = float(txt_dia.value)
                D = D_in / 12.0
                Span, Rise = D, D
                A = (math.pi * (D**2)) / 4
                P = math.pi * D
            else:
                Span = float(txt_span.value)
                Rise = float(txt_rise.value)
                D = Rise
                A = Span * Rise
                P = 2 * (Span + Rise)
            
            R = A / P
            V = Q / A
            g = 32.2

            Q_AD = Q / (A * math.sqrt(D))
            
            HWi_sub_ratio = c * (Q_AD**2) + Y - (0.5 * S)
            HWi_sub = HWi_sub_ratio * D
            
            if shape == "box":
                dc = ((Q / Span)**2 / g)**(1/3)
            else:
                dc = 0.325 * (Q / D)**(0.5) + 0.083 * D
            dc = min(dc, D)
            Vc = Q / (Span * dc) if shape == "box" else Q / A
            Hc = dc + (Vc**2) / (2 * g)
            
            HWi_unsub_ratio = (Hc / D) + K * (Q_AD**M) - (0.5 * S)
            HWi_unsub = HWi_unsub_ratio * D
            HWi = max(HWi_sub, HWi_unsub)

            friction_loss_term = (29 * (n**2) * L) / (R**1.33)
            H = (1 + ke + friction_loss_term) * ((V**2) / (2 * g))
            ho = max(TW, (dc + D) / 2)
            HWo = H + ho - (L * S)

            if dd_control.value == "Inlet-Controlled":
                controlling_HW = HWi
                active_control = "Inlet Control (Forced)"
            elif dd_control.value == "Outlet-Controlled":
                controlling_HW = HWo
                active_control = "Outlet Control (Forced)"
            else:
                controlling_HW = max(HWi, HWo)
                active_control = "Inlet Control" if HWi > HWo else "Outlet Control"
            
            result_text.value = f"✅ Controlling Headwater: {controlling_HW:.2f} ft ({active_control})"
            calc_details.value = (
                f"--- Flow & Geometry (Per Barrel) ---\n"
                f"Flow per barrel: {Q:.2f} cfs | Area: {A:.2f} sq.ft | Vel: {V:.2f} fps\n\n"
                f"--- Inlet Control ---\n"
                f"HWi Unsubmerged: {HWi_unsub:.2f} ft | HWi Submerged: {HWi_sub:.2f} ft\n"
                f"Max HWi: {HWi:.2f} ft\n\n"
                f"--- Outlet Control ---\n"
                f"ho (effective TW): {ho:.2f} ft | Total HWo: {HWo:.2f} ft"
            )
        except Exception as ex:
            result_text.value = "⚠️ Error in calculation."
            calc_details.value = str(ex)
        page.update()

    async def download_pdf(e):
        try:
            asset_path = os.path.join("assets", "HDS5_Analysis_Reference.pdf")
            if os.path.exists(asset_path):
                with open(asset_path, "rb") as f:
                    pdf_bytes = f.read()
                # 2. Use the persistent file_picker instance bound to page.overlay
                saved_path = await file_picker.save_file(
                    file_name="HDS5_Analysis_Reference.pdf",
                    src_bytes=pdf_bytes
                )
                if saved_path:
                    page.snack_bar = ft.SnackBar(ft.Text("✅ PDF reference downloaded successfully!"))
                    page.snack_bar.open = True
                    page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("⚠️ Reference PDF file not found in assets folder."))
                page.snack_bar.open = True
                page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ Error saving file: {ex}"))
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        padding=15,
        content=ft.Column([
            ft.Text("TxDOT / FHWA HDS-5 Culvert Analyzer", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([dd_culvert_type, dd_control], wrap=True),
            ft.Row([txt_q, txt_barrels], wrap=True),
            ft.Row([txt_span, txt_rise, txt_dia], wrap=True),
            ft.Row([txt_length, txt_slope, txt_n, txt_tw], wrap=True),
            ft.Row([
                ft.ElevatedButton("Calculate Hydraulics", on_click=calculate_hydraulics, bgcolor="blue700", color="white"),
                ft.ElevatedButton("📄 Download PDF Reference", on_click=download_pdf)
            ]),
            ft.Divider(),
            result_text,
            calc_details
        ], spacing=15, scroll=ft.ScrollMode.AUTO)
    )