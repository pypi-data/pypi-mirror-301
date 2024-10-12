from kivy.uix.button import Button as KivyButton
from kivy.graphics import Line, Color
from kivy.core.window import Window as KivyWindow
from kivy.core.text import LabelBase


class BasicButton:
    _window_bound = False  # Track if the window mouse binding is set up

    def __init__(self, window, x, y, width=140, height=50, text="CLICK ME",
                 font="Roboto", font_size=16, font_color="#FFFFFF",
                 idle_color="#f9b732", hover_color="#ffd278", clicked_color="#d1910f",
                 border_color=(0, 0, 0, 0), border_thickness=0,
                 on_hover=None, on_click=None, on_release=None, name=None,
                 force_bind=False):  # New parameter to force window binding
        # Initialize button properties
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.idle_color = (idle_color)  # Convert to RGBA
        self.hover_color = (hover_color)  # Convert to RGBA
        self.clicked_color = (clicked_color)  # Convert to RGBA
        self.font_color = (font_color)  # Convert to RGBA
        self.border_color = (border_color)  # Ensure color is RGBA
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.on_click = on_click
        self.on_release = on_release
        self.on_hover = on_hover  # Store the hover callback function
        self.name = name
        self.is_pressed = False  # Track if the button is pressed

        # Register font if a file path is provided
        if font.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font)
            self.font_name = "CustomFont"
        else:
            self.font_name = font

        # Create a Kivy button widget
        self.button_widget = KivyButton(
            text=self.text,
            size=(self.width, self.height),
            pos=(self.x, self.y),  # Positioning will work with FloatLayout
            background_normal='',  # Disable default Kivy background
            background_down='',  # Disable default Kivy down state
            background_color=self.idle_color,
            color=self.font_color,
            font_name=self.font_name,
            font_size=self.font_size,
            size_hint=(None, None)  # Disable size_hint to manually set size
        )

        # Draw the custom border
        self.draw_border()

        # Bind events for click, release, and hover callbacks
        self.button_widget.bind(on_press=self.handle_click)  # Use internal click handler
        self.button_widget.bind(on_release=self.handle_release)  # Always bind release for safety

        # Ensure window mouse binding is done as needed
        if force_bind or not BasicButton._window_bound:
            KivyWindow.bind(mouse_pos=self.on_mouse_pos)
            BasicButton._window_bound = True

        # Add the button to the window
        window.add_widget(self.button_widget)

    def draw_border(self):
        """Draw a custom border around the button."""
        with self.button_widget.canvas.before:
            Color(*self.border_color)  # Set the border color
            Line(
                rectangle=(
                self.button_widget.x, self.button_widget.y, self.button_widget.width, self.button_widget.height),
                width=self.border_thickness
            )

    def handle_click(self, instance):
        """Handle the button click event and change the color to clicked state."""
        self.is_pressed = True
        self.update_button_color(self.clicked_color)
        if self.on_click:
            self.on_click(self)  # Invoke the click callback

    def handle_release(self, instance):
        """Handle the button release event and revert color based on mouse position."""
        self.is_pressed = False
        if self.on_release:
            self.on_release(self)  # Invoke the release callback
        self.on_mouse_pos(None, KivyWindow.mouse_pos)  # Re-check hover state

    def on_mouse_pos(self, window, pos):
        """Detect hover by checking if the mouse is within the button area."""
        if self.is_mouse_hovering(pos):
            if self.is_pressed:
                self.update_button_color(self.clicked_color)
            else:
                self.update_button_color(self.hover_color)
            if self.on_hover:
                self.on_hover(self)  # Invoke the hover callback
        else:
            self.update_button_color(self.idle_color)

    def update_button_color(self, color):
        """Update the button's background color."""
        self.button_widget.background_color = color

    def is_mouse_hovering(self, pos):
        """Check if the mouse is within the button's boundaries."""
        return (self.button_widget.x <= pos[0] <= self.button_widget.x + self.button_widget.width and
                self.button_widget.y <= pos[1] <= self.button_widget.y + self.button_widget.height)


if __name__ == "__main__":
    import pyvisual as pv

    window = pv.Window()
    # Create a button with hover, click, and release callbacks
    button = BasicButton(
        window=window,
        x=325, y=275,
        width=150, height=50,
        text="Click Me!",
    )

    window.show()
