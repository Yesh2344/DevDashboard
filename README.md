# DevDashboard

DevDashboard is a comprehensive, single-file Python application designed to enhance the daily life of software developers. It serves as a personal dashboard, combining task management, time tracking, GitHub activity monitoring, and system resource tracking in one convenient interface.

## Features

1. **To-Do List Management**
   - Add new tasks
   - Mark tasks as complete
   - Remove tasks from the list

2. **Time Tracking**
   - Start time entries for your work
   - Stop ongoing time entries
   - View recent time entries with durations

3. **GitHub Activity Monitoring**
   - Display recent GitHub events for a specified user
   - Shows event type, repository, and timestamp

4. **System Resource Monitoring**
   - Real-time display of CPU usage
   - Current memory utilization
   - Disk space usage

## Requirements

- Python 3.7+
- rich
- requests
- psutil

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/DevDashboard.git
   cd DevDashboard
   ```

2. Install the required packages:
   ```
   pip install rich requests psutil
   ```

3. Update the GitHub username in the script:
   Open `dev_dashboard.py` and replace `"yesh2344"` with your actual GitHub username.

## Usage

Run the script from the command line:

```
python dev_dashboard.py
```

The dashboard will display in your terminal. Use the following commands to interact with the dashboard:

- `add`: Add a new task
- `complete`: Mark a task as complete
- `remove`: Remove a task
- `start`: Start a new time entry
- `stop`: Stop the current time entry
- `quit`: Exit the dashboard

## Customization

You can easily customize the DevDashboard by modifying the `dev_dashboard.py` file. Some possible customizations include:

- Adding new features or panels to the dashboard
- Changing the color scheme or layout
- Integrating with other APIs or services

## Contributing

Contributions to DevDashboard are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions, feel free to reach out to me at [your-email@example.com](mailto:yeswanthsoma83@example.com).

Happy coding!
