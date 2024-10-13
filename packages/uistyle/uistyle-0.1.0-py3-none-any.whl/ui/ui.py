from datetime import datetime
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from colorama import init, Fore, Style
from loguru import logger

# Initialize colorama for colored console text
init(autoreset=True)

console = Console()

class MyConsoleUI:
    def __init__(self):
        self.start_time = datetime.now()
        logger.add("app.log", format="{time} {level} {message}", level="INFO")
        self.display_banner()

    def display_banner(self):
        """Displays an ASCII banner using pyfiglet."""
        banner = pyfiglet.figlet_format("My Console UI")
        console.print(Panel(banner, title="[green]Welcome![/]", border_style="cyan"))

    def show_time(self):
        """Displays the current time."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        console.print(f"{Fore.LIGHTGREEN_EX}Current Time: {now}{Style.RESET_ALL}")

    def uptime(self):
        """Displays how long the application has been running."""
        elapsed = datetime.now() - self.start_time
        console.print(f"{Fore.LIGHTCYAN_EX}Uptime: {elapsed}{Style.RESET_ALL}")

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
        table = Table(title="Sample Data")

        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="green")

        table.add_row("1", "Alice", "Active")
        table.add_row("2", "Bob", "Inactive")
        table.add_row("3", "Charlie", "Active")

        console.print(table)

# Usage example
if __name__ == "__main__":
    ui = MyConsoleUI()
    ui.show_time()
    ui.display_table()
    ui.uptime()
    ui.log_message("info", "Application started successfully.")
