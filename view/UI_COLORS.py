from PyQt5.QtWidgets import QWidget

class UIColors:
    # Define color constants for UI elements
    BACKGROUND_COLOR = "#121212"  # Black color code for background
    TEXT_COLOR = "#FFFFFF"        # Black color code for text
    BUTTON_COLOR = "#404040"      # Black color code for buttons
    WIDGET_COLOR = "#000000"      # Black color code for widgets
    DROPDOWN_COLOR = "#282828"
    
    @staticmethod
    def initialize_ui_colors(ui_elements):
        for element, properties in ui_elements.items():
            if not isinstance(element, QWidget):
                continue  # Skip non-widget elements like layouts

            styles = []
            for property, value in properties.items():
                if property == 'background':
                    print(f"applying background color style")
                    styles.append(f"background-color: {UIColors.BACKGROUND_COLOR};")
                elif property == 'text':
                    print(f"applying text color style")
                    styles.append(f"color: {UIColors.TEXT_COLOR};")
                elif property == 'button':
                    print(f"applying button color style")
                    styles.append(f"background-color: {UIColors.BUTTON_COLOR};")
                elif property == 'widget':
                    print(f"applying widget color style")
                    styles.append(f"background-color: {UIColors.WIDGET_COLOR};")
                elif property == 'dropdown':
                    print(f"applying dropdown color style")
                    styles.append(f"background-color: {UIColors.DROPDOWN_COLOR};")
                # Add more properties if needed
            element.setStyleSheet(' '.join(styles))