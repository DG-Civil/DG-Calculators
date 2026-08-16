import os
import platform
import subprocess
import webbrowser
import flet as ft

# -------------------------------------------------------------------------
# DATABASE IMPORT
# -------------------------------------------------------------------------
try:
    from drainage_standards_data import TXDOT_DRAINAGE_STANDARDS
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

# -------------------------------------------------------------------------
# PDF HANDLING STRATEGY
# -------------------------------------------------------------------------
def open_pdf_in_system_viewer(path: str):
    if not path:
        return False, "No valid path provided."

    try:
        if path.startswith("http://") or path.startswith("https://"):
            webbrowser.open(path, new=2)
            return True, "Opening standard PDF in default browser..."

        if not os.path.exists(path):
            return False, f"File not found: {path}"

        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", path], check=True)
        return True, f"Opened '{os.path.basename(path)}' in default viewer."
    except Exception as err:
        return False, f"Error opening PDF: {str(err)}"

# -------------------------------------------------------------------------
# UI LAYOUT
# -------------------------------------------------------------------------
def main(page: ft.Page):
    page.title = "TxDOT Drainage Standards Viewer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 860
    page.window_height = 680
    page.padding = 20

    # Build primary dictionary lookup matching schema
    standards_map = {
        f"[{item.get('code', 'N/A')}] {item.get('title', 'Untitled')}": item 
        for item in TXDOT_DRAINAGE_STANDARDS
    }

    default_key = list(standards_map.keys())[0] if standards_map else None

    # --- Details Panel Controls ---
    code_title_text = ft.Text("Select a standard to view details.", size=16, weight=ft.FontWeight.BOLD)
    category_text = ft.Text("Category: -", weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_700)
    constraints_text = ft.Text("Constraints: -", italic=True, size=13)
    dgn_file_text = ft.Text("DGN Reference: -", size=12, color=ft.Colors.GREY_700)
    summary_text = ft.Text("", size=13, selectable=True)
    status_text = ft.Text("", size=12, italic=True)

    open_pdf_btn = ft.ElevatedButton(
        content=ft.Text("Open Standard PDF"),
        icon=ft.Icons.PICTURE_AS_PDF,
        disabled=True,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700
    )

    # --- Dynamic Update Handler ---
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

    # --- Dropdown and Search Controls ---
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
            success, msg = open_pdf_in_system_viewer(pdf_path)
            status_text.value = msg
            status_text.color = ft.Colors.GREEN_700 if success else ft.Colors.RED_700
            status_text.update()

    open_pdf_btn.on_click = on_open_pdf_clicked

    # --- Layout Assembly ---
    left_panel = ft.Column(
        controls=[
            ft.Text("TxDOT Standards Index", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            search_box,
            standard_dropdown,
        ],
        width=380,
        spacing=12
    )

    right_panel = ft.Card(
        elevation=2,
        content=ft.Container(
            padding=20,
            width=420,
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
                    ft.Text("Summary:", weight=ft.FontWeight.BOLD, size=13),
                    ft.Container(
                        content=ft.Column([summary_text], scroll=ft.ScrollMode.AUTO),
                        height=130,
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

    main_layout = ft.Row(
        controls=[left_panel, ft.VerticalDivider(width=20), right_panel],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    page.add(main_layout)
    update_standard_details()

if __name__ == "__main__":
    ft.run(main)