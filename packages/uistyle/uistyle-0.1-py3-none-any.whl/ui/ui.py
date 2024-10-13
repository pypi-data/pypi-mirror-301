from datetime import datetime
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from colorama import init, Fore, Style
from loguru import logger

# Initialize colorama for colored console text
init(autoreset=True)

console = Console()

class MyConsoleUI:
    def __init__(self):
        self.start_time = datetime.now()
        logger.add("uistyle.log", format="{time} {level} {message}", level="INFO")

        # List of fonts to choose from
        self.font_options = [
            "slant", "graffiti", "big", "larry3d", 
            "banner3-D", "speed", "block", "roman", 
            "smkeyboard", "standard"
        ]

    def banner(self, font="slant", text_color="yellow", border_color="bright_yellow", width=80, name="UI STYLE", show_border=True):
        """Displays a custom ASCII banner."""
        try:
            # Create banner using pyfiglet
            banner_text = pyfiglet.Figlet(font=font, width=width).renderText(name)
            colored_text = f"[{text_color}]{banner_text}[/{text_color}]"

            if show_border:
                # Display with a border using rich Panel
                panel = Panel(
                    Text.from_markup(colored_text),
                    title=f"",
                    border_style=border_color,
                    padding=(1, 2),
                    expand=False
                )
                console.print(panel)
            else:
                console.print(Text.from_markup(colored_text))
        except pyfiglet.FontNotFound:
            console.print(f"[bold red]Font '{font}' not found! Using default font.[/bold red]")
            console.print(pyfiglet.figlet_format(name))

    def show_time(self):
        """Displays the current time."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        console.print(f"{Fore.LIGHTGREEN_EX}⏰ Current Time: {now}{Style.RESET_ALL}")

    def uptime(self):
        """Displays how long the application has been running."""
        elapsed = datetime.now() - self.start_time
        console.print(f"{Fore.LIGHTCYAN_EX}🕒 Uptime: {elapsed}{Style.RESET_ALL}")

    def log_message(self, level, message):
        """Logs a message with the specified level."""
        log_methods = {
            'info': logger.info,
            'debug': logger.debug,
            'error': logger.error,
            'warning': logger.warning
        }
        log_methods.get(level, logger.info)(message)

    def create_custom_table(self, headers, data):
        """Creates a table with user-specified headers and data."""
        if not headers or not data:
            console.print("[bold red]Headers and data cannot be empty![/bold red]")
            return

        # Initialize the table
        table = Table(title="[bold magenta]Custom Table[/bold magenta]")

        # Add user-defined headers
        for header in headers:
            table.add_column(header, style="bold cyan")

        # Add data rows
        for row in data:
            table.add_row(*[str(item) for item in row])

        # Display the table
        console.print(table)

    def list_fonts(self):
        """Displays the available font options."""
        console.print("[bold magenta]Available Fonts:[/bold magenta]")
        for idx, font in enumerate(self.font_options, 1):
            console.print(f"{Fore.CYAN}{idx}. {font}")

# Usage example
if __name__ == "__main__":
    ui = MyConsoleUI()

    # List available fonts
    ui.list_fonts()

    # Display banners with fonts and border options
    ui.banner("graffiti", text_color="cyan", border_color="bright_cyan", name="🔥 GRAFFITI 🔥")
    ui.banner("big", text_color="magenta", border_color="bright_magenta", name="🔥 BIG FONT 🔥", show_border=False)
    ui.banner("larry3d", text_color="green", border_color="bright_green", name="🔥 3D LOOK 🔥")

    # Show current time and uptime
    ui.show_time()
    ui.uptime()

    # Log a custom message
    ui.log_message("info", "Application started successfully.")

    # Example of creating a custom table
    headers = ["ID", "Name", "Status"]
    data = [
        [1, "Alice", "Active"],
        [2, "Bob", "Inactive"],
        [3, "Charlie", "Active"]
    ]
    ui.create_custom_table(headers, data)
