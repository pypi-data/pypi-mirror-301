from enum import Enum


class AnsiColor:
    def __init__(self, colorCode: int):
        self.code = f"\033[{colorCode}m"

    @property
    def value(self):
        return self.code


class AnsiRGB:
    def __init__(self, r: int, g: int, b: int):
        self.code = f"\u001b[38;2;{r};{g};{b}m"

    @property
    def value(self):
        return self.code


class Colors(Enum):
    BLACK = AnsiColor(30)
    RED = AnsiColor(31).value
    GREEN = AnsiColor(32).value
    YELLOW = AnsiColor(33).value  # orange on some systems
    BLUE = AnsiColor(34).value
    MAGENTA = AnsiColor(35).value
    CYAN = AnsiColor(36).value
    LIGHT_GRAY = AnsiColor(37).value
    DARK_GRAY = AnsiColor(90).value
    BRIGHT_RED = AnsiColor(91).value
    BRIGHT_GREEN = AnsiColor(92).value
    BRIGHT_YELLOW = AnsiColor(93).value
    BRIGHT_BLUE = AnsiColor(94).value
    BRIGHT_MAGENTA = AnsiColor(95).value
    BRIGHT_CYAN = AnsiColor(96).value
    WHITE = AnsiColor(97).value

    RESET = '\033[0m'  # called to return to standard terminal text color


def color(text: str, color: Colors | AnsiColor | AnsiRGB, reset: bool = True) -> str:
    if reset:
        text = color + text + Colors.RESET.value
    elif not reset:
        text = color.value + text

    return text
