# Syntecxhub To-Do List Manager

A simple, desktop-based To-Do List Manager written in Python using the Tkinter graphical library. This project was developed as part of an internship task to demonstrate fundamental programming concepts, input validation, file I/O operations, desktop UI layouts, and clean logic separation.

## Project Overview

The Syntecxhub To-Do List Manager is a desktop GUI application designed to help users organize their daily tasks. Tasks are saved locally in a JSON file, ensuring that they persist even after the program is closed or restarted. 

## Features

- **Add Task (Left Panel)**: Input a task title, select a priority level (High, Medium, Low) using a dropdown, and add it directly to your list.
- **View Tasks (Right Panel)**: Display all tasks in a clean, scrollable tabular view (Treeview) showing ID, Task Name, Priority, and Status.
- **Complete Task**: Select a pending task from the table and mark it as completed.
- **Delete Task**: Select a task and delete it permanently.
- **Search Task**: Filter tasks by entering a search keyword.
- **Refresh View**: Clear search filters to show the full list of tasks.
- **Statistics (Bottom Bar)**: View dynamic counts of total, completed, and pending tasks.
- **Data Persistence**: Tasks are saved to and loaded from `tasks.json`.

## Technologies Used

- **Language**: Python 3
- **GUI Toolkit**: Tkinter & Ttk (Python standard library)
- **Data Storage**: JSON (Python standard library `json` module)
- **Path Handling**: `os` module for cross-platform path resolution

## Installation

1. Make sure Python 3.x is installed on your computer.
2. Clone or download the repository files:
   ```bash
   git clone https://github.com/yourusername/Syntecxhub_Todo_List_Manager.git
   cd Syntecxhub_Todo_List_Manager
   ```
3. Since the app uses standard Tkinter libraries, no external dependencies or packages need to be installed.

## Usage

Run the program by executing `main.py` using Python in your terminal:

```bash
python main.py
```

This will launch a desktop GUI window. All options and inputs are managed through the graphical interface.

## GUI Layout

- **Left Side Panel**: Includes fields to type new tasks, select priorities, and search by keywords.
- **Right Side Panel**: Houses the main tasks table and action buttons (`Mark Complete`, `Delete Task`).
- **Bottom Panel**: Contains the live statistics panel.

## Future Improvements

- Add task sorting based on priority levels.
- Implement due dates for tasks.
- Add task categorization tags (e.g., Work, Personal, Study).
