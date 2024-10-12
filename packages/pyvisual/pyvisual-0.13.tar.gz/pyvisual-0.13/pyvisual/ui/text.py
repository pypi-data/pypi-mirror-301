from kivy.uix.label import Label
from kivy.core.text import LabelBase


class Text(Label):
    def __init__(self, window, x, y, text="Hello",
                 font=None, font_size=20, font_color=(0.3, 0.3, 0.3, 1),
                 bold=False, italic=False, underline=False, strikethrough=False):
        # Initialize the main text label with basic properties
        super().__init__(
            size_hint=(None, None),  # Disable size hint
            halign='left',
            valign='top',
            text_size=(None, None),
        )

        # Store initial position
        self.anchor_x = x
        self.anchor_y = y

        # Store reference to the window
        self.window = window

        # Enable markup to use BBCode-like tags
        self.markup = True

        # Store style properties
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough

        # Store initial text without markup
        self.raw_text = text

        # Apply the text with markup
        self.text = self.apply_markup(text)

        # Register custom font if provided
        if font and font.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font)
            self.font_name = "CustomFont"
        else:
            self.font_name = "Roboto"  # Default font

        # Set font properties
        self.font_size = font_size
        self.color = font_color

        # Bind the on_font_size method to handle font size changes
        self.bind(font_size=self.on_font_size)

        # Update texture and size
        self.texture_update()
        self.size = self.texture_size

        # Adjust position to keep top-left corner at (x, y)
        self.update_position()

        # Add the text widget to the window
        window.add_widget(self)

    def apply_markup(self, text):
        """Apply markup tags to the text based on style properties."""
        # Start with the raw text
        styled_text = text

        # Apply tags in the correct order
        if self.strikethrough:
            styled_text = f"[s]{styled_text}[/s]"
        if self.underline:
            styled_text = f"[u]{styled_text}[/u]"
        if self.italic:
            styled_text = f"[i]{styled_text}[/i]"
        if self.bold:
            styled_text = f"[b]{styled_text}[/b]"

        return styled_text

    def on_font_size(self, instance, value):
        """Automatically called when font_size changes."""
        self.texture_update()
        self.size = self.texture_size
        self.update_position()

    def update_position(self):
        """Adjust the position of the text to keep the anchor point fixed."""
        # Update texture and size
        self.texture_update()
        self.size = self.texture_size

        # Set position
        self.x = self.anchor_x
        self.y = self.anchor_y - self.height  # Adjust y position based on height

    def set_position(self, x, y):
        """Update the anchor position of the text."""
        self.anchor_x = x
        self.anchor_y = y
        self.update_position()

    def set_text(self, text):
        """Update the text content."""
        self.raw_text = text
        self.text = self.apply_markup(text)
        self.texture_update()
        self.size = self.texture_size

        # Update position after text change
        self.update_position()

    def set_font(self, font):
        """Set a new font for the text."""
        if font and font.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font)
            self.font_name = "CustomFont"
        else:
            self.font_name = font

        self.texture_update()
        self.size = self.texture_size

        # Update position after font change
        self.update_position()

    def set_color(self, color):
        """Set the color of the text."""
        self.color = color

    def set_font_size(self, font_size):
        """Set a new font size for the text."""
        self.font_size = font_size
        # The on_font_size method will be called automatically

    def set_bold(self, bold):
        """Set the bold style."""
        self.bold = bold
        self.text = self.apply_markup(self.raw_text)
        self.texture_update()
        self.size = self.texture_size
        self.update_position()

    def set_italic(self, italic):
        """Set the italic style."""
        self.italic = italic
        self.text = self.apply_markup(self.raw_text)
        self.texture_update()
        self.size = self.texture_size
        self.update_position()

    def set_underline(self, underline):
        """Set the underline style."""
        self.underline = underline
        self.text = self.apply_markup(self.raw_text)
        self.texture_update()
        self.size = self.texture_size
        self.update_position()

    def set_strikethrough(self, strikethrough):
        """Set the strikethrough style."""
        self.strikethrough = strikethrough
        self.text = self.apply_markup(self.raw_text)
        self.texture_update()
        self.size = self.texture_size
        self.update_position()

    def destroy(self):
        """Remove the text widget from the window."""
        # Check if the widget is still part of the window
        if self.window and self in self.window.children:
            self.window.remove_widget(self)


if __name__ == "__main__":
    import pyvisual as pv

    window = pv.Window()

    # Add a text element to the window with styling options
    text_label = Text(
        window=window,
        x=100, y=500,  # Position of the text
        text="Hello World",
        font="Roboto",
        font_size=60,  # Initial font size
        font_color=(0.3, 0.3, 0.3, 1),  # Text color
        bold=True,  # Make the text bold
        italic=True,  # Make the text italic
        underline=True,  # Underline the text
        strikethrough=True,  # strikethrough the text
    )

    # Show the window
    window.show()
