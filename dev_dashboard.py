import os
import time
import json
import requests
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from datetime import datetime, timedelta

console = Console()

class DevDashboard:
    def __init__(self):
        self.todos = self.load_todos()
        self.time_entries = self.load_time_entries()

    def load_todos(self):
        if os.path.exists('todos.json'):
            with open('todos.json', 'r') as f:
                return json.load(f)
        return []

    def save_todos(self):
        with open('todos.json', 'w') as f:
            json.dump(self.todos, f)

    def load_time_entries(self):
        if os.path.exists('time_entries.json'):
            with open('time_entries.json', 'r') as f:
                return json.load(f)
        return []

    def save_time_entries(self):
        with open('time_entries.json', 'w') as f:
            json.dump(self.time_entries, f)

    def add_todo(self, task):
        self.todos.append({"task": task, "done": False})
        self.save_todos()

    def complete_todo(self, index):
        if 0 <= index < len(self.todos):
            self.todos[index]["done"] = True
            self.save_todos()

    def remove_todo(self, index):
        if 0 <= index < len(self.todos):
            del self.todos[index]
            self.save_todos()

    def start_time_entry(self, description):
        self.time_entries.append({"description": description, "start": time.time(), "end": None})
        self.save_time_entries()

    def stop_time_entry(self):
        if self.time_entries and self.time_entries[-1]["end"] is None:
            self.time_entries[-1]["end"] = time.time()
            self.save_time_entries()

    def get_github_activity(self, username):
        url = f"https://api.github.com/users/{username}/events/public"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()[:5]  # Return the 5 most recent events
        return []

    def get_system_resources(self):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        return cpu, memory, disk

    def display_dashboard(self):
        layout = Layout()
        layout.split_column(
            Layout(name="header"),
            Layout(name="body"),
            Layout(name="footer")
        )
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        layout["right"].split_column(
            Layout(name="right_top"),
            Layout(name="right_bottom")
        )

        # Header
        layout["header"].update(Panel("Developer Dashboard", style="bold magenta"))

        # To-Do List
        todo_table = Table(title="To-Do List", box=box.SIMPLE)
        todo_table.add_column("ID", style="cyan", no_wrap=True)
        todo_table.add_column("Task", style="magenta")
        todo_table.add_column("Status", justify="right", style="green")

        for i, todo in enumerate(self.todos):
            status = "[green]Done" if todo["done"] else "[red]Pending"
            todo_table.add_row(str(i), todo["task"], status)

        # Time Tracker
        time_table = Table(title="Recent Time Entries", box=box.SIMPLE)
        time_table.add_column("Description", style="cyan")
        time_table.add_column("Duration", justify="right", style="green")

        for entry in self.time_entries[-5:]:
            start = entry["start"]
            end = entry["end"] or time.time()
            duration = timedelta(seconds=int(end - start))
            time_table.add_row(entry["description"], str(duration))

        # GitHub Activity
        github_table = Table(title="Recent GitHub Activity", box=box.SIMPLE)
        github_table.add_column("Type", style="cyan")
        github_table.add_column("Repo", style="magenta")
        github_table.add_column("Time", justify="right", style="green")

        github_username = "your_github_username"  # Replace with your GitHub username
        for event in self.get_github_activity(github_username):
            event_type = event["type"].replace("Event", "")
            repo = event["repo"]["name"]
            event_time = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")
            github_table.add_row(event_type, repo, event_time)

        # System Resources
        cpu, memory, disk = self.get_system_resources()
        system_table = Table(title="System Resources", box=box.SIMPLE)
        system_table.add_column("Resource", style="cyan")
        system_table.add_column("Usage", justify="right", style="green")
        system_table.add_row("CPU", f"{cpu}%")
        system_table.add_row("Memory", f"{memory}%")
        system_table.add_row("Disk", f"{disk}%")

        # Update layout
        layout["left"].update(Panel(todo_table, title="Tasks"))
        layout["right"]["right_top"].update(Panel(time_table, title="Time Tracking"))
        layout["right"]["right_bottom"].split_row(
            Panel(github_table, title="GitHub"),
            Panel(system_table, title="System")
        )

        # Render layout
        console.print(layout)

    def run(self):
        while True:
            self.display_dashboard()
            command = console.input("[bold yellow]Enter command (add/complete/remove/start/stop/quit): [/bold yellow]")
            
            if command == "add":
                task = console.input("Enter task: ")
                self.add_todo(task)
            elif command == "complete":
                index = int(console.input("Enter task ID to complete: "))
                self.complete_todo(index)
            elif command == "remove":
                index = int(console.input("Enter task ID to remove: "))
                self.remove_todo(index)
            elif command == "start":
                description = console.input("Enter time entry description: ")
                self.start_time_entry(description)
            elif command == "stop":
                self.stop_time_entry()
            elif command == "quit":
                break
            else:
                console.print("Invalid command. Try again.", style="bold red")

if __name__ == "__main__":
    dashboard = DevDashboard()
    dashboard.run()