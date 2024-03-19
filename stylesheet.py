BACKGROUND_COLOR = "#121212"
BLACK = "#000000"
TEXT_COLOR = "#FFFFFF"
BUTTON_COLOR = "#404040"
BUTTON_TEXT_COLOR = "#FFFFFF"
WIDGET_COLOR = "#121212"
DROPDOWN_COLOR = "#404040"
DROPDOWN_TEXT_COLOR = "#FFFFFF"
LIST_COLOR = "#282828"
LIST_TEXT_COLOR = "#FFFFFF"
LIST_BORDER_COLOR = "#282828"
INPUT_BOX_COLOR = "#404040"
INPUT_BOX_TEXT_COLOR = "#FFFFFF"
INPUT_BOX_BORDER_COLOR = "#404040"
LAYER_BACKGROUND = "#000000"
LAYER_COLOR = "#000000"
MENU_BAR_COLOR = "#404040"
MENU_BAR_TEXT_COLOR = "#FFFFFF"
MENU_BAR_ITEM_COLOR = "#404040"
MENU_BAR_ITEM_TEXT_COLOR = "#404040"
MENU_BAR_ITEM_SELECTED_COLOR = "#282828"
MENU_BAR_ITEM_PRESSED_COLOR = "#282828"
MENU_BAR_ITEM_HOVER_COLOR = "#282828"
TOOL_TIP_BACKGROUND_COLOR = "#404040"
TOOL_TIP_TEXT_COLOR = "#FFFFFF"
TOOL_TIP_BORDER_COLOR = "#000000"

widget_stylesheet = f"""
    QWidget {{
        background-color: {WIDGET_COLOR};
        color: {TEXT_COLOR};
    }}
"""

push_button_stylesheet = f"""
    QPushButton {{
        background-color: {BUTTON_COLOR};
        color: {BUTTON_TEXT_COLOR};
        border: 1px solid {INPUT_BOX_BORDER_COLOR};
        border-radius: 1px;
        padding: 3px;
        font: normal 11px;
        min-width: 6em;
    }}
"""

label_stylesheet = f"""
    QLabel {{
        color: {TEXT_COLOR};
    }}
"""

menu_bar_stylesheet = f"""
    QMenuBar {{
        background-color: {MENU_BAR_COLOR};
        color: {MENU_BAR_TEXT_COLOR};
    }}

    QMenuBar::item {{
        background-color: {MENU_BAR_ITEM_COLOR};
        color: {MENU_BAR_ITEM_TEXT_COLOR};
    }}

    QMenuBar::item:selected {{
        background-color: {MENU_BAR_ITEM_SELECTED_COLOR};
    }}

    QMenuBar::item:pressed {{
        background-color: {MENU_BAR_ITEM_PRESSED_COLOR};
    }}

    QMenuBar::item:hover {{
        background-color: {MENU_BAR_ITEM_HOVER_COLOR};
    }}
"""

tool_tip_stylesheet = f"""
    QToolTip {{
        background-color: {TOOL_TIP_BACKGROUND_COLOR};
        color: {TOOL_TIP_TEXT_COLOR};
        border: 1px solid {TOOL_TIP_BORDER_COLOR};
    }}
"""

combo_box_stylesheet = f"""
    QComboBox {{
        background-color: {DROPDOWN_COLOR};
        color: {DROPDOWN_TEXT_COLOR};
        border: 1px solid {INPUT_BOX_BORDER_COLOR};
        border-radius: 1px;
        padding: 2px 8px;
        font: normal 11px;
        min-width: 6em;
    }}
"""

line_edit_stylesheet = f"""
    QLineEdit {{
        background-color: {INPUT_BOX_COLOR};
        color: {INPUT_BOX_TEXT_COLOR};
    }}
"""

global_stylesheet = widget_stylesheet + push_button_stylesheet + label_stylesheet + menu_bar_stylesheet + tool_tip_stylesheet + combo_box_stylesheet + line_edit_stylesheet

