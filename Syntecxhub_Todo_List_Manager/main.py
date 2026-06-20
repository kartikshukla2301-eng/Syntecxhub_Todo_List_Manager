import os
import json
import tkinter as tk
from tkinter import messagebox, ttk

# Path to the tasks JSON file (relative to the script location)
FILENAME = os.path.join(os.path.dirname(__file__), "tasks.json")

# =====================================================================
# FILE OPERATIONS
# =====================================================================

def load_tasks(file_path):
    """Loads tasks from the JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, PermissionError):
        # Return empty list if file is empty or corrupted
        return []

def save_tasks(file_path, tasks):
    """Saves the tasks list to the JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, indent=2)
        return True
    except IOError:
        return False

# =====================================================================
# BUSINESS LOGIC (Separated from UI and File I/O)
# =====================================================================

def add_task(tasks, title, priority):
    """Creates a new task and appends it to the tasks list."""
    new_id = 1
    if tasks:
        new_id = max(task['id'] for task in tasks) + 1
    
    new_task = {
        "id": new_id,
        "task": title,
        "priority": priority,
        "completed": False
    }
    tasks.append(new_task)
    return new_task

def complete_task(tasks, task_id):
    """Marks the task with the given ID as completed."""
    for task in tasks:
        if task['id'] == task_id:
            if task['completed']:
                return "already_completed"
            task['completed'] = True
            return "success"
    return "not_found"

def delete_task(tasks, task_id):
    """Deletes the task with the given ID from the tasks list."""
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            return True
    return False

def search_tasks(tasks, keyword):
    """Searches for tasks matching the keyword in the title (case-insensitive)."""
    keyword_lower = keyword.lower()
    return [task for task in tasks if keyword_lower in task['task'].lower()]

def calculate_statistics(tasks):
    """Calculates summary statistics of the tasks."""
    total = len(tasks)
    completed = sum(1 for task in tasks if task['completed'])
    pending = total - completed
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }

