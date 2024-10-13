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
        logger.add("app.log", format="{time} {level} {message}", level="INFO")

    def banner(self, font="slant", name="🔥 SEXY UI 🔥"):
        """Displays a custom ASCII banner with the chosen font."""
        try:
            # Create the banner with pyfiglet
            banner_text = pyfiglet.Figlet(font=font).renderText(name)
            # Display with rich's panel for side borders
            panel = Panel(
                Text.from_ansi(banner_text),
                title=f"[bold magenta]✨ Welcome to {name}! ✨[/]",
                border_style="bright_yellow",
                padding=(1, 2),  # Add some space around the banner
                expand=False  # Keep the panel tight
            )
            console.print(panel)
        except pyfiglet.FontNotFound:
            console.print(f"[bold red]Font '{font}' not found! Using default font.[/bold red]")
            banner_text = pyfiglet.figlet_format(name)
            console.print(Panel(banner_text, title="[green]Welcome![/]", border_style="cyan"))

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

    def display_table(self):
        """Displays a sample table using rich."""
        table = Table(title="[bold magenta]Sample Data[/bold magenta]")

        # Add columns with styles
        table.add_column("ID", style="bold cyan", justify="right", no_wrap=True)
        table.add_column("Name", style="bold magenta")
        table.add_column("Status", style="bold green")

        # Add rows with content
        table.add_row("1", "Alice", "[green]Active[/green]")
        table.add_row("2", "Bob", "[red]Inactive[/red]")
        table.add_row("3", "Charlie", "[green]Active[/green]")

        console.print(table)

# Usage example
if __name__ == "__main__":
    ui = MyConsoleUI()

    # Showcase different banners with various fonts
    ui.banner("graffiti", "🔥 SEXY UI 🔥")
    ui.banner("big", "BIG FONT")
    ui.banner("larry3d", "3D Look")

    ui.show_time()
    ui.display_table()
    ui.uptime()
    ui.log_message("info", "Application started successfully.")
