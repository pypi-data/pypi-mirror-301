```python
from ui import MyConsoleUI
ui = MyConsoleUI()

ui.list_fonts()
ui.banner("slant", text_color="cyan", border_color="bright_cyan", name="UI STYLE")
ui.show_time()
ui.uptime()
ui.log_message("info", "This is an informational message.")
ui.log_message("error", "This is an error message.")
ui.log_message("debug", "This is a debug message.")
ui.log_message("warning", "this is a warning message")
# Example of creating a custom table
headers = ["ID", "Name", "Status"]
data = [
        [1, "Alice", "Active"],
        [2, "Bob", "Inactive"],
        [3, "Charlie", "Active"]
    ]
ui.create_custom_table(headers, data)
```