# =====================================================================
# DESKTOP APPLICATION CLASS (Tkinter UI)
# =====================================================================

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntecxhub To-Do List Manager")
        self.root.geometry("820x520")
        self.root.configure(bg="white")
        
        # Load tasks from file
        self.tasks = load_tasks(FILENAME)
        
        # Set up a clean default layout style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure style parameters (Simple white & light gray theme)
        self.style.configure(".", background="white", foreground="black")
        self.style.configure("TLabel", background="white", foreground="black", font=("Arial", 10))
        self.style.configure("TButton", background="#f0f0f0", foreground="black", font=("Arial", 10), borderwidth=1)
        self.style.map("TButton", background=[("active", "#e0e0e0")])
        self.style.configure("Heading.TLabel", font=("Arial", 14, "bold"), background="white")
        
        # Configure Table (Treeview) Styling
        self.style.configure("Treeview", background="white", fieldbackground="white", foreground="black", font=("Arial", 9))
        self.style.configure("Treeview.Heading", background="#f0f0f0", foreground="black", font=("Arial", 9, "bold"))
        self.style.map("Treeview", background=[("selected", "#e0e0e0")], foreground=[("selected", "black")])
        
        # Main Title Label
        title_label = ttk.Label(self.root, text="TO-DO LIST MANAGER", style="Heading.TLabel")
        title_label.pack(pady=15)
        
        # Main Grid/Box Container
        self.main_container = tk.Frame(self.root, bg="white")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # -------------------------------------------------------------
        # LEFT PANEL: Controls & Input
        # -------------------------------------------------------------
        self.left_frame = tk.LabelFrame(
            self.main_container, 
            text="Task Details", 
            bg="white", 
            fg="black", 
            font=("Arial", 10, "bold"), 
            padx=15, 
            pady=15, 
            bd=1, 
            relief=tk.SOLID
        )
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=5)
        
        # Task Title Entry
        ttk.Label(self.left_frame, text="Task Title:").pack(anchor=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(self.left_frame, width=25, font=("Arial", 10))
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Task Priority Selection
        ttk.Label(self.left_frame, text="Priority:").pack(anchor=tk.W, pady=(0, 5))
        self.priority_combo = ttk.Combobox(
            self.left_frame, 
            values=["High", "Medium", "Low"], 
            state="readonly", 
            width=23, 
            font=("Arial", 10)
        )
        self.priority_combo.set("Medium")
        self.priority_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Add Task Button
        self.add_button = ttk.Button(self.left_frame, text="Add Task", command=self.add_task_click)
        self.add_button.pack(fill=tk.X, pady=(0, 20))
        
        # Separator line
        separator = ttk.Separator(self.left_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 15))
        
        # Search Section
        ttk.Label(self.left_frame, text="Search Keyword:").pack(anchor=tk.W, pady=(0, 5))
        self.search_entry = ttk.Entry(self.left_frame, width=25, font=("Arial", 10))
        self.search_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Search Buttons Grid
        self.search_btn_frame = tk.Frame(self.left_frame, bg="white")
        self.search_btn_frame.pack(fill=tk.X)
        
        self.search_btn = ttk.Button(self.search_btn_frame, text="Search", command=self.search_task_click, width=10)
        self.search_btn.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        
        self.refresh_btn = ttk.Button(self.search_btn_frame, text="Refresh", command=self.refresh_task_click, width=10)
        self.refresh_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        # -------------------------------------------------------------
        # RIGHT PANEL: Table View & Selection Actions
        # -------------------------------------------------------------
        self.right_frame = tk.Frame(self.main_container, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5)
        
        # Table Scrollbar
        scroll_y = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL)
        
        # Treeview (Table Widget)
        self.tree = ttk.Treeview(
            self.right_frame, 
            columns=("id", "task", "priority", "status"), 
            show="headings", 
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.tree.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Set Table Headers
        self.tree.heading("id", text="ID", anchor=tk.W)
        self.tree.heading("task", text="Task Name", anchor=tk.W)
        self.tree.heading("priority", text="Priority", anchor=tk.W)
        self.tree.heading("status", text="Status", anchor=tk.W)
        
        # Set Columns configuration
        self.tree.column("id", width=50, minwidth=50, stretch=tk.NO)
        self.tree.column("task", width=250, minwidth=150, stretch=tk.YES)
        self.tree.column("priority", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("status", width=95, minwidth=95, stretch=tk.NO)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control Buttons Frame
        self.action_frame = tk.Frame(self.right_frame, bg="white")
        self.action_frame.pack(fill=tk.X)
        
        self.complete_btn = ttk.Button(self.action_frame, text="Mark Complete", command=self.complete_task_click)
        self.complete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_btn = ttk.Button(self.action_frame, text="Delete Task", command=self.delete_task_click)
        self.delete_btn.pack(side=tk.LEFT)
        
        # -------------------------------------------------------------
        # BOTTOM PANEL: Statistics Bar
        # -------------------------------------------------------------
        self.stats_frame = tk.LabelFrame(
            self.root, 
            text="Statistics", 
            bg="#fcfcfc", 
            fg="black", 
            font=("Arial", 9, "bold"), 
            bd=1, 
            relief=tk.SOLID
        )
        self.stats_frame.pack(fill=tk.X, padx=20, pady=(10, 15))
        
        # Dynamic tracking string variables
        self.total_stats_var = tk.StringVar(value="Total Tasks: 0")
        self.completed_stats_var = tk.StringVar(value="Completed: 0")
        self.pending_stats_var = tk.StringVar(value="Pending: 0")
        
        self.total_lbl = tk.Label(self.stats_frame, textvariable=self.total_stats_var, bg="#fcfcfc", fg="black", font=("Arial", 9))
        self.total_lbl.pack(side=tk.LEFT, padx=30, pady=5)
        
        self.completed_lbl = tk.Label(self.stats_frame, textvariable=self.completed_stats_var, bg="#fcfcfc", fg="green", font=("Arial", 9))
        self.completed_lbl.pack(side=tk.LEFT, padx=30, pady=5)
        
        self.pending_lbl = tk.Label(self.stats_frame, textvariable=self.pending_stats_var, bg="#fcfcfc", fg="#b05000", font=("Arial", 9))
        self.pending_lbl.pack(side=tk.LEFT, padx=30, pady=5)
        
        # Load tasks into interface
        self.refresh_tasks_display(self.tasks)
        
    # =================================================================
    # ACTIONS & EVENT HANDLERS
    # =================================================================
    
    def refresh_tasks_display(self, tasks_to_show):
        """Clears and re-populates the Treeview table with the given tasks list."""
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Re-populate
        for t in tasks_to_show:
            status_text = "Completed" if t["completed"] else "Pending"
            self.tree.insert("", tk.END, values=(t["id"], t["task"], t["priority"], status_text))
            
        # Update statistics based on standard task list (active data)
        self.update_statistics()

    def update_statistics(self):
        """Calculates task numbers and updates statistics labels."""
        stats = calculate_statistics(self.tasks)
        self.total_stats_var.set(f"Total Tasks: {stats['total']}")
        self.completed_stats_var.set(f"Completed Tasks: {stats['completed']}")
        self.pending_stats_var.set(f"Pending Tasks: {stats['pending']}")

    def add_task_click(self):
        """Adds a new task using inputs from the text entry and priority combobox."""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Task title cannot be empty.")
            return
            
        priority = self.priority_combo.get()
        new_task = add_task(self.tasks, title, priority)
        
        if save_tasks(FILENAME, self.tasks):
            # Reset title field
            self.title_entry.delete(0, tk.END)
            self.refresh_tasks_display(self.tasks)
            messagebox.showinfo("Success", f"Task '{title}' has been added successfully.")
        else:
            messagebox.showerror("File Error", "Failed to save the task. Please check file permissions.")

    def get_selected_task_id(self):
        """Retrieves the ID from the selected treeview row."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a task from the table first.")
            return None
        values = self.tree.item(selected_item, "values")
        return int(values[0])

    def complete_task_click(self):
        """Marks the selected task as completed."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
            
        status = complete_task(self.tasks, task_id)
        if status == "success":
            if save_tasks(FILENAME, self.tasks):
                self.refresh_task_click()
                messagebox.showinfo("Success", f"Task ID {task_id} has been marked as completed.")
            else:
                messagebox.showerror("File Error", "Failed to save updates to disk.")
        elif status == "already_completed":
            messagebox.showinfo("Info", "This task is already completed.")
        else:
            messagebox.showerror("Error", f"Task ID {task_id} not found.")

    def delete_task_click(self):
        """Deletes the selected task."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
            
        # Request confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to permanently delete Task ID {task_id}?"
        )
        if not confirm:
            return
            
        if delete_task(self.tasks, task_id):
            if save_tasks(FILENAME, self.tasks):
                self.refresh_task_click()
                messagebox.showinfo("Success", f"Task ID {task_id} has been deleted.")
            else:
                messagebox.showerror("File Error", "Failed to save changes to tasks.json.")
        else:
            messagebox.showerror("Error", f"Task ID {task_id} not found.")

    def search_task_click(self):
        """Filters tasks shown based on keyword entry."""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Validation Error", "Please enter a search keyword.")
            return
            
        matching_tasks = search_tasks(self.tasks, keyword)
        self.refresh_tasks_display(matching_tasks)

    def refresh_task_click(self):
        """Clears search filter and displays the full active list."""
        self.search_entry.delete(0, tk.END)
        self.refresh_tasks_display(self.tasks)


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
