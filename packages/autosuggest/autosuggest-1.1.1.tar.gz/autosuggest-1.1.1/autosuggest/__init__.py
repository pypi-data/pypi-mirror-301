import os
import sys

# Platform-specific imports
if os.name == 'nt':
    import msvcrt  # Windows
else:
    import tty
    import termios


class Styles:
    """Class to define terminal text styles."""
    HEADER = "\033[1;34m"  # Blue
    PROMPT = "\033[1;32m"  # Green
    INSTRUCTION = "\033[1;34m"  
    SUGGESTION_HIGHLIGHT = "\033[1;33m"  # Yellow
    MATCH_HIGHLIGHT = "\033[1;32m"  # Green
    ERROR = "\033[1;31m"  # Red
    RESET = "\033[0m"  # Reset color


class InputHandler:
    """Class to handle input from the user."""
    def getch(self):
        """Reads a single character from standard input."""
        if os.name == 'nt':  # Windows
            return msvcrt.getch().decode()
        else:  # Unix-based systems
            return self._getch_unix()

    def _getch_unix(self):
        """Unix-specific method to read a single character."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')


class Suggestions:
    """Class to manage suggestions based on user input."""
    def __init__(self, suggestions):
        self.suggestions = suggestions

    def get_matching_suggestions(self, current_input):
        """Returns suggestions matching the current input."""
        return [name for name in self.suggestions if name.lower().startswith(current_input.lower())]

    def highlight_match(self, current_input, suggestion):
        """Highlights the matching part of the suggestion."""
        match_length = len(current_input)
        return f"{Styles.MATCH_HIGHLIGHT}{suggestion[:match_length]}{Styles.RESET}{suggestion[match_length:]}"  # Highlight matching part


class AutoSuggest:
    """Main class to run the auto-suggestion feature."""
    def __init__(self, suggestions, input_message="Enter name: ", use_colors=True):
        self.input_handler = InputHandler()
        self.suggestions = Suggestions(suggestions)
        self.current_input = ""
        self.input_message = input_message
        self.use_colors = use_colors

    def run(self):
        """Runs the auto-suggest feature."""
        self.input_handler.clear_screen()

        while True:
            # Construct the prompt based on color usage
            if self.use_colors:
                prompt = f"{Styles.PROMPT}{self.input_message}{Styles.RESET}"
            else:
                prompt = self.input_message

            print(f"{prompt}{self.current_input}", end='', flush=True)

            # Get user input
            char = self.input_handler.getch()

            if char == '\x1b':  # ESC key
                break
            elif char == '\x08' or char == '\x7f':  # Backspace
                self.current_input = self.current_input[:-1]
            elif char == '\n':  # Enter key
                print(f"\nYou selected: {self.current_input}")
                break
            else:
                self.current_input += char

            # Clear the current line and display suggestions
            self.input_handler.clear_screen()
            
            # Get suggestions and highlight matches
            suggestions = self.suggestions.get_matching_suggestions(self.current_input)
            if self.use_colors:
                for suggestion in suggestions:
                    highlighted = self.suggestions.highlight_match(self.current_input, suggestion)
                    print(highlighted)
            else:
                for suggestion in suggestions:
                    print(suggestion)  # Print without colors

        return self.current_input

