# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:32:04 2026

@author: dawit.ghebreyesus
"""

# -*- coding: utf-8 -*-
"""
Engineering Calculator Suite
Developed by: Dawit Ghebreyesus
"""

import os
import platform
import subprocess
import webbrowser
import math
import csv
import flet as ft
import io

# Chart imports for Drainage Area Calculator with fallback across Flet versions
try:
    import flet_charts as fch
    PieChart = fch.PieChart
    PieChartSection = fch.PieChartSection
except (ImportError, AttributeError):
    PieChart = getattr(ft, "PieChart", None)
    PieChartSection = getattr(ft, "PieChartSection", None)

from rational_calculator import COUNTY_INTENSITIES, RUNOFF_COEFFICIENTS, calculate_rational_peak_discharge
from scs_calculator_v1 import SCS_CURVE_NUMBERS, calculate_composite_cn_with_impervious, calculate_scs_peak_flow
from tc_calculator import calculate_nrcs_tc, calculate_kerby_kirpich_tc
from ditch_pipe_calculator import calculate_ditch_hydraulics, calculate_pipe_hydraulics
from Drainage_Area_calculator import (
    UNIT_CONVERSIONS_TO_SQFT,
    compute_composite_c,
    compute_composite_cn as compute_area_composite_cn,
    get_subarea_label,
)
from txdot_engine import evaluate_horizontal_alignment, evaluate_vertical_alignment

try:
    from drainage_standards_data_v2 import TXDOT_DRAINAGE_STANDARDS
except ImportError:
    TXDOT_DRAINAGE_STANDARDS = [
        {
            "code": "SCC-MD",
            "category": "Single Box Culverts",
            "title": "Cast-In-Place Miscellaneous Details",
            "summary": "Miscellaneous details for cast-in-place single box culverts, including joint details, wingwall connections, and standard notes.",
            "constraints": "Miscellaneous details",
            "file_name": "CD-SCC-21.dgn",
            "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SCC-21.pdf"
        }
    ]

def open_pdf_in_system_viewer(path: str,  page: ft.Page):
    if not path:
        return False, "No valid path provided."
    try:
        if path.startswith("http://") or path.startswith("https://"):
            #webbrowser.open(path, new=2)
            page.launch_url(path, web_popup_window_name="_blank")
            return True, "Opening standard PDF in default browser..."

        if not os.path.exists(path):
            return False, f"File not found: {path}"

        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", path], check=True)
        else:
            subprocess.run(["xdg-open", path], check=True)
        return True, f"Opened '{os.path.basename(path)}' in default viewer."
    except Exception as err:
        return False, f"Error opening PDF: {str(err)}"

# ==============================================================================
# ROADWAY ALIGNMENT UI COMPONENTS
# ==============================================================================
class HorizontalPiRow(ft.Row):
    def __init__(self, index: int, delete_callback):
        super().__init__()
        self.index = index
        self.delete_callback = delete_callback
        
        self.lbl_index = ft.Text(f"PI {self.index}", width=40, weight=ft.FontWeight.BOLD)
        self.txt_pi_sta = ft.TextField(label="PI Sta (e.g. 12+50)", width=130, text_align=ft.TextAlign.RIGHT)
        self.txt_delta = ft.TextField(label="Delta (deg)", width=90, text_align=ft.TextAlign.RIGHT)
        
        self.dd_turn = ft.Dropdown(
            label="Turn",
            options=[ft.dropdown.Option("Right"), ft.dropdown.Option("Left")],
            value="Right",
            width=90
        )
        self.dd_type = ft.Dropdown(
            label="Type",
            options=[ft.dropdown.Option("Radius"), ft.dropdown.Option("Length")],
            value="Radius",
            width=100
        )
        self.txt_value = ft.TextField(label="Value (ft)", width=100, text_align=ft.TextAlign.RIGHT)
        
        self.btn_delete = ft.Button(
            content=ft.Text("Delete"), 
            color="red", 
            on_click=self.trigger_delete
        )
        self.lbl_output = ft.Text("Ready", color="grey", expand=True, size=13)
        
        self.controls = [
            self.lbl_index, 
            self.txt_pi_sta, 
            self.txt_delta, 
            self.dd_turn,
            self.dd_type, 
            self.txt_value, 
            self.btn_delete, 
            self.lbl_output
        ]
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

    def trigger_delete(self, e):
        self.delete_callback(self)

class VerticalPviRow(ft.Row):
    def __init__(self, index: int, delete_callback):
        super().__init__()
        self.index = index
        self.delete_callback = delete_callback
        
        self.lbl_index = ft.Text(f"PVI {self.index}", width=45, weight=ft.FontWeight.BOLD)
        self.txt_sta = ft.TextField(label="PVI Sta (e.g. 15+00)", width=120, text_align=ft.TextAlign.RIGHT)
        self.txt_g1 = ft.TextField(label="G1 (%)", width=80, text_align=ft.TextAlign.RIGHT)
        self.txt_g2 = ft.TextField(label="G2 (%)", width=80, text_align=ft.TextAlign.RIGHT)
        self.txt_l1 = ft.TextField(label="L1 (ft)", value="200", width=80, text_align=ft.TextAlign.RIGHT)
        self.txt_l2 = ft.TextField(label="L2 (ft)", value="200", width=80, text_align=ft.TextAlign.RIGHT)
        
        self.btn_delete = ft.Button(
            content=ft.Text("Delete"), 
            color="red", 
            on_click=self.trigger_delete
        )
        self.lbl_output = ft.Text("Ready (K: --)", color="grey", expand=True, size=13)
        
        self.controls = [
            self.lbl_index, 
            self.txt_sta, 
            self.txt_g1, 
            self.txt_g2, 
            self.txt_l1, 
            self.txt_l2, 
            self.btn_delete, 
            self.lbl_output
        ]
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

    def trigger_delete(self, e):
        self.delete_callback(self)


def main(page: ft.Page):
    page.title = "Engineering Calculator Suite"
    page.window.maximized = True
    page.window_width = 1024
    page.window_height = 720
    page.window.left = 10
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    def developer_footer():
        return ft.Container(
            content=ft.Text("Developed by : Dawit Ghebreyesus", size=22, color="#9E9E9E", italic=True),
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.only(top=15, bottom=5)
        )

    # ==========================================
    # CALCULATOR 1: STANDARD SLOPE CALCULATOR
    # ==========================================
    s_target_var = None
    s_required_vars = []
    s_current_idx = 0
    s_current_input = ""
    s_saved_values = {}

    s_main_display = ft.Text(value="What to calculate?", size=24, weight="bold")
    s_sub_display = ft.Text(value="Select a variable below to begin.", size=14, color="#616161")

    def s_reset_state():
        nonlocal s_target_var, s_required_vars, s_current_idx, s_current_input, s_saved_values
        s_target_var = None
        s_required_vars = []
        s_current_idx = 0
        s_current_input = ""
        s_saved_values = {}
        s_main_display.value = "What to calculate?"
        s_sub_display.value = "Select a variable below to begin."
        page.update()

    def s_calculate_result():
        try:
            up = s_saved_values.get("Upstream Elev", 0.0)
            dn = s_saved_values.get("Downstream Elev", 0.0)
            length = s_saved_values.get("Length", 0.0)
            slope = s_saved_values.get("Slope (%)", 0.0)

            if s_target_var == "Slope (%)":
                ans = ((up - dn) / length) * 100
                s_main_display.value = f"Slope: {ans:.2f}%"
            elif s_target_var == "Upstream Elev":
                ans = dn + ((slope / 100) * length)
                s_main_display.value = f"Upstream Elev: {ans:.2f}"
            elif s_target_var == "Downstream Elev":
                ans = up - ((slope / 100) * length)
                s_main_display.value = f"Downstream Elev: {ans:.2f}"
            elif s_target_var == "Length":
                ans = (up - dn) / (slope / 100)
                s_main_display.value = f"Length: {ans:.2f}"
            
            s_sub_display.value = "Calculation complete. Press 'C' to start over."
        except ZeroDivisionError:
            s_main_display.value = "Error: Div by Zero"
            s_sub_display.value = "Check inputs. Press 'C' to reset."
        except Exception:
            s_main_display.value = "Error"
            s_sub_display.value = "Press 'C' to reset."

    def make_var_handler(var_name):
        def var_click(e):
            nonlocal s_target_var, s_required_vars, s_current_idx, s_current_input, s_saved_values
            s_target_var = var_name
            s_saved_values = {}
            s_current_idx = 0
            s_current_input = ""

            if s_target_var == "Slope (%)":
                s_required_vars = ["Upstream Elev", "Downstream Elev", "Length"]
            elif s_target_var == "Upstream Elev":
                s_required_vars = ["Downstream Elev", "Length", "Slope (%)"]
            elif s_target_var == "Downstream Elev":
                s_required_vars = ["Upstream Elev", "Length", "Slope (%)"]
            elif s_target_var == "Length":
                s_required_vars = ["Upstream Elev", "Downstream Elev", "Slope (%)"]

            s_main_display.value = f"Input {s_required_vars[s_current_idx]}:"
            s_sub_display.value = "Waiting for input..."
            page.update()
        return var_click

    def make_num_handler(val_str):
        def num_click(e):
            nonlocal s_current_input
            if not s_target_var: return 
            if val_str == "." and "." in s_current_input: return
            if val_str == "(-)":
                s_current_input = s_current_input[1:] if s_current_input.startswith("-") else "-" + s_current_input
            else:
                s_current_input += val_str
            s_sub_display.value = s_current_input if s_current_input else "Waiting for input..."
            page.update()
        return num_click

    def s_enter_click(e):
        nonlocal s_current_idx, s_current_input
        if not s_target_var or s_current_input in ["", "-", "."]: return
        s_saved_values[s_required_vars[s_current_idx]] = float(s_current_input)
        s_current_input = ""
        s_current_idx += 1

        if s_current_idx < len(s_required_vars):
            s_main_display.value = f"Input {s_required_vars[s_current_idx]}:"
            s_sub_display.value = "Waiting for input..."
        else:
            s_calculate_result()
        page.update()

    def s_clear_click(e):
        s_reset_state()

    def btn(text, on_click, color=None, text_color=None, expand=1):
        return ft.Button(content=text, on_click=on_click, expand=expand, bgcolor=color, color=text_color, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

    s_numpad = ft.Column([
        ft.Row([btn("7", make_num_handler("7")), btn("8", make_num_handler("8")), btn("9", make_num_handler("9")), btn("C", s_clear_click, "#FFCDD2", "#B71C1C")]),
        ft.Row([btn("4", make_num_handler("4")), btn("5", make_num_handler("5")), btn("6", make_num_handler("6")), btn("Enter", s_enter_click, "#C8E6C9", "#1B5E20")]),
        ft.Row([btn("1", make_num_handler("1")), btn("2", make_num_handler("2")), btn("3", make_num_handler("3")), btn("(-)", make_num_handler("(-)"))]), 
        ft.Row([btn("0", make_num_handler("0"), expand=2), btn(".", make_num_handler(".")), ft.Container(expand=1)]),
    ], spacing=8)

    slope_calc_view = ft.Container(
        content=ft.Column([
            ft.Container(content=ft.Column([s_main_display, s_sub_display]), padding=15, bgcolor="#ECEFF1", border_radius=8, width=float("inf")),
            ft.Divider(height=10, color="transparent"),
            ft.Text("1. Select Target Variable:", weight="bold", size=14),
            ft.Row([
                ft.Button(content="Slope (%)", on_click=make_var_handler("Slope (%)"), expand=1, color="#1976D2"),
                ft.Button(content="Upstream Elev", on_click=make_var_handler("Upstream Elev"), expand=1, color="#1976D2"),
            ]),
            ft.Row([
                ft.Button(content="Downstream Elev", on_click=make_var_handler("Downstream Elev"), expand=1, color="#1976D2"),
                ft.Button(content="Length", on_click=make_var_handler("Length"), expand=1, color="#1976D2"),
            ]),
            ft.Divider(height=10),
            ft.Text("2. Enter Values:", weight="bold", size=14),
            s_numpad,
            developer_footer()
        ], scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    )

    # ==========================================
    # CALCULATOR 2: MIDDLE ELEVATION CALCULATOR
    # ==========================================
    m_required_vars = ["Top Elevation", "Top Pipe Length", "Bottom Pipe Length", "Bottom Elevation"]
    m_current_idx = 0
    m_current_input = ""
    m_saved_values = {}

    m_main_display = ft.Text(value=f"Input {m_required_vars[0]}:", size=22, weight="bold")
    m_sub_display = ft.Text(value="Waiting for input...", size=14, color="#616161")
    m_extra_display = ft.Text(value="", size=14, weight="bold", color="#1976D2")

    def m_reset_state():
        nonlocal m_current_idx, m_current_input, m_saved_values
        m_current_idx = 0
        m_current_input = ""
        m_saved_values = {}
        m_main_display.value = f"Input {m_required_vars[0]}:"
        m_sub_display.value = "Waiting for input..."
        m_extra_display.value = ""
        page.update()

    def m_calculate_result():
        try:
            top_elev = m_saved_values.get("Top Elevation", 0.0)
            top_len = m_saved_values.get("Top Pipe Length", 0.0)
            bot_len = m_saved_values.get("Bottom Pipe Length", 0.0)
            bot_elev = m_saved_values.get("Bottom Elevation", 0.0)

            total_length = top_len + bot_len
            if total_length == 0: raise ZeroDivisionError

            total_drop = top_elev - bot_elev
            drop_per_unit = total_drop / total_length
            middle_elev = top_elev - (drop_per_unit * top_len)
            slope_percent = drop_per_unit * 100

            m_main_display.value = f"Middle Elev: {middle_elev:.2f}"
            m_extra_display.value = f"Slope: {slope_percent:.2f}%"
            m_sub_display.value = "Calculation complete. Press 'C' to start over."
        except ZeroDivisionError:
            m_main_display.value = "Error: Div by Zero"
            m_extra_display.value = ""
            m_sub_display.value = "Check lengths. Press 'C' to reset."
        except Exception:
            m_main_display.value = "Error"
            m_extra_display.value = ""
            m_sub_display.value = "Press 'C' to reset."

    def make_m_num_handler(val_str):
        def m_num_click(e):
            nonlocal m_current_input
            if val_str == "." and "." in m_current_input: return
            if val_str == "(-)":
                m_current_input = m_current_input[1:] if m_current_input.startswith("-") else "-" + m_current_input
            else:
                m_current_input += val_str
            m_sub_display.value = m_current_input if m_current_input else "Waiting for input..."
            page.update()
        return m_num_click

    def m_enter_click(e):
        nonlocal m_current_idx, m_current_input
        if m_current_input in ["", "-", "."]: return
        m_saved_values[m_required_vars[m_current_idx]] = float(m_current_input)
        m_current_input = ""
        m_current_idx += 1

        if m_current_idx < len(m_required_vars):
            m_main_display.value = f"Input {m_required_vars[m_current_idx]}:"
            m_sub_display.value = "Waiting for input..."
        else:
            m_calculate_result()
        page.update()

    def m_clear_click(e):
        m_reset_state()

    middle_calc_view = ft.Container(
        content=ft.Column([
            ft.Container(content=ft.Column([m_main_display, m_extra_display, m_sub_display], spacing=4), padding=15, bgcolor="#ECEFF1", border_radius=8, width=float("inf")),
            ft.Divider(height=15, color="transparent"),
            ft.Text("Sequential Input Mode:", weight="bold", size=14),
            ft.Text("Provide parameters in order: Top Elev -> Top Len -> Bot Len -> Bot Elev", size=12, color="#78909C"),
            ft.Divider(height=10),
            ft.Column([
                ft.Row([btn("7", make_m_num_handler("7")), btn("8", make_m_num_handler("8")), btn("9", make_m_num_handler("9")), btn("C", m_clear_click, "#FFCDD2", "#B71C1C")]),
                ft.Row([btn("4", make_m_num_handler("4")), btn("5", make_m_num_handler("5")), btn("6", make_m_num_handler("6")), btn("Enter", m_enter_click, "#C8E6C9", "#1B5E20")]),
                ft.Row([btn("1", make_m_num_handler("1")), btn("2", make_m_num_handler("2")), btn("3", make_m_num_handler("3")), btn("(-)", make_m_num_handler("(-)"))]), 
                ft.Row([btn("0", make_m_num_handler("0"), expand=2), btn(".", make_m_num_handler(".")), ft.Container(expand=1)]),
            ], spacing=8),
            developer_footer()
        ], scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    )

    # ==========================================
    # CALCULATOR 3: TIME OF CONCENTRATION
    # ==========================================
    manual_url = "https://www.txdot.gov/manuals/des/hyd/chapter-4--hydrology/section-11--time-of-concentration.html"

    def manual_link_banner():
        return ft.Container(
            content=ft.Row([
                ft.Text("Reference Manual:", size=13, weight=ft.FontWeight.BOLD),
                ft.TextButton(
                    content=ft.Text("TxDOT HDM Chapter 4, Section 11"),
                    on_click=lambda e: page.run_task(ft.UrlLauncher().launch_url, manual_url)
                )
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.Padding.symmetric(vertical=5)
        )

    # KERBY-KIRPICH METHOD UI
    kk_l1 = ft.TextField(label="Overland Flow Length (L1)", suffix=ft.Text("ft"), value="300", text_size=13, width=340)
    kk_eup1 = ft.TextField(label="Overland Upstream Elevation", suffix=ft.Text("ft"), value="105.0", text_size=13, width=340)
    kk_edown1 = ft.TextField(label="Overland Downstream Elevation", suffix=ft.Text("ft"), value="100.0", text_size=13, width=340)
    
    kk_n_dropdown = ft.Dropdown(
        label="Overland Retardance Coefficient N (Table 4-5)",
        value="0.40",
        width=340,
        options=[
            ft.dropdown.Option("0.02", "Pavement (0.02)"),
            ft.dropdown.Option("0.10", "Smooth, bare, packed soil (0.10)"),
            ft.dropdown.Option("0.20", "Poor grass, cultivated rows (0.20)"),
            ft.dropdown.Option("0.40", "Pasture, average grass (0.40)"),
            ft.dropdown.Option("0.60", "Deciduous forest (0.60)"),
            ft.dropdown.Option("0.80", "Dense grass / Coniferous forest (0.80)"),
        ]
    )

    kk_l2 = ft.TextField(label="Channel Length (L2)", suffix=ft.Text("ft"), value="1200", text_size=13, width=340)
    kk_eup2 = ft.TextField(label="Channel Upstream Elevation", suffix=ft.Text("ft"), value="100.0", text_size=13, width=340)
    kk_edown2 = ft.TextField(label="Channel Downstream Elevation", suffix=ft.Text("ft"), value="82.0", text_size=13, width=340)

    kk_result_text = ft.Text("Enter parameters and click Calculate.", size=15, weight=ft.FontWeight.BOLD, color="#1B5E20")
    kk_result_container = ft.Container(content=kk_result_text, padding=15, bgcolor="#F1F8E9", border_radius=8)

    def on_kk_calculate(e):
        try:
            L1 = float(kk_l1.value)
            E_up1 = float(kk_eup1.value)
            E_down1 = float(kk_edown1.value)
            N = float(kk_n_dropdown.value)
            L2 = float(kk_l2.value)
            E_up2 = float(kk_eup2.value)
            E_down2 = float(kk_edown2.value)

            res = calculate_kerby_kirpich_tc(L1, E_up1, E_down1, N, L2, E_up2, E_down2)

            kk_result_text.value = (
                f"TOTAL TIME OF CONCENTRATION (tc):\n"
                f"  {res['total_tc_hours']:.3f} hours ({res['total_tc_minutes']:.1f} minutes)\n\n"
                f"Reference: TxDOT HDM Chapter 4, Section 11\n"
                f"• Overland Flow tc1 (Kerby Eq. 4-14): {res['tc1_minutes']:.2f} min (Slope S1: {res['S1']:.4f} ft/ft)\n"
                f"• Channel Flow tc2 (Kirpich Eq. 4-15): {res['tc2_minutes']:.2f} min (Slope S2: {res['S2']:.4f} ft/ft)"
            )
        except ValueError as err:
            kk_result_text.value = f"Error: {str(err)}"
        page.update()

    kk_calc_btn = ft.Button(
        content="Calculate Kerby-Kirpich tc", 
        on_click=on_kk_calculate, 
        bgcolor="green", 
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    kk_tab_content = ft.Column([
        ft.Text("TxDOT Kerby-Kirpich Method", size=18, weight=ft.FontWeight.BOLD),
        manual_link_banner(),
        ft.Divider(),
        ft.Text("1. Overland Flow Segment (Kerby Equation 4-14)", weight=ft.FontWeight.BOLD, color="green"),
        kk_l1, kk_eup1, kk_edown1, kk_n_dropdown,
        ft.Divider(),
        ft.Text("2. Channel Flow Segment (Kirpich Equation 4-15)", weight=ft.FontWeight.BOLD, color="green"),
        kk_l2, kk_eup2, kk_edown2,
        ft.Container(height=10),
        kk_calc_btn,
        ft.Divider(),
        kk_result_container,
        developer_footer()
    ], spacing=12, scroll=ft.ScrollMode.AUTO)

    # NRCS METHOD UI
    nrcs_l_sh = ft.TextField(label="Sheet Flow Length (L_sh, max 100 ft)", suffix=ft.Text("ft"), value="100", text_size=13, width=340)
    nrcs_eup_sh = ft.TextField(label="Sheet Flow Upstream Elevation", suffix=ft.Text("ft"), value="105.0", text_size=13, width=340)
    nrcs_edown_sh = ft.TextField(label="Sheet Flow Downstream Elevation", suffix=ft.Text("ft"), value="103.0", text_size=13, width=340)
    nrcs_p2 = ft.TextField(label="2-Year 24-Hour Rainfall Depth (P2)", suffix=ft.Text("in"), value="4.0", text_size=13, width=340)
    
    nrcs_nol_dropdown = ft.Dropdown(
        label="Sheet Flow Roughness nol (Table 4-6)",
        value="0.15",
        width=340,
        options=[
            ft.dropdown.Option("0.011", "Smooth surfaces [0.011]"),
            ft.dropdown.Option("0.05", "Fallow (no residue) [0.05]"),
            ft.dropdown.Option("0.06", "Cultivated soils (Residue <= 20%) [0.06]"),
            ft.dropdown.Option("0.17", "Cultivated soils (Residue > 20%) [0.17]"),
            ft.dropdown.Option("0.15", "Short grass prairie [0.15]"),
            ft.dropdown.Option("0.24", "Dense grass [0.24]"),
            ft.dropdown.Option("0.41", "Bermudagrass [0.41]"),
            ft.dropdown.Option("0.13", "Range (natural) [0.13]"),
            ft.dropdown.Option("0.40", "Woods (Light underbrush) [0.40]"),
            ft.dropdown.Option("0.80", "Woods (Dense underbrush) [0.80]"),
        ]
    )

    nrcs_l_sc = ft.TextField(label="Shallow Concentrated Flow Length (L_sc)", suffix=ft.Text("ft"), value="800", text_size=13, width=340)
    nrcs_eup_sc = ft.TextField(label="Shallow Flow Upstream Elevation", suffix=ft.Text("ft"), value="103.0", text_size=13, width=340)
    nrcs_edown_sc = ft.TextField(label="Shallow Flow Downstream Elevation", suffix=ft.Text("ft"), value="90.0", text_size=13, width=340)
    
    nrcs_surface_sc = ft.Dropdown(
        label="Shallow Flow Surface Type",
        value="Unpaved",
        width=340,
        options=[
            ft.dropdown.Option("Unpaved", "Unpaved Surface (K = 16.13)"),
            ft.dropdown.Option("Paved", "Paved Surface (K = 20.32)"),
        ]
    )

    nrcs_l_ch = ft.TextField(label="Channel Flow Length (L_ch)", suffix=ft.Text("ft"), value="1500", text_size=13, width=340)
    nrcs_eup_ch = ft.TextField(label="Channel Upstream Elevation", suffix=ft.Text("ft"), value="90.0", text_size=13, width=340)
    nrcs_edown_ch = ft.TextField(label="Channel Downstream Elevation", suffix=ft.Text("ft"), value="75.0", text_size=13, width=340)
    nrcs_n_ch = ft.TextField(label="Channel Manning's n", value="0.035", text_size=13, width=340)
    nrcs_r_ch = ft.TextField(label="Channel Hydraulic Radius (R)", suffix=ft.Text("ft"), value="2.0", text_size=13, width=340)

    nrcs_result_text = ft.Text("Enter parameters and click Calculate.", size=15, weight=ft.FontWeight.BOLD, color="#1B5E20")
    nrcs_result_container = ft.Container(content=nrcs_result_text, padding=15, bgcolor="#F1F8E9", border_radius=8)

    def on_nrcs_calculate(e):
        try:
            L_sh = float(nrcs_l_sh.value)
            E_up_sh = float(nrcs_eup_sh.value)
            E_down_sh = float(nrcs_edown_sh.value)
            P2 = float(nrcs_p2.value)
            n_ol = float(nrcs_nol_dropdown.value)

            L_sc = float(nrcs_l_sc.value)
            E_up_sc = float(nrcs_eup_sc.value)
            E_down_sc = float(nrcs_edown_sc.value)
            surface_type_sc = nrcs_surface_sc.value

            L_ch = float(nrcs_l_ch.value)
            E_up_ch = float(nrcs_eup_ch.value)
            E_down_ch = float(nrcs_edown_ch.value)
            n_ch = float(nrcs_n_ch.value)
            R_ch = float(nrcs_r_ch.value)

            res = calculate_nrcs_tc(
                L_sh, E_up_sh, E_down_sh, P2, n_ol,
                L_sc, E_up_sc, E_down_sc, surface_type_sc,
                L_ch, E_up_ch, E_down_ch, n_ch, R_ch
            )

            nrcs_result_text.value = (
                f"TOTAL TIME OF CONCENTRATION (tc):\n"
                f"  {res['tc_hours']:.3f} hours ({res['tc_minutes']:.1f} minutes)\n\n"
                f"Reference: TxDOT HDM Chapter 4, Section 11 (NRCS Eq. 4-16)\n"
                f"• Sheet Flow Time (Eq. 4-17): {res['t_sh_minutes']:.2f} min (Slope: {res['S_sh']:.4f})\n"
                f"• Shallow Concentrated Flow Time (Eq. 4-18): {res['t_sc_minutes']:.2f} min (Slope: {res['S_sc']:.4f})\n"
                f"• Channel Flow Time (Eq. 4-19): {res['t_ch_minutes']:.2f} min (Velocity: {res['V_ch']:.2f} ft/s; Slope: {res['S_ch']:.4f})"
            )
        except ValueError as err:
            nrcs_result_text.value = f"Error: {str(err)}"
        page.update()

    nrcs_calc_btn = ft.Button(
        content="Calculate NRCS tc", 
        on_click=on_nrcs_calculate, 
        bgcolor="blue", 
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    nrcs_tab_content = ft.Column([
        ft.Text("TxDOT NRCS Method (3-Component Breakdown)", size=18, weight=ft.FontWeight.BOLD),
        manual_link_banner(),
        ft.Divider(),
        ft.Text("1. Sheet Flow Segment (Equation 4-17)", weight=ft.FontWeight.BOLD, color="blue"),
        nrcs_l_sh, nrcs_eup_sh, nrcs_edown_sh, nrcs_p2, nrcs_nol_dropdown,
        ft.Divider(),
        ft.Text("2. Shallow Concentrated Flow Segment (Equation 4-18)", weight=ft.FontWeight.BOLD, color="blue"),
        nrcs_l_sc, nrcs_eup_sc, nrcs_edown_sc, nrcs_surface_sc,
        ft.Divider(),
        ft.Text("3. Channel Flow Segment (Equation 4-19)", weight=ft.FontWeight.BOLD, color="blue"),
        nrcs_l_ch, nrcs_eup_ch, nrcs_edown_ch, nrcs_n_ch, nrcs_r_ch,
        ft.Container(height=10),
        nrcs_calc_btn,
        ft.Divider(),
        nrcs_result_container,
        developer_footer()
    ], spacing=12, scroll=ft.ScrollMode.AUTO)

    tc_calc_view = ft.Container(
        content=ft.Column([
            ft.Text("TxDOT Time of Concentration Calculator Suite", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Tabs(
                length=2,
                selected_index=0,
                animation_duration=300,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.TabBar(
                            tabs=[
                                ft.Tab(label="Kerby-Kirpich Method"),
                                ft.Tab(label="NRCS Method"),
                            ]
                        ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                ft.Container(content=kk_tab_content, padding=20),
                                ft.Container(content=nrcs_tab_content, padding=20),
                            ]
                        )
                    ]
                )
            )
        ], expand=True),
        padding=20,
        expand=True
    )

    # ==========================================
    # CALCULATOR 4: DRAINAGE AREA (COMPOSITE C & CN)
    # ==========================================
    units_list = list(UNIT_CONVERSIONS_TO_SQFT.keys())
    chart_colors = [
        ft.Colors.BLUE_500, ft.Colors.GREEN_500, ft.Colors.ORANGE_500, ft.Colors.PURPLE_500,
        ft.Colors.TEAL_500, ft.Colors.PINK_500, ft.Colors.AMBER_500, ft.Colors.INDIGO_500,
    ]

    # --- TAB 1: RUNOFF COEFFICIENT (C) CALCULATOR ---
    c_total_area_field = ft.TextField(
        label="Total Drainage Area (Optional)", width=250, keyboard_type=ft.KeyboardType.NUMBER,
    )
    c_total_area_unit = ft.Dropdown(
        value="acres", options=[ft.dropdown.Option(u) for u in units_list], width=150,
    )
    c_rows_data = []
    c_rows_column = ft.Column(spacing=10)
    c_error_banner = ft.Text("", color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD)

    c_results_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("C Calculation Results", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_800),
                ft.Divider(),
                ft.Text("Composite Runoff Coefficient (C): --", size=14),
                ft.Text("Total Catchment Area: --", size=14),
                ft.Text("", size=12, color=ft.Colors.GREEN_700),
            ]),
            padding=15,
        ),
        visible=False,
    )

    c_chart_container = ft.Container(padding=10)
    c_chart_caption = ft.Text("", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.BLUE_800)
    c_chart_layout = ft.Column([c_chart_container, c_chart_caption], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def update_c_chart():
        sections = []
        legend_items = []
        total_val = 0.0

        for r in c_rows_data:
            val_str = r["area"].value.strip() if r["area"].value else ""
            try: v = float(val_str) if val_str != "" else 0.0
            except ValueError: v = 0.0
            total_val += v

        divisor = total_val if total_val > 0 else 1.0

        for idx, r in enumerate(c_rows_data):
            val_str = r["area"].value.strip() if r["area"].value else ""
            try: v = float(val_str) if val_str != "" else 0.0
            except ValueError: v = 0.0

            color = chart_colors[idx % len(chart_colors)]
            name = r["name"].value.strip() or f"Sub-area {get_subarea_label(idx)}"
            pct = (v / divisor) * 100 if total_val > 0 else 0.0

            if PieChartSection:
                sections.append(
                    PieChartSection(
                        value=v if v > 0 else 0.001,
                        title=f"{pct:.1f}%" if v > 0 else "0%",
                        title_style=ft.TextStyle(size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        color=color,
                        radius=55,
                    )
                )
            legend_items.append(
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=color, border_radius=2),
                    ft.Text(f"{name}: {val_str or '0'} ({pct:.1f}%)", size=12),
                ], spacing=6)
            )

        if PieChart and sections:
            chart = PieChart(sections=sections, sections_space=2, center_space_radius=25, width=160, height=160)
            c_chart_container.content = ft.Row(
                [chart, ft.VerticalDivider(), ft.Column(legend_items, spacing=4)],
                alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        else:
            c_chart_container.content = ft.Column(legend_items, spacing=4)
        page.update()

    def clear_c_caption(e):
        c_chart_caption.value = ""
        update_c_chart()

    def create_c_row(name="", area="", unit="acres", c="0.30"):
        row_ref = {}
        idx = len(c_rows_data)
        default_name = f"Sub-area {get_subarea_label(idx)}"

        name_field = ft.TextField(label="Name", value=name or default_name, width=130, dense=True, on_change=clear_c_caption)
        area_field = ft.TextField(label="Area (blank if missing)", value=str(area), width=160, dense=True, keyboard_type=ft.KeyboardType.NUMBER, on_change=clear_c_caption)
        unit_dropdown = ft.Dropdown(value=unit, options=[ft.dropdown.Option(u) for u in units_list], width=140, dense=True)
        unit_dropdown.on_change = clear_c_caption
        c_field = ft.TextField(label="Runoff Coeff (C)", value=str(c), width=130, dense=True, keyboard_type=ft.KeyboardType.NUMBER, on_change=clear_c_caption)

        def delete_row(e):
            if row_container in c_rows_column.controls: c_rows_column.controls.remove(row_container)
            if row_ref in c_rows_data: c_rows_data.remove(row_ref)
            for i, r in enumerate(c_rows_data):
                curr_val = r["name"].value.strip()
                if curr_val.startswith("Sub-area ") or not curr_val: r["name"].value = f"Sub-area {get_subarea_label(i)}"
            c_chart_caption.value = ""
            update_c_chart()

        delete_btn = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400, tooltip="Remove Sub-area", on_click=delete_row)
        row_container = ft.Row([name_field, area_field, unit_dropdown, c_field, delete_btn], alignment=ft.MainAxisAlignment.START, wrap=True)

        row_ref = {"container": row_container, "name": name_field, "area": area_field, "unit": unit_dropdown, "c": c_field}
        c_rows_data.append(row_ref)
        return row_container

    def add_c_row_click(e):
        row = create_c_row()
        c_rows_column.controls.append(row)
        c_chart_caption.value = ""
        update_c_chart()

    def calculate_c_click(e):
        c_error_banner.value = ""
        try:
            sub_list = []
            for r in c_rows_data:
                a_val = r["area"].value.strip()
                sub_list.append({
                    "name": r["name"].value.strip(),
                    "area": float(a_val) if a_val != "" else None,
                    "unit": r["unit"].value,
                    "c": float(r["c"].value) if r["c"].value.strip() else 0.0,
                })
            if not sub_list: raise ValueError("Please add at least one sub-area.")

            tot_val = c_total_area_field.value.strip()
            tot_float = float(tot_val) if tot_val != "" else None

            res = compute_composite_c(sub_list, tot_float, c_total_area_unit.value)
            solved_idx = res["solved_index"]
            if solved_idx != -1:
                c_rows_data[solved_idx]["area"].value = f"{res['sub_areas'][solved_idx]['area_display']:.4f}"

            res_controls = c_results_card.content.content.controls
            res_controls[2].value = f"Composite Runoff Coefficient (C): {res['c_composite']}"
            res_controls[3].value = f"Total Catchment Area: {res['total_acres']:.4f} acres ({res['total_sqft']:,.2f} sq ft)"
            res_controls[4].value = (f"✔ Automatically solved missing area for '{res['sub_areas'][solved_idx]['name']}' = {res['sub_areas'][solved_idx]['area_display']:.4f} {res['sub_areas'][solved_idx]['unit']}" if solved_idx != -1 else "")
            
            c_chart_caption.value = f"Composite C = {res['c_composite']}"
            c_results_card.visible = True
            update_c_chart()
        except Exception as ex:
            c_error_banner.value = f"Error: {str(ex)}"
            page.update()

    add_c_btn = ft.Button(content=ft.Text("Add Sub-Area"), icon=ft.Icons.ADD, on_click=add_c_row_click)
    calc_c_btn = ft.Button(content=ft.Text("Calculate Composite C"), icon=ft.Icons.CALCULATE, on_click=calculate_c_click, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)

    c_rows_column.controls.append(create_c_row(area="2.0", c="0.30"))
    c_rows_column.controls.append(create_c_row(area="", c="0.90"))
    c_total_area_field.value = "5.0"
    update_c_chart()

    # --- TAB 2: CURVE NUMBER (CN) CALCULATOR ---
    # [Implementation mirrors C tab]
    cn_total_area_field = ft.TextField(label="Total Drainage Area (Optional)", width=250, keyboard_type=ft.KeyboardType.NUMBER)
    cn_total_area_unit = ft.Dropdown(value="acres", options=[ft.dropdown.Option(u) for u in units_list], width=150)
    cn_rows_data = []
    cn_rows_column = ft.Column(spacing=10)
    cn_error_banner = ft.Text("", color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD)

    cn_results_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("CN Calculation Results", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.GREEN_800),
                ft.Divider(),
                ft.Text("Composite Curve Number (CN): --", size=14),
                ft.Text("Total Catchment Area: --", size=14),
                ft.Text("", size=12, color=ft.Colors.GREEN_700),
            ]),
            padding=15,
        ),
        visible=False,
    )
    cn_chart_container = ft.Container(padding=10)
    cn_chart_caption = ft.Text("", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.GREEN_800)
    cn_chart_layout = ft.Column([cn_chart_container, cn_chart_caption], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def update_cn_chart():
        sections = []
        legend_items = []
        total_val = 0.0

        for r in cn_rows_data:
            val_str = r["area"].value.strip() if r["area"].value else ""
            try: v = float(val_str) if val_str != "" else 0.0
            except ValueError: v = 0.0
            total_val += v

        divisor = total_val if total_val > 0 else 1.0

        for idx, r in enumerate(cn_rows_data):
            val_str = r["area"].value.strip() if r["area"].value else ""
            try: v = float(val_str) if val_str != "" else 0.0
            except ValueError: v = 0.0
            color = chart_colors[idx % len(chart_colors)]
            name = r["name"].value.strip() or f"Sub-area {get_subarea_label(idx)}"
            pct = (v / divisor) * 100 if total_val > 0 else 0.0

            if PieChartSection:
                sections.append(
                    PieChartSection(
                        value=v if v > 0 else 0.001,
                        title=f"{pct:.1f}%" if v > 0 else "0%",
                        title_style=ft.TextStyle(size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        color=color, radius=55,
                    )
                )
            legend_items.append(ft.Row([ft.Container(width=12, height=12, bgcolor=color, border_radius=2), ft.Text(f"{name}: {val_str or '0'} ({pct:.1f}%)", size=12)], spacing=6))

        if PieChart and sections:
            chart = PieChart(sections=sections, sections_space=2, center_space_radius=25, width=160, height=160)
            cn_chart_container.content = ft.Row([chart, ft.VerticalDivider(), ft.Column(legend_items, spacing=4)], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        else:
            cn_chart_container.content = ft.Column(legend_items, spacing=4)
        page.update()

    def clear_cn_caption(e):
        cn_chart_caption.value = ""
        update_cn_chart()

    def create_cn_row(name="", area="", unit="acres", cn="75"):
        row_ref = {}
        idx = len(cn_rows_data)
        default_name = f"Sub-area {get_subarea_label(idx)}"
        name_field = ft.TextField(label="Name", value=name or default_name, width=130, dense=True, on_change=clear_cn_caption)
        area_field = ft.TextField(label="Area (blank if missing)", value=str(area), width=160, dense=True, keyboard_type=ft.KeyboardType.NUMBER, on_change=clear_cn_caption)
        unit_dropdown = ft.Dropdown(value=unit, options=[ft.dropdown.Option(u) for u in units_list], width=140, dense=True)
        unit_dropdown.on_change = clear_cn_caption
        cn_field = ft.TextField(label="Curve Number (CN)", value=str(cn), width=130, dense=True, keyboard_type=ft.KeyboardType.NUMBER, on_change=clear_cn_caption)

        def delete_row(e):
            if row_container in cn_rows_column.controls: cn_rows_column.controls.remove(row_container)
            if row_ref in cn_rows_data: cn_rows_data.remove(row_ref)
            for i, r in enumerate(cn_rows_data):
                curr_val = r["name"].value.strip()
                if curr_val.startswith("Sub-area ") or not curr_val: r["name"].value = f"Sub-area {get_subarea_label(i)}"
            cn_chart_caption.value = ""
            update_cn_chart()

        delete_btn = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400, tooltip="Remove Sub-area", on_click=delete_row)
        row_container = ft.Row([name_field, area_field, unit_dropdown, cn_field, delete_btn], alignment=ft.MainAxisAlignment.START, wrap=True)
        row_ref = {"container": row_container, "name": name_field, "area": area_field, "unit": unit_dropdown, "cn": cn_field}
        cn_rows_data.append(row_ref)
        return row_container

    def add_cn_row_click(e):
        row = create_cn_row()
        cn_rows_column.controls.append(row)
        cn_chart_caption.value = ""
        update_cn_chart()

    def calculate_cn_click(e):
        cn_error_banner.value = ""
        try:
            sub_list = []
            for r in cn_rows_data:
                a_val = r["area"].value.strip()
                sub_list.append({
                    "name": r["name"].value.strip(),
                    "area": float(a_val) if a_val != "" else None,
                    "unit": r["unit"].value,
                    "cn": float(r["cn"].value) if r["cn"].value.strip() else 0.0,
                })
            if not sub_list: raise ValueError("Please add at least one sub-area.")

            tot_val = cn_total_area_field.value.strip()
            tot_float = float(tot_val) if tot_val != "" else None

            res = compute_area_composite_cn(sub_list, tot_float, cn_total_area_unit.value)
            solved_idx = res["solved_index"]
            if solved_idx != -1:
                cn_rows_data[solved_idx]["area"].value = f"{res['sub_areas'][solved_idx]['area_display']:.4f}"

            res_controls = cn_results_card.content.content.controls
            res_controls[2].value = f"Composite Curve Number (CN): {res['cn_composite']}"
            res_controls[3].value = f"Total Catchment Area: {res['total_acres']:.4f} acres ({res['total_sqft']:,.2f} sq ft)"
            res_controls[4].value = (f"✔ Automatically solved missing area for '{res['sub_areas'][solved_idx]['name']}' = {res['sub_areas'][solved_idx]['area_display']:.4f} {res['sub_areas'][solved_idx]['unit']}" if solved_idx != -1 else "")
            
            cn_chart_caption.value = f"Composite CN = {res['cn_composite']}"
            cn_results_card.visible = True
            update_cn_chart()
        except Exception as ex:
            cn_error_banner.value = f"Error: {str(ex)}"
            page.update()

    add_cn_btn = ft.Button(content=ft.Text("Add Sub-Area"), icon=ft.Icons.ADD, on_click=add_cn_row_click)
    calc_cn_btn = ft.Button(content=ft.Text("Calculate Composite CN"), icon=ft.Icons.CALCULATE, on_click=calculate_cn_click, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)

    cn_rows_column.controls.append(create_cn_row(area="2.0", cn="75"))
    cn_rows_column.controls.append(create_cn_row(area="", cn="90"))
    cn_total_area_field.value = "5.0"
    update_cn_chart()

    c_tab_content = ft.Column([
        ft.Container(height=5),
        ft.Text("Total Catchment Area (Optional if all sub-areas are provided):", weight=ft.FontWeight.BOLD, size=13),
        ft.Row([c_total_area_field, c_total_area_unit], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        ft.Text("Sub-Areas Breakdown & Proportion Analysis:", weight=ft.FontWeight.BOLD, size=14),
        ft.Row([c_rows_column, c_chart_layout], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
        ft.Container(height=10),
        ft.Row([add_c_btn, calc_c_btn]),
        ft.Container(height=10),
        c_error_banner,
        c_results_card,
    ], scroll=ft.ScrollMode.AUTO)

    cn_tab_content = ft.Column([
        ft.Container(height=5),
        ft.Text("Total Catchment Area (Optional if all sub-areas are provided):", weight=ft.FontWeight.BOLD, size=13),
        ft.Row([cn_total_area_field, cn_total_area_unit], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        ft.Text("Sub-Areas Breakdown & Proportion Analysis:", weight=ft.FontWeight.BOLD, size=14),
        ft.Row([cn_rows_column, cn_chart_layout], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
        ft.Container(height=10),
        ft.Row([add_cn_btn, calc_cn_btn]),
        ft.Container(height=10),
        cn_error_banner,
        cn_results_card,
    ], scroll=ft.ScrollMode.AUTO)

    drainage_area_calc_view = ft.Container(
        content=ft.Column([
            ft.Text("Drainage Area", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Tabs(
                selected_index=0, length=2, expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.TabBar(tabs=[ft.Tab(label="Composite C (Rational Method)"), ft.Tab(label="Composite CN (SCS Method)")]),
                        ft.TabBarView(expand=True, controls=[ft.Container(content=c_tab_content, padding=15), ft.Container(content=cn_tab_content, padding=15)]),
                    ],
                ),
            ),
            developer_footer()
        ], expand=True),
        padding=20, expand=True
    )

    # ==========================================
    # CALCULATOR 5: RATIONAL METHOD
    # ==========================================
    selected_county_name = None
    selected_county_text = ft.Text("Selected County: None", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    e_field = ft.TextField(label="Parameter e", value="0.0", width=130, text_size=13, read_only=True)
    b_field = ft.TextField(label="Parameter b", value="0.0", width=130, text_size=13, read_only=True)
    d_field = ft.TextField(label="Parameter d", value="0.0", width=130, text_size=13, read_only=True)
    tc_field = ft.TextField(label="Time of Concentration (min)", value="15", width=200, text_size=13)
    
    def update_idf_parameters(e=None):
        if selected_county_name and selected_county_name in COUNTY_INTENSITIES:
            try: tr = int(return_period_dropdown.value)
            except (ValueError, TypeError): tr = 10
            tr_params = COUNTY_INTENSITIES[selected_county_name].get(tr)
            if tr_params:
                e_field.value = str(tr_params["e"])
                b_field.value = str(tr_params["b"])
                d_field.value = str(tr_params["d"])
                e_field.update(); b_field.update(); d_field.update()

    return_period_dropdown = ft.Dropdown(
        label="Return Period (Years)", value="10",
        options=[ft.dropdown.Option("2"), ft.dropdown.Option("5"), ft.dropdown.Option("10"), ft.dropdown.Option("25"), ft.dropdown.Option("50"), ft.dropdown.Option("100")],
        width=200, text_size=13, on_select=update_idf_parameters
    )

    result_intensity = ft.Text("Design Rainfall Intensity (i): -- in/hr", size=15, weight=ft.FontWeight.BOLD)
    result_peak_q = ft.Text("Peak Discharge (Q): -- cfs", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)

    area_rows = []
    total_area_text = ft.Text("Total Area: 0.00 acres", weight=ft.FontWeight.BOLD)
    composite_c_text = ft.Text("Composite Weighted C: 0.00", weight=ft.FontWeight.BOLD)

    def select_county(county_name):
        nonlocal selected_county_name
        selected_county_name = county_name
        selected_county_text.value = f"Selected County: {county_name}"
        selected_county_text.update()
        update_idf_parameters()

    county_search = ft.TextField(label="Search County", hint_text="Type to filter...", text_size=13)
    county_list_view = ft.ListView(expand=1, spacing=2, padding=5, height=150)

    def update_county_list(e):
        query = county_search.value.lower()
        county_list_view.controls.clear()
        for county in sorted(COUNTY_INTENSITIES.keys()):
            if query in county.lower():
                county_list_view.controls.append(ft.TextButton(content=ft.Text(county), on_click=lambda _, c=county: select_county(c)))
        county_list_view.update()

    county_search.on_change = update_county_list
    for county in sorted(COUNTY_INTENSITIES.keys()):
        county_list_view.controls.append(ft.TextButton(content=ft.Text(county), on_click=lambda _, c=county: select_county(c)))

    def add_area_row(e=None):
        area_input = ft.TextField(label="Area (acres)", width=110, value="1.0", text_size=13)
        surface_keys = list(RUNOFF_COEFFICIENTS.keys())
        initial_surface = surface_keys[0] if surface_keys[0] != "Custom" else (surface_keys[1] if len(surface_keys) > 1 else "Custom")
        
        c_input = ft.TextField(label="C Value", width=80, value=str(RUNOFF_COEFFICIENTS.get(initial_surface, "")), text_size=13, disabled=True)
        
        def on_surface_change(e):
            val = e.control.value
            if val == "Custom":
                c_input.disabled = False
                c_input.value = "" 
            else:
                c_input.disabled = True
                c_input.value = str(RUNOFF_COEFFICIENTS.get(val, ""))
            c_input.update()

        surface_dropdown = ft.Dropdown(label="Surface Type", options=[ft.dropdown.Option(k) for k in surface_keys], value=initial_surface, width=240, text_size=13, on_select=on_surface_change)
        row_container = ft.Row(alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        def remove_row(e):
            if row_container in rows_column.controls: rows_column.controls.remove(row_container)
            for item in area_rows[:]:
                if item[0] == row_container: area_rows.remove(item)
            rows_column.update()
            
        remove_btn = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, tooltip="Remove Surface", on_click=remove_row)
        row_container.controls = [area_input, surface_dropdown, c_input, remove_btn]
        area_rows.append((row_container, area_input, surface_dropdown, c_input))
        rows_column.controls.append(row_container)
        
        if e is not None and rows_column.page: rows_column.update()

    rows_column = ft.Column([], scroll=ft.ScrollMode.AUTO, height=160)
    add_area_row()

    def handle_rational_calculation(e):
        try:
            if not selected_county_name:
                result_peak_q.value = "Error: Please select a county."
                result_peak_q.update()
                return

            tc = float(tc_field.value)
            tr = int(return_period_dropdown.value)
            
            areas_and_surfaces = []
            for container, a_inp, s_drop, c_inp in area_rows:
                val_a = float(a_inp.value or 0)
                surf_type = s_drop.value
                val_c = float(c_inp.value) if surf_type == "Custom" and c_inp.value else RUNOFF_COEFFICIENTS.get(surf_type, 0.0)
                areas_and_surfaces.append((val_a, surf_type, val_c))

            intensity, total_a, composite_c, peak_q = calculate_rational_peak_discharge(selected_county_name, tr, tc, areas_and_surfaces)

            result_intensity.value = f"Design Rainfall Intensity (i): {intensity:.2f} in/hr"
            total_area_text.value = f"Total Area: {total_a:.2f} acres"
            composite_c_text.value = f"Composite Weighted C: {composite_c:.3f}"
            result_peak_q.value = f"Peak Discharge (Q): {peak_q:.2f} cfs"

            result_intensity.update(); total_area_text.update(); composite_c_text.update(); result_peak_q.update()
        except ValueError:
            result_peak_q.value = "Error: Please check numeric inputs."
            result_peak_q.update()

    calc_button = ft.Button(content="Calculate Peak Discharge (Q)", on_click=handle_rational_calculation, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

    rational_calc_view = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("County Database", weight=ft.FontWeight.BOLD),
                    county_search,
                    ft.Container(content=county_list_view, border=ft.Border.all(1, "#CFD8DC"), border_radius=8, padding=5),
                    selected_county_text,
                ], width=280),
                ft.VerticalDivider(width=20),
                ft.Column([
                    ft.Text("IDF Curve Parameters (from CSV)", weight=ft.FontWeight.BOLD),
                    ft.Row([e_field, b_field, d_field]),
                    ft.Row([tc_field, return_period_dropdown]),
                    ft.Divider(height=10),
                    ft.Text("Drainage Area Components", weight=ft.FontWeight.BOLD),
                    rows_column,
                    ft.Button(content="Add Surface Area Row", on_click=add_area_row),
                    ft.Row([total_area_text, composite_c_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=10),
                    calc_button,
                    result_intensity,
                    result_peak_q,
                ], expand=True)
            ], expand=True),
            developer_footer()
        ], expand=True),
        padding=20, expand=True
    )

    # ==========================================
    # CALCULATOR 6: SCS METHOD PEAK FLOW
    # ==========================================
    scs_storm_duration = ft.Dropdown(label="Storm Duration (hr)", options=[ft.dropdown.Option("2"), ft.dropdown.Option("6"), ft.dropdown.Option("12"), ft.dropdown.Option("24")], value="24", width=140, text_size=13)
    scs_intensity_duration = ft.Dropdown(label="Intensity Duration", options=[ft.dropdown.Option("5-Min"), ft.dropdown.Option("15-Min"), ft.dropdown.Option("1-Hour"), ft.dropdown.Option("3-Hours")], value="1-Hour", width=140, text_size=13)
    scs_intensity_position = ft.TextField(label="Intensity Position (%)", value="50", width=140, text_size=13)
    scs_prf_field = ft.TextField(label="Peak Rate Factor (PRF)", value="484", width=140, text_size=13)
    
    scs_tc_field = ft.TextField(label="Time of Concentration, tc (min)", value="30", width=200, text_size=13)
    scs_time_step_field = ft.TextField(label="Computational Time Step, dt (min)", value="5", width=200, text_size=13)

    depth_table_inputs = [
        ("5 Min", ft.TextField(value="1.23", width=90, text_size=12)), ("15 Min", ft.TextField(value="2.44", width=90, text_size=12)),
        ("1 Hr", ft.TextField(value="4.55", width=90, text_size=12)), ("2 Hr", ft.TextField(value="6.16", width=90, text_size=12)),
        ("3 Hr", ft.TextField(value="7.27", width=90, text_size=12)), ("6 Hr", ft.TextField(value="9.04", width=90, text_size=12)),
        ("12 Hr", ft.TextField(value="10.49", width=90, text_size=12)), ("24 Hr", ft.TextField(value="11.82", width=90, text_size=12)),
    ]

    scs_area_rows = []
    scs_total_area_text = ft.Text("Total Area: 0.00 acres", weight=ft.FontWeight.BOLD)
    scs_composite_cn_text = ft.Text("Composite Effective CN: 0.00", weight=ft.FontWeight.BOLD)

    scs_res_s = ft.Text("Potential Retention (S): -- in", size=13)
    scs_res_q = ft.Text("Runoff Depth (Q): -- in", size=13)
    scs_res_tp = ft.Text("Unit Hydrograph tp: -- min", size=13)
    scs_res_hms_time = ft.Text("Est. HMS Clock Time of Peak: --:--", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    scs_res_loss = ft.Text("Total Loss: -- in (-- ac-ft)", size=13, color=ft.Colors.GREY_700) 
    scs_res_hms_qp = ft.Text("HMS Routed Peak (Qp): -- cfs", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
    
    def add_scs_area_row(e=None):
        area_input = ft.TextField(label="Area (acres)", width=95, value="1.0", text_size=13)
        cn_keys = list(SCS_CURVE_NUMBERS.keys())
        initial_cn_key = cn_keys[1] if len(cn_keys) > 1 else "Custom"
        
        cn_input = ft.TextField(label="Curve Number (CN)", width=100, value=str(SCS_CURVE_NUMBERS.get(initial_cn_key, "")), text_size=13, disabled=True)
        impervious_input = ft.TextField(label="Impervious %", width=95, value="0.0", text_size=13)
        
        def on_cn_type_change(e):
            val = e.control.value
            if val == "Custom":
                cn_input.disabled = False
                cn_input.value = ""
            else:
                cn_input.disabled = True
                cn_input.value = str(SCS_CURVE_NUMBERS.get(val, ""))
            cn_input.update()

        cn_dropdown = ft.Dropdown(label="Land Use / Soil Type", options=[ft.dropdown.Option(k) for k in cn_keys], value=initial_cn_key, width=220, text_size=13, on_select=on_cn_type_change)
        row_container = ft.Row(alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        def remove_scs_row(e):
            if row_container in scs_rows_column.controls: scs_rows_column.controls.remove(row_container)
            for item in scs_area_rows[:]:
                if item[0] == row_container: scs_area_rows.remove(item)
            scs_rows_column.update()
            
        remove_btn = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=remove_scs_row)
        row_container.controls = [area_input, cn_dropdown, cn_input, impervious_input, remove_btn]
        scs_area_rows.append((row_container, area_input, cn_dropdown, cn_input, impervious_input))
        scs_rows_column.controls.append(row_container)
        if e is not None and scs_rows_column.page: scs_rows_column.update()

    scs_rows_column = ft.Column([], scroll=ft.ScrollMode.AUTO, height=150)
    add_scs_area_row()

    def handle_scs_calculation(e):
        try:
            tc_min_val = float(scs_tc_field.value)
            time_step_min_val = float(scs_time_step_field.value)
            prf_val = float(scs_prf_field.value)
            storm_dur = float(scs_storm_duration.value)
            int_pos = float(scs_intensity_position.value) / 100.0

            int_dur_str = scs_intensity_duration.value
            int_dur_map = {"5-Min": 5, "15-Min": 15, "1-Hour": 60, "3-Hours": 180}
            int_dur_min = int_dur_map.get(int_dur_str, 5)

            durations_min = [5, 15, 60, 120, 180, 360, 720, 1440]
            depths_val = [float(ctrl.value or 0.0) for _, ctrl in depth_table_inputs]

            areas_and_cns_imp = []
            for container, a_inp, cn_drop, cn_inp, imp_inp in scs_area_rows:
                val_a = float(a_inp.value or 0)
                val_cn = float(cn_inp.value) if cn_drop.value == "Custom" else SCS_CURVE_NUMBERS.get(cn_drop.value, 0.0)
                val_imp = float(imp_inp.value or 0.0)
                areas_and_cns_imp.append((val_a, val_cn, val_imp))

            total_area, composite_cn, composite_imp = calculate_composite_cn_with_impervious(areas_and_cns_imp)
            if total_area <= 0:
                scs_res_hms_qp.value = "Error: Total area must be > zero."
                scs_res_hms_qp.update()
                return

            results = calculate_scs_peak_flow(
                depths=depths_val, durations=durations_min, storm_duration_hr=storm_dur,
                CN=composite_cn, total_area_acres=total_area, tc_min=tc_min_val,
                time_step_min=time_step_min_val, intensity_duration_min=int_dur_min, 
                intensity_pos=int_pos, prf=prf_val
            )

            peak_rain_hr = storm_dur * int_pos
            total_clock_time_hr = peak_rain_hr + results['Unit Time to Peak (tp_hr)']
            clock_hr = int(total_clock_time_hr)
            clock_min = int(round((total_clock_time_hr - clock_hr) * 60))
            if clock_min == 60: clock_min = 0; clock_hr += 1

            scs_total_area_text.value = f"Total Area: {total_area:.2f} acres"
            scs_composite_cn_text.value = f"Effective CN: {composite_cn:.2f} (Imp: {composite_imp}%)"
            scs_res_s.value = f"Potential Retention (S): {results['Potential Retention (S)']} in"
            scs_res_q.value = f"Runoff Depth (Q): {results['Runoff Depth (Q)']} in"
            scs_res_tp.value = f"Unit Hydrograph tp: {results['Unit Time to Peak (tp_min)']} min"
            scs_res_hms_time.value = f"Est. HMS Clock Time of Peak: {clock_hr:02d}:{clock_min:02d}"
            
            scs_res_loss.value = f"Total Loss: {results['Total Loss (in)']} in ({results['Total Loss (ac-ft)']} ac-ft)"
            scs_res_hms_qp.value = f"HMS Routed Peak (Qp): {results['HMS Routed Peak Flow (Qp)']} cfs"

            for ctrl in [scs_total_area_text, scs_composite_cn_text, scs_res_s, scs_res_q, scs_res_tp, scs_res_hms_time, scs_res_loss, scs_res_hms_qp]:
                ctrl.update()
        except ValueError:
            scs_res_hms_qp.value = "Error: Please verify all numeric inputs."
            scs_res_hms_qp.update()
            
    scs_calc_button = ft.Button(content="Calculate SCS Peak Flow", on_click=handle_scs_calculation, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

    frequency_storm_section = ft.Container(
        content=ft.Column([
            ft.Text("Meteorological Model: Frequency Storm Parameters", weight=ft.FontWeight.BOLD, size=13),
            ft.Row([scs_storm_duration, scs_intensity_duration, scs_intensity_position, scs_prf_field], wrap=True),
            ft.Text("Frequency Storm Depth-Duration Table (Inches)", weight=ft.FontWeight.W_500, size=12),
            ft.Row([ft.Text(label, size=11, width=90) for label, _ in depth_table_inputs], wrap=True),
            ft.Row([ctrl for _, ctrl in depth_table_inputs], wrap=True),
        ]),
        padding=10, bgcolor="#F5F5F5", border_radius=8
    )
    
    atlas14_link = ft.TextButton(content=ft.Text("NOAA Atlas 14 Precipitation Data (Texas)"), url="https://hdsc.nws.noaa.gov/pfds/pfds_map_cont.html?bkmrk=txt")
    txdot_ref_text = ft.Row([
        ft.Text("TxDOT recommends to use the Annual maximum (", size=12, italic=True),
        ft.TextButton(content=ft.Text("reference chapter 14 section 13"), url="https://www.txdot.gov/manuals/des/hyd/chapter-4--hydrology/section-13--hydrograph-method/design-storm-development.html", style=ft.ButtonStyle(padding=0)),
        ft.Text(")", size=12, italic=True)
    ], wrap=True, spacing=0)

    scs_calc_view = ft.Container(
        content=ft.Column([
            ft.Text("SCS Peak Discharge Method", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            frequency_storm_section,
            atlas14_link, txdot_ref_text,
            ft.Divider(height=10),
            ft.Row([scs_tc_field, scs_time_step_field], wrap=True),
            ft.Divider(height=10),
            ft.Text("Watershed Drainage Subareas", weight=ft.FontWeight.BOLD),
            scs_rows_column,
            ft.Button(content="Add Subarea Row", on_click=add_scs_area_row),
            ft.Row([scs_total_area_text, scs_composite_cn_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=10),
            scs_calc_button,
            ft.Row([scs_res_s, scs_res_q, scs_res_tp], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([scs_res_hms_time, scs_res_loss], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), 
            scs_res_hms_qp
        ], expand=True, scroll=ft.ScrollMode.AUTO),
        padding=20, expand=True
    )

    # ==========================================
    # CALCULATOR 7: PIPES & DITCHES ANALYSIS
    # ==========================================
    def get_flow_type(v, dm):
        if dm <= 0: return "Unknown"
        g = 32.2
        fr = v / math.sqrt(g * dm)
        if fr < 0.95: return f"Subcritical (Fr = {fr:.2f})"
        elif fr > 1.05: return f"Supercritical (Fr = {fr:.2f})"
        else: return f"Critical (Fr = {fr:.2f})"

    OptionClass = getattr(ft, "Option", getattr(ft.dropdown, "Option", None))

    d_n = ft.TextField(label="Manning's Roughness (n)", value="0.030", width=210, text_size=13)
    d_s = ft.TextField(label="Bed Slope (S) [ft/ft]", value="0.005", width=210, text_size=13)
    d_z_left = ft.TextField(label="Left Side Slope [H:1V]", value="3.0", width=210, text_size=13)
    d_z_right = ft.TextField(label="Right Side Slope [H:1V]", value="3.0", width=210, text_size=13)
    d_b = ft.TextField(label="Bottom Width (b) [ft] (Trapezoidal Only)", value="2.0", width=280, disabled=True, text_size=13)
    d_y = ft.TextField(label="Normal Depth (y) [ft]", value="1.5", width=220, disabled=False, text_size=13)
    d_q = ft.TextField(label="Discharge (Q) [cfs]", value="25.0", width=220, disabled=True, text_size=13)

    def on_ditch_shape_change(e):
        is_trapezoidal = (e.control.value == "Trapezoidal")
        d_b.disabled = not is_trapezoidal
        d_b.update()
        page.update()

    def on_ditch_mode_change(e):
        is_calc_q = "Discharge (Q) from" in e.control.value
        d_y.disabled = not is_calc_q
        d_q.disabled = is_calc_q
        d_y.update()
        d_q.update()
        page.update()

    ditch_shape_dd = ft.Dropdown(label="Ditch Cross-Section Shape", options=[OptionClass("Triangular"), OptionClass("Trapezoidal")], value="Triangular", width=280, text_size=13, on_select=on_ditch_shape_change)
    ditch_mode_dd = ft.Dropdown(label="Calculation Mode", options=[OptionClass("Calculate Discharge (Q) from Normal Depth (y)"), OptionClass("Calculate Normal Depth (y) from Discharge (Q)")], value="Calculate Discharge (Q) from Normal Depth (y)", width=420, text_size=13, on_select=on_ditch_mode_change)

    d_result_txt = ft.Text(value="Configure parameters above and click 'Run Ditch Analysis'.", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
    d_equation_txt = ft.Text(
        spans=[
            ft.TextSpan("Reference: TxDOT Hydraulic Design Manual (Eq. 6-2 & 6-3)", style=ft.TextStyle(color=ft.Colors.BLUE_600, decoration=ft.TextDecoration.UNDERLINE), url="https://www.txdot.gov/manuals/des/hyd/chapter-6--hydraulic-principles.html#_74b76647-1934-40bc-b514-d98ef3d10cde"),
            ft.TextSpan("\nManning's Eq: Q = (1.486 / n) * A * R^(2/3) * S^(1/2)")
        ], size=11, italic=True, color=ft.Colors.GREY_600
    )

    def on_run_ditch(e):
        try:
            if not d_n.value.strip(): raise ValueError("Manning's 'n' field is empty.")
            if not d_s.value.strip(): raise ValueError("Bed Slope 'S' field is empty.")
            if not d_z_left.value.strip(): raise ValueError("Left Side Slope field is empty.")
            if not d_z_right.value.strip(): raise ValueError("Right Side Slope field is empty.")

            n, s, z_left, z_right = float(d_n.value), float(d_s.value), float(d_z_left.value), float(d_z_right.value)
            b = float(d_b.value) if not d_b.disabled else 0.0
            shape = ditch_shape_dd.value
            is_calc_q = "Discharge (Q) from" in ditch_mode_dd.value

            if is_calc_q and not d_y.value.strip(): raise ValueError("Normal Depth (y) field is empty.")
            if not is_calc_q and not d_q.value.strip(): raise ValueError("Discharge (Q) field is empty.")

            res = calculate_ditch_hydraulics(n, s, shape, b, z_left, z_right, is_calc_q, d_y.value, d_q.value)
            y_val = res['val'] if res["mode"] == "y" else float(d_y.value)
            v = res['velocity']
            
            if shape == "Triangular":
                top_width = (z_left + z_right) * y_val
                dm = res['area'] / top_width if top_width > 0 else (y_val / 2.0)
            else:
                top_width = b + (z_left + z_right) * y_val
                dm = res['area'] / top_width if top_width > 0 else 0.1

            flow_type = get_flow_type(v, dm)

            res_label = "Discharge (Q)" if res["mode"] == "Q" else "Normal Depth (y)"
            unit_label = "cfs" if res["mode"] == "Q" else "ft"

            d_result_txt.value = (
                f"Results — {res_label}: {res['val']:.2f} {unit_label} | "
                f"Flow Area: {res['area']:.2f} sq ft | Velocity: {res['velocity']:.2f} fps\n"
                f"Hydraulic Radius (R): {res['radius']:.2f} ft | Flow Type: {flow_type}"
            )
        except ValueError as ve: d_result_txt.value = f"Input Error: {str(ve)}"
        except Exception as ex: d_result_txt.value = f"Calculation Error: {str(ex)}"
        page.update()

    ditch_calc_btn = ft.Button("Run Ditch Analysis", icon=ft.Icons.CALCULATE, color=ft.Colors.WHITE, bgcolor=ft.Colors.INDIGO, on_click=on_run_ditch)

    tab_ditch_content = ft.Container(
        padding=15,
        content=ft.Column([
            ft.Text("Roadside & Open Channel Ditch Analysis (TxDOT Standard)", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([ditch_shape_dd, ditch_mode_dd], wrap=True),
            ft.Row([d_n, d_s, d_z_left, d_z_right], wrap=True),
            ft.Row([d_b, d_y, d_q], wrap=True),
            ft.Container(height=10),
            ditch_calc_btn,
            ft.Divider(),
            d_result_txt, d_equation_txt
        ], spacing=15, scroll=ft.ScrollMode.AUTO)
    )

    p_n = ft.TextField(label="Manning's Roughness (n)", value="0.012", width=220, text_size=13)
    p_s = ft.TextField(label="Bed Slope (S) [ft/ft]", value="0.005", width=220, text_size=13)
    pipe_sizes = [OptionClass(f'{i}"') for i in range(6, 66, 6)]
    p_dia = ft.Dropdown(label="Pipe Diameter (D) [inches]", options=pipe_sizes, value='24"', width=220, text_size=13)
    p_y = ft.TextField(label="Depth of Flow (y) [ft]", value="1.5", width=220, disabled=False, text_size=13)
    p_q = ft.TextField(label="Discharge (Q) [cfs]", value="20.0", width=220, disabled=True, text_size=13)

    def on_pipe_mode_change(e):
        is_calc_q = "Discharge (Q) from" in e.control.value
        p_y.disabled = not is_calc_q
        p_q.disabled = is_calc_q
        p_y.update()
        p_q.update()
        page.update()

    pipe_mode_dd = ft.Dropdown(label="Calculation Mode", options=[OptionClass("Calculate Discharge (Q) from Normal Depth (y)"), OptionClass("Calculate Normal Depth (y) from Discharge (Q)")], value="Calculate Discharge (Q) from Normal Depth (y)", width=420, text_size=13, on_select=on_pipe_mode_change)

    p_result_txt = ft.Text(value="Configure parameters above and click 'Run Pipe Analysis'.", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
    p_equation_txt = ft.Text(
        spans=[
            ft.TextSpan("Reference: TxDOT Hydraulic Design Manual (Eq. 6-2 & 6-3)", style=ft.TextStyle(color=ft.Colors.BLUE_600, decoration=ft.TextDecoration.UNDERLINE), url="https://www.txdot.gov/manuals/des/hyd/chapter-6--hydraulic-principles.html#_74b76647-1934-40bc-b514-d98ef3d10cde"),
            ft.TextSpan("\nManning's Eq: Q = (1.486 / n) * A * R^(2/3) * S^(1/2)")
        ], size=11, italic=True, color=ft.Colors.GREY_600
    )

    def on_run_pipe(e):
        try:
            if not p_n.value.strip(): raise ValueError("Manning's 'n' field is empty.")
            if not p_s.value.strip(): raise ValueError("Bed Slope 'S' field is empty.")

            n, s = float(p_n.value), float(p_s.value)
            dia_in = float(p_dia.value.replace('"', ''))
            is_calc_q = "Discharge (Q) from" in pipe_mode_dd.value

            if is_calc_q and not p_y.value.strip(): raise ValueError("Depth of Flow (y) field is empty.")
            if not is_calc_q and not p_q.value.strip(): raise ValueError("Discharge (Q) field is empty.")

            res = calculate_pipe_hydraulics(n, s, dia_in, is_calc_q, p_y.value, p_q.value)
            v = res['velocity']
            dm = res['area'] / (dia_in / 12.0) 
            flow_type = get_flow_type(v, dm)

            res_label = "Discharge (Q)" if res["mode"] == "Q" else "Depth of Flow (y)"
            unit_label = "cfs" if res["mode"] == "Q" else "ft"

            p_result_txt.value = (
                f"Results — {res_label}: {res['val']:.2f} {unit_label} | "
                f"Flow Area: {res['area']:.2f} sq ft | Velocity: {res['velocity']:.2f} fps\n"
                f"Hydraulic Radius (R): {res['radius']:.2f} ft | Flow Type: {flow_type}"
            )
        except ValueError as ve: p_result_txt.value = f"Input Error: {str(ve)}"
        except Exception as ex: p_result_txt.value = f"Calculation Error: {str(ex)}"
        page.update()

    pipe_calc_btn = ft.Button("Run Pipe Analysis", icon=ft.Icons.CALCULATE, color=ft.Colors.WHITE, bgcolor=ft.Colors.INDIGO, on_click=on_run_pipe)

    tab_pipe_content = ft.Container(
        padding=15,
        content=ft.Column([
            ft.Text("Circular Pipe Analysis (TxDOT Standard)", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            pipe_mode_dd,
            ft.Row([p_n, p_s, p_dia], wrap=True),
            ft.Row([p_y, p_q], wrap=True),
            ft.Container(height=10),
            pipe_calc_btn,
            ft.Divider(),
            p_result_txt, p_equation_txt
        ], spacing=15, scroll=ft.ScrollMode.AUTO)
    )

    pipes_ditches_calc_view = ft.Container(
        content=ft.Column([
            ft.Text("Pipes & Ditches Analysis", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Tabs(
                length=1,  # Update this integer to match your total number of tabs
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.TabBar(
                            tabs=[
                                ft.Tab(label="Open Channel Ditches"),
                                ft.Tab(label="Circular Pipes"),
                                # If you have additional tabs, add them here: ft.Tab(label="Tab Name")
                            ]
                        ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                tab_ditch_content,
                                # If you have additional tabs, place their content variables here in the exact same order
                            ]
                        )
                    ]
                )
            ),
           developer_footer()
        ], expand=True),
        padding=20, expand=True
    )

    # ==============================================================================
    # CALCULATOR 8: TXDOT MULTI-CURVE ALIGNMENT MODELER (ROADWAY)
    # ==============================================================================
    align_last_h_export_elements = []
    align_last_v_export_data = []

    # Global Inputs Dashboard for Alignment
    align_dd_speed = ft.Dropdown(
        label="Design Speed (mph)",
        options=[ft.dropdown.Option(str(s)) for s in [30, 45, 60, 70]],
        value="45", width=140
    )
    align_txt_start_sta = ft.TextField(label="Start Station", value="0+00", width=120)
    align_txt_start_north = ft.TextField(label="Start Northing (ft)", value="10000.0000", width=140)
    align_txt_start_east = ft.TextField(label="Start Easting (ft)", value="50000.0000", width=140)
    align_txt_start_bearing = ft.TextField(label="Initial Bearing / Azimuth", value="N 45°00'00\" E", width=170)
    align_txt_start_elev = ft.TextField(label="Start Elev (ft)", value="100.0000", width=120)
    align_txt_v_interval = ft.TextField(label="Vertical Interval (ft)", value="50", width=130)
    
    align_dashboard = ft.Container(
        content=ft.Row([
            align_dd_speed, align_txt_start_sta, align_txt_start_north, align_txt_start_east, 
            align_txt_start_bearing, align_txt_start_elev, align_txt_v_interval
        ], alignment=ft.MainAxisAlignment.START, wrap=True),
        padding=10, border=ft.Border.all(width=1, color="grey"), border_radius=8, margin=5
    )

    align_col_h_rows = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    align_col_v_rows = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    align_col_h_elements_output = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

    def align_reindex_horizontal():
        for i, row in enumerate(align_col_h_rows.controls):
            row.index = i + 1
            row.lbl_index.value = f"PI {row.index}"
        page.update()

    def align_reindex_vertical():
        for i, row in enumerate(align_col_v_rows.controls):
            row.index = i + 1
            row.lbl_index.value = f"PVI {row.index}"
        page.update()

    def align_delete_h_row(row_instance):
        align_col_h_rows.controls.remove(row_instance)
        align_reindex_horizontal()

    def align_delete_v_row(row_instance):
        align_col_v_rows.controls.remove(row_instance)
        align_reindex_vertical()

    def align_add_h_row(e=None):
        align_col_h_rows.controls.append(HorizontalPiRow(len(align_col_h_rows.controls) + 1, align_delete_h_row))
        if e: page.update()

    def align_add_v_row(e=None):
        align_col_v_rows.controls.append(VerticalPviRow(len(align_col_v_rows.controls) + 1, align_delete_v_row))
        if e: page.update()

    align_add_h_row()
    align_add_v_row()

    def align_render_horizontal_element_cards(elements):
        align_col_h_elements_output.controls.clear()
        if not elements:
            align_col_h_elements_output.controls.append(ft.Text("No element output available. Click 'Run Diagnostics' first.", italic=True, color="grey"))
            return

        for elem in elements:
            if elem["type"] == "Linear":
                card_content = ft.Column([
                    ft.Text(f"Element #{elem['element_index']} - LINEAR TANGENT", weight=ft.FontWeight.BOLD, color="blue"),
                    ft.Row([
                        ft.Text(f"Start Sta: {elem['start_sta']}"),
                        ft.Text(f"PC Sta: {elem['end_sta']}"),
                        ft.Text(f"PC Northing: {elem['pc_northing']}"),
                        ft.Text(f"PC Easting: {elem['pc_easting']}"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text(f"Tangential Bearing: {elem['bearing']}", weight=ft.FontWeight.W_500),
                        ft.Text(f"Tangent Length: {elem['length']} ft"),
                    ], alignment=ft.MainAxisAlignment.START, spacing=30)
                ])
            else: 
                card_content = ft.Column([
                    ft.Text(f"Element #{elem['element_index']} - CIRCULAR CURVE", weight=ft.FontWeight.BOLD, color="green"),
                    ft.Row([
                        ft.Text(f"PC: {elem['pc_sta']} (N: {elem['pc_northing']}, E: {elem['pc_easting']})"),
                        ft.Text(f"HPI: {elem['pi_sta']} (N: {elem['pi_northing']}, E: {elem['pi_easting']})"),
                        ft.Text(f"PT: {elem['pt_sta']} (N: {elem['pt_northing']}, E: {elem['pt_easting']})"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text(f"Radius: {elem['radius']} ft"),
                        ft.Text(f"Delta: {elem['delta']}"),
                        ft.Text(f"Turn Direction: {elem['turn']}"),
                        ft.Text(f"Curve Length: {elem['length']} ft"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text(f"Back Tangent Bearing: {elem['back_bearing']}"),
                        ft.Text(f"Ahead Tangent Bearing: {elem['ahead_bearing']}"),
                    ], alignment=ft.MainAxisAlignment.START, spacing=30)
                ])
            card = ft.Card(content=ft.Container(content=card_content, padding=12))
            align_col_h_elements_output.controls.append(card)

    def align_run_diagnostics(e):
        nonlocal align_last_h_export_elements, align_last_v_export_data
        try:
            speed = int(align_dd_speed.value)
            start_sta = align_txt_start_sta.value
            start_north = align_txt_start_north.value
            start_east = align_txt_start_east.value
            start_bearing = align_txt_start_bearing.value
            start_elev = align_txt_start_elev.value
            interval = align_txt_v_interval.value
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid Global Inputs! Check parameters."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
            
        h_data = []
        h_error = False
        for row in align_col_h_rows.controls:
            try:
                h_data.append({
                    'pi_sta': row.txt_pi_sta.value,
                    'delta': float(row.txt_delta.value),
                    'turn': row.dd_turn.value,
                    'input_type': row.dd_type.value,
                    'value': float(row.txt_value.value)
                })
            except ValueError:
                row.lbl_output.value = "ERROR: Missing or non-numeric inputs"
                row.lbl_output.color = "red"
                h_error = True
                
        if not h_error and h_data:
            h_results, align_last_h_export_elements = evaluate_horizontal_alignment(
                speed, start_sta, start_north, start_east, start_bearing, h_data
            )
            for row, res in zip(align_col_h_rows.controls, h_results):
                row.lbl_output.value = res["msg"]
                row.lbl_output.color = "green" if res["status"] == "PASS" else "red"
            align_render_horizontal_element_cards(align_last_h_export_elements)

        v_data = []
        v_error = False
        for row in align_col_v_rows.controls:
            try:
                l1 = float(row.txt_l1.value)
                l2 = float(row.txt_l2.value)
                v_data.append({
                    'sta': row.txt_sta.value,
                    'g1': float(row.txt_g1.value),
                    'g2': float(row.txt_g2.value),
                    'l1': l1,
                    'l2': l2,
                    'length': l1 + l2
                })
            except ValueError:
                row.lbl_output.value = "ERROR: Missing or non-numeric inputs"
                row.lbl_output.color = "red"
                v_error = True
                
        if not v_error and v_data:
            v_results, align_last_v_export_data = evaluate_vertical_alignment(
                speed, start_sta, start_elev, interval, v_data
            )
            for row, res in zip(align_col_v_rows.controls, v_results):
                l1 = float(row.txt_l1.value)
                l2 = float(row.txt_l2.value)
                g1 = float(row.txt_g1.value)
                g2 = float(row.txt_g2.value)
                tot_l = l1 + l2
                a_diff = abs(g2 - g1)
                k_val = (tot_l / a_diff) if a_diff > 0 else 0.0
                symmetry = "Symmetrical" if l1 == l2 else "Unsymmetrical"
                
                row.lbl_output.value = f"{res['msg']} | K = {k_val:.4f} ({symmetry}, L1={l1}, L2={l2})"
                row.lbl_output.color = "green" if res["status"] == "PASS" else "red"
                
        page.update()

    async def align_export_h_csv(e):
        if not align_last_h_export_elements:
            page.snack_bar = ft.SnackBar(ft.Text("Run Diagnostics first to generate horizontal export data!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            # 1. Create a virtual text file in memory
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["Element_Index", "Element_Type", "Start/PC_Sta", "PI_Sta", "PT_Sta", "PC_Northing", "PC_Easting", "PI_Northing", "PI_Easting", "PT_Northing", "PT_Easting", "Radius", "Delta", "Turn", "Back_Bearing", "Ahead_Bearing", "Length"])
            
            for elem in align_last_h_export_elements:
                if elem["type"] == "Linear":
                    writer.writerow([
                        elem["element_index"], "Linear", elem["start_sta"], "", elem["end_sta"],
                        elem["pc_northing"], elem["pc_easting"], "", "", "", "",
                        "", "", "", elem["bearing"], "", elem["length"]
                    ])
                else:
                    writer.writerow([
                        elem["element_index"], "Circular", elem["pc_sta"], elem["pi_sta"], elem["pt_sta"],
                        elem["pc_northing"], elem["pc_easting"], elem["pi_northing"], elem["pi_easting"], elem["pt_northing"], elem["pt_easting"],
                        elem["radius"], elem["delta"], elem["turn"], elem["back_bearing"], elem["ahead_bearing"], elem["length"]
                    ])
            
            # 2. Convert the virtual text file into raw bytes
            csv_bytes = buffer.getvalue().encode('utf-8')

            # 3. Hand the bytes to Flet. Flet will automatically download it on the web, 
            # or save it to the user's chosen folder on desktop.
            await ft.FilePicker().save_file(
                file_name="horizontal_alignment_elements.csv", 
                allowed_extensions=["csv"],
                src_bytes=csv_bytes
            )

            page.snack_bar = ft.SnackBar(ft.Text("Horizontal elements exported successfully!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Export Error: {str(ex)}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()


    async def align_export_v_csv(e):
        if not align_last_v_export_data:
            page.snack_bar = ft.SnackBar(ft.Text("Run Diagnostics first to generate vertical export data!"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return
            
        try:
            # 1. Create a virtual text file in memory
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=["Station", "Elevation", "Point_Type"])
            writer.writeheader()
            
            for row in align_last_v_export_data:
                writer.writerow({
                    "Station": row.get("Station"),
                    "Elevation": row.get("Elevation"),
                    "Point_Type": row.get("Point_Type")
                })
            
            # 2. Convert the virtual text file into raw bytes
            csv_bytes = buffer.getvalue().encode('utf-8')

            # 3. Hand the bytes to Flet.
            await ft.FilePicker().save_file(
                file_name="vertical_profile_report.csv", 
                allowed_extensions=["csv"],
                src_bytes=csv_bytes
            )

            page.snack_bar = ft.SnackBar(ft.Text("Vertical profile CSV exported successfully!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Export Error: {str(ex)}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    align_btn_add_h = ft.Button(content=ft.Text("Add Horizontal PI"), on_click=align_add_h_row)
    align_btn_add_v = ft.Button(content=ft.Text("Add Vertical PVI"), on_click=align_add_v_row)
    align_btn_export_h = ft.Button(content=ft.Text("Export Horizontal CSV"), on_click=align_export_h_csv, color="green")
    align_btn_export_v = ft.Button(content=ft.Text("Export Vertical CSV"), on_click=align_export_v_csv, color="green")
    
    align_tabs = ft.Tabs(
        length=2, selected_index=0, animation_duration=300, expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(tabs=[ft.Tab(label="Horizontal Alignment"), ft.Tab(label="Vertical Profile")]),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                ft.Row([align_btn_add_h, align_btn_export_h], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Divider(), 
                                ft.Text("Horizontal PIs Input:", weight=ft.FontWeight.BOLD),
                                ft.Container(content=align_col_h_rows, height=180),
                                ft.Divider(),
                                ft.Text("Horizontal Output (Element-Based Format):", weight=ft.FontWeight.BOLD),
                                align_col_h_elements_output
                            ], expand=True), padding=15
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([align_btn_add_v, align_btn_export_v], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Divider(), 
                                align_col_v_rows
                            ], expand=True), padding=15
                        ),
                    ]
                )
            ]
        )
    )
    
    align_txdot_link = ft.TextButton(
        content=ft.Text("TxDOT Roadway Design Manual: K-Values Reference", style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE), size=13),
        url="https://www.txdot.gov/manuals/des/rdw/chapter-4--basic-design-criteria/4-8-vertical-alignment.html",
    )
    
    align_btn_run = ft.Button(
        content=ft.Text("Run Diagnostics & Compute Outputs"),
        on_click=align_run_diagnostics, bgcolor="blue", color="white", width=300
    )

    align_footnote = ft.Text(
        "Legend: GREEN text = PASS (Geometry closes, no station overlaps, and meets TxDOT min K-values for selected Design Speed) | "
        "RED text = FAIL (Station overlaps, negative lengths, math exceptions, or fails TxDOT minimum criteria)", 
        size=13, color="grey"
    )

    alignment_calc_view = ft.Container(
        content=ft.Column([
            ft.Text("TxDOT Multi-Curve Alignment Modeler", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            align_dashboard,
            ft.Container(content=align_tabs, expand=True, border=ft.Border.all(width=1, color="grey"), border_radius=8),
            ft.Row([align_txdot_link, align_btn_run], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            align_footnote,
            developer_footer()
        ], expand=True),
        padding=20, expand=True
    )

    # ==========================================
    # CALCULATOR 8: TXDOT DRAINAGE STANDARDS VIEWER
    # ==========================================
    standards_map = {
        f"[{item.get('code', 'N/A')}] {item.get('title', 'Untitled')}": item 
        for item in TXDOT_DRAINAGE_STANDARDS
    }

    default_key = list(standards_map.keys())[0] if standards_map else None
    default_item = standards_map.get(default_key, {}) if default_key else {}

    code_title_text = ft.Text(
        f"[{default_item.get('code', 'N/A')}] {default_item.get('title', '')}" if default_key else "Select a standard to view details.", 
        size=16, 
        weight=ft.FontWeight.BOLD
    )
    category_text = ft.Text(f"Category: {default_item.get('category', '-')}", weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_700)
    constraints_text = ft.Text(f"Constraints: {default_item.get('constraints', '-')}", italic=True, size=13)
    dgn_file_text = ft.Text(f"DGN Reference: {default_item.get('file_name', '-')}", size=12, color=ft.Colors.GREY_700)
    summary_text = ft.Text(default_item.get('summary', ''), size=13, selectable=True)
    status_text = ft.Text(f"Loaded details for {default_item.get('code', '')}" if default_key else "", size=12, italic=True)

    open_pdf_btn = ft.Button(
        content=ft.Row([ft.Icon(ft.Icons.PICTURE_AS_PDF), ft.Text("Open Standard PDF")], alignment=ft.MainAxisAlignment.CENTER),
        disabled=not bool(default_key),
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        data=default_item.get('url', '')
    )

    def update_standard_details(e=None):
        selected_key = standard_dropdown.value
        
        if selected_key and selected_key in standards_map:
            item = standards_map[selected_key]
            code_title_text.value = f"[{item.get('code', 'N/A')}] {item.get('title', '')}"
            category_text.value = f"Category: {item.get('category', 'N/A')}"
            constraints_text.value = f"Constraints: {item.get('constraints', 'N/A')}"
            dgn_file_text.value = f"DGN Reference: {item.get('file_name', 'N/A')}"
            summary_text.value = item.get('summary', 'No summary available.')

            open_pdf_btn.disabled = False
            open_pdf_btn.data = item.get('url', '')
            status_text.value = f"Loaded details for {item.get('code', '')}"
            status_text.color = ft.Colors.BLACK
        else:
            code_title_text.value = "Select a standard to view details."
            category_text.value = "Category: -"
            constraints_text.value = "Constraints: -"
            dgn_file_text.value = "DGN Reference: -"
            summary_text.value = ""
            open_pdf_btn.disabled = True
            open_pdf_btn.data = None

        code_title_text.update()
        category_text.update()
        constraints_text.update()
        dgn_file_text.update()
        summary_text.update()
        open_pdf_btn.update()
        status_text.update()

    standard_dropdown = ft.Dropdown(
        label="Select Standard Drawing",
        width=360,
        options=[ft.dropdown.Option(k) for k in standards_map.keys()],
        value=default_key,
        on_select=update_standard_details
    )

    def filter_standards(e):
        query = search_box.value.lower().strip()
        filtered_options = []
        
        for key, item in standards_map.items():
            code = str(item.get("code", "")).lower()
            title = str(item.get("title", "")).lower()
            category = str(item.get("category", "")).lower()

            if not query or query in code or query in title or query in category:
                filtered_options.append(ft.dropdown.Option(key))
                
        standard_dropdown.options = filtered_options
        
        if filtered_options:
            standard_dropdown.value = filtered_options[0].key
        else:
            standard_dropdown.value = None

        standard_dropdown.update()
        update_standard_details()

        status_text.value = f"Filtered {len(filtered_options)} matching standards."
        status_text.color = ft.Colors.GREY_700
        status_text.update()

    search_box = ft.TextField(
        label="Search Standards",
        hint_text="Type code, title, or category...",
        prefix_icon=ft.Icons.SEARCH,
        width=360,
        on_change=filter_standards
    )

    def on_open_pdf_clicked(e):
        pdf_path = e.control.data
        if pdf_path:
            success, msg = open_pdf_in_system_viewer(pdf_path, e.page)
            status_text.value = msg
            status_text.color = ft.Colors.GREEN_700 if success else ft.Colors.RED_700
            status_text.update()

    open_pdf_btn.on_click = on_open_pdf_clicked

    txdot_left_panel = ft.Column(
        controls=[
            ft.Text("TxDOT Standards Index", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            search_box,
            standard_dropdown,
        ],
        width=360,
        spacing=12
    )

    txdot_right_panel = ft.Card(
        elevation=2,
        content=ft.Container(
            padding=20,
            width=620,
            content=ft.Column(
                controls=[
                    ft.Row([
                        ft.Icon(ft.Icons.MENU_BOOK, color=ft.Colors.BLUE_600),
                        ft.Text("Standard Details", size=18, weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Divider(),
                    code_title_text,
                    category_text,
                    constraints_text,
                    dgn_file_text,
                    ft.Divider(),
                    ft.Text("Summary:", weight=ft.FontWeight.BOLD, size=15),
                    ft.Container(
                        content=ft.Column([summary_text], scroll=ft.ScrollMode.AUTO),
                        height=260,
                        padding=5,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=6,
                    ),
                    ft.Divider(),
                    open_pdf_btn,
                    status_text
                ],
                spacing=8
            )
        )
    )

    txdot_calc_view = ft.Container(
        content=ft.Column([
            ft.Row(
                controls=[txdot_left_panel, ft.VerticalDivider(width=20), txdot_right_panel],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            ),
            developer_footer()
        ], expand=True, scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    )

    # ==========================================
    # NAVIGATION & LAYOUT
    # ==========================================
    content_area = ft.Container(content=slope_calc_view, expand=True)
    views = [
        slope_calc_view,
        middle_calc_view,
        tc_calc_view,
        drainage_area_calc_view,
        rational_calc_view,
        scs_calc_view,
        pipes_ditches_calc_view,
        alignment_calc_view,
        txdot_calc_view,
    ]

    def nav_change(e):
        content_area.content = views[e.control.selected_index]
        page.update()

    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=180,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.ANALYTICS, label="Standard Slope"),
            ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_TREE, label="Middle Elev"),
            ft.NavigationRailDestination(icon=ft.Icons.ACCESS_TIME, label="Time of Concentration"),
            ft.NavigationRailDestination(icon=ft.Icons.SQUARE_FOOT, label="Drainage Area"),
            ft.NavigationRailDestination(icon=ft.Icons.WATER, label="Rational Q"),
            ft.NavigationRailDestination(icon=ft.Icons.LANDSCAPE, label="SCS Qp"),
            ft.NavigationRailDestination(icon=ft.Icons.WATERFALL_CHART, label="Pipes & Ditches"),
            ft.NavigationRailDestination(icon=ft.Icons.ADD_ROAD, label="Alignment"),
            ft.NavigationRailDestination(icon=ft.Icons.MENU_BOOK, label="TxDOT Standards"),
        ],
        on_change=nav_change,
    )

    page.add(
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1),
            content_area
        ], expand=True)
    )
if __name__ == "__main__":
    ft.run(main)