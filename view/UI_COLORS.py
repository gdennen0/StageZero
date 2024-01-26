from PyQt5.QtWidgets import QWidget


class UIColors:
    # Define color constants for UI elements
    BACKGROUND_COLOR = "#121212"  # Black color code for background
    TEXT_COLOR = "#FFFFFF"
    BUTTON_COLOR = "#404040"
    BUTTON_TEXT_COLOR = "#FFFFFF"
    WIDGET_COLOR = "#00000000"
    DROPDOWN_COLOR = "#404040"
    DROPDOWN_TEXT_COLOR = "#FFFFFF"
    LIST_COLOR = "#282828"
    LIST_TEXT_COLOR = "#FFFFFF"
    LIST_BORDER_COLOR = "#282828"
    INPUT_BOX_COLOR = "#404040"
    INPUT_BOX_TEXT_COLOR = "#FFFFFF"
    INPUT_BOX_BORDER_COLOR = "#404040"

    @staticmethod
    def initialize_ui_colors(ui_elements):
        for element, properties in ui_elements.items():
            if not isinstance(element, QWidget):
                continue  # Skip non-widget elements like layouts

            styles = []
            for property, value in properties.items():
                if property == "background":
                    styles.append(f"background-color: {UIColors.BACKGROUND_COLOR};")
                elif property == "text":
                    styles.append(f"color: {UIColors.TEXT_COLOR};")
                elif property == "button":
                    styles.append(f"background-color: {UIColors.BUTTON_COLOR};")
                    styles.append(f"color: {UIColors.BUTTON_TEXT_COLOR};")
                elif property == "widget":
                    styles.append(f"background-color: {UIColors.WIDGET_COLOR};")
                elif property == "dropdown":
                    styles.append(f"background-color: {UIColors.DROPDOWN_COLOR};")
                    styles.append(f"color: {UIColors.DROPDOWN_TEXT_COLOR};")
                elif property == "list":
                    styles.append(f"background-color: {UIColors.LIST_COLOR};")
                    styles.append(f"color: {UIColors.LIST_TEXT_COLOR};")
                    styles.append(f"border-top-color: {UIColors.LIST_BORDER_COLOR};")
                    styles.append(f"border-bottom-color: {UIColors.LIST_BORDER_COLOR};")
                    styles.append(f"border: 1px solid {UIColors.LIST_BORDER_COLOR};")
                elif property == "inputbox":
                    styles.append(f"background-color: {UIColors.INPUT_BOX_COLOR};")
                    styles.append(f"color: {UIColors.INPUT_BOX_TEXT_COLOR};")
                    styles.append(
                        f"border: 1px solid {UIColors.INPUT_BOX_BORDER_COLOR};"
                    )

            element.setStyleSheet(" ".join(styles))
