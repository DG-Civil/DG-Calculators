import flet as ft

def main(page: ft.Page):
    page.title = "Engineering Calculator Suite"
    page.window_width = 750
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

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

            ans = 0.0
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

    s_var_row_1 = ft.Row([
        ft.ElevatedButton("Slope (%)", on_click=make_var_handler("Slope (%)"), expand=1, color="#1976D2"),
        ft.ElevatedButton("Upstream Elev", on_click=make_var_handler("Upstream Elev"), expand=1, color="#1976D2"),
    ])
    s_var_row_2 = ft.Row([
        ft.ElevatedButton("Downstream Elev", on_click=make_var_handler("Downstream Elev"), expand=1, color="#1976D2"),
        ft.ElevatedButton("Length", on_click=make_var_handler("Length"), expand=1, color="#1976D2"),
    ])

    def btn(text, on_click, color=None, text_color=None, expand=1):
        return ft.ElevatedButton(text, on_click=on_click, expand=expand, bgcolor=color, color=text_color, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

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
            s_var_row_1,
            s_var_row_2,
            ft.Divider(height=10),
            ft.Text("2. Enter Values:", weight="bold", size=14),
            s_numpad
        ]),
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
            if total_length == 0:
                raise ZeroDivisionError

            total_drop = top_elev - bot_elev
            drop_per_unit = total_drop / total_length
            middle_elev = top_elev - (drop_per_unit * top_len)
            slope_percent = (drop_per_unit) * 100

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
            ft.Container(
                content=ft.Column([
                    m_main_display, 
                    m_extra_display,
                    m_sub_display
                ], spacing=4), 
                padding=15, 
                bgcolor="#ECEFF1", 
                border_radius=8, 
                width=float("inf")
            ),
            ft.Divider(height=15, color="transparent"),
            ft.Text("Sequential Input Mode:", weight="bold", size=14),
            ft.Text("Provide parameters in order: Top Elev -> Top Len -> Bot Len -> Bot Elev", size=12, color="#78909C"),
            ft.Divider(height=10),
            ft.Column([
                ft.Row([btn("7", make_m_num_handler("7")), btn("8", make_m_num_handler("8")), btn("9", make_m_num_handler("9")), btn("C", m_clear_click, "#FFCDD2", "#B71C1C")]),
                ft.Row([btn("4", make_m_num_handler("4")), btn("5", make_m_num_handler("5")), btn("6", make_m_num_handler("6")), btn("Enter", m_enter_click, "#C8E6C9", "#1B5E20")]),
                ft.Row([btn("1", make_m_num_handler("1")), btn("2", make_m_num_handler("2")), btn("3", make_m_num_handler("3")), btn("(-)", make_m_num_handler("(-)"))]), 
                ft.Row([btn("0", make_m_num_handler("0"), expand=2), btn(".", make_m_num_handler(".")), ft.Container(expand=1)]),
            ], spacing=8)
        ]),
        padding=20,
        expand=True
    )


    # ==========================================
    # NAVIGATION & LAYOUT
    # ==========================================
    content_area = ft.Container(content=slope_calc_view, expand=True)

    def nav_change(e):
        index = e.control.selected_index
        if index == 0:
            content_area.content = slope_calc_view
        else:
            content_area.content = middle_calc_view
        page.update()

    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=180,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.ANALYTICS,
                selected_icon=ft.Icons.ANALYTICS,
                label="Standard Slope",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ACCOUNT_TREE,
                selected_icon=ft.Icons.ACCOUNT_TREE,
                label="Middle Elev",
            ),
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

ft.app(target=main)