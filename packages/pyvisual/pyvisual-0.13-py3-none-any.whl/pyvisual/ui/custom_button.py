import os
from kivy.core.window import Window as KivyWindow
from kivy.uix.label import Label
from pyvisual.ui.image import Image


class CustomButton(Image):
    def __init__(self, window, x, y, idle_image=None, hover_image=None, clicked_image=None, scale=1.0,
                 text=None, text_anchor='center', text_color=(1, 1, 1, 1), font="Roboto", text_size=14,
                 on_hover=None, on_click=None, on_release=None, name=None):

        # Get the base path to the assets folder by moving up two directory levels and then navigating to assets/buttons/sample/
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_image_folder = os.path.join(base_path, "assets", "buttons", "sample")
        self.name = name  # Set the hidden access text for buttons without visible labels

        # Use default images if not provided
        self.idle_image_path = idle_image or os.path.join(default_image_folder, "idle.png")
        self.hover_image_path = hover_image or os.path.join(default_image_folder, "hover.png")
        self.clicked_image_path = clicked_image or os.path.join(default_image_folder, "clicked.png")

        # Store callback functions
        self.on_click = on_click
        self.on_release = on_release
        self.on_hover = on_hover

        # Initialize the button with the idle image (and add it to the window automatically)
        super().__init__(window, x, y, image_path=self.idle_image_path, scale=scale)

        # Monitor mouse position to simulate hover
        KivyWindow.bind(mouse_pos=self.on_mouse_pos)

        # Add text if provided
        self.text = text
        self.text_anchor = text_anchor
        self.text_color = text_color
        self.text_font = text_font
        self.text_size = text_size

        if self.text:
            self.add_text(window)

    def add_text(self, window):
        """Create and add a text label centered on top of the button image."""
        # Create a Kivy Label widget
        self.label = Label(
            text=self.text,
            color=self.text_color,  # Set text color
            font_name=self.text_font,
            font_size=self.text_size,
            size_hint=(None, None),  # Disable size hint
            halign='center',
            valign='middle'
        )

        # Update the text size and position
        self.label.bind(texture_size=self._update_text_position)

        # Set the position and size of the label based on the button
        self._update_text_position()

        # Add the label to the window
        window.add_widget(self.label)

    def set_text_color(self, color):
        """Set the text color of the label."""
        self.text_color = color
        if hasattr(self, 'label'):
            self.label.color = color

    def set_text_size(self, font_size):
        """Set the text size of the label."""
        self.text_size = font_size
        if hasattr(self, 'label'):
            self.label.font_size = font_size

    def set_text_font(self, font_name):
        """Set the text font of the label."""
        self.text_font = font_name
        if hasattr(self, 'label'):
            self.label.font_name = font_name

    def _update_text_position(self, *args):
        """Update the text position to ensure it is centered over the image."""
        # Calculate the center position of the image and set the label position
        self.label.size = self.label.texture_size  # Set size to the texture size for proper positioning
        self.label.pos = (
            self.x + (self.width - self.label.texture_size[0]) / 2,
            self.y + (self.height - self.label.texture_size[1]) / 2
        )

    def on_mouse_pos(self, window, pos):
        """Detect hover by checking if the mouse is within the button area and switch to hover image."""
        if self.is_hovered(pos):
            self.source = self.hover_image_path
            if self.on_hover:
                self.on_hover(self)
        else:
            self.source = self.idle_image_path

    def on_touch_down(self, touch):
        """Handle mouse click by switching to clicked image and invoking the callback."""
        if self.is_hovered(touch.pos):
            self.source = self.clicked_image_path
            if self.on_click:
                self.on_click(self)
            return True  # Indicate that the touch was handled
        return False

    def on_touch_up(self, touch):
        """Handle mouse release by switching back to hover or idle state and invoking the callback."""
        if self.is_hovered(touch.pos):
            self.source = self.hover_image_path
            if self.on_release:
                self.on_release(self)
            return True  # Indicate that the touch was handled
        else:
            self.source = self.idle_image_path
        return False

    def is_hovered(self, pos):
        """Check if the mouse is within the button's boundaries."""
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

    def destroy(self):
        # Check if the widget is still part of the window
        if self.window and self in self.window.children:
            self.window.remove_widget(self)


if __name__ == "__main__":
    import pyvisual as pv

    window = pv.Window()

    # Create a ButtonImage with text and callbacks
    button = CustomButton(
        window=window,
        x=280, y=270,  # Adjusted position for better visibility
        idle_image="../assets/buttons/blue_round/idle.png",
        hover_image="../assets/buttons/blue_round/hover.png",
        clicked_image="../assets/buttons/blue_round/clicked.png",
        scale=0.6,
        text="CLICK ME",
        text_anchor='center',
        text_color=(1, 1, 1, 1),  # Set text color to black
        text_font="Roboto",
        text_size=18,
        on_click=lambda instance: print("Button clicked!"),
        on_release=lambda instance: print("Button released!"),
        on_hover=lambda instance: print("Button hovered!")
    )

    # # Change text properties dynamically
    # button.set_text_color((1, 0, 0, 1))  # Change text color to red
    # button.set_text_size(24)  # Change text size to 24
    # button.set_text_font("Arial")  # Change text font to Arial

    window.show()
