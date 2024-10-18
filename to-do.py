import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class Task:
    def __init__(self, title, description, category, due_date=None):
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date if due_date else None  # Ensure that due_date is not null when it's optional.
        self.completed = False

    def dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "completed": self.completed
        }

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.dict() for task in tasks], f)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            tasks_data = json.load(f)
            return [
                Task(
                    title=data.get('title', ''),
                    description=data.get('description', ''),
                    category=data.get('category', ''),
                    due_date=data.get('due_date', None),
                ) for data in tasks_data if 'title' in data and 'category' in data
            ]
    except FileNotFoundError:
        return []

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List Application")
        # Set the main window background to light blue (simulated)
        self.root.config(bg='#ADD8E6')  # Light Blue Color
        self.tasks = load_tasks()
        
        self.task_listbox = tk.Listbox(root, width=70, height=20)
        self.task_listbox.pack(pady=10)
        
        # Create buttons with hover effects
        self.add_button = self.create_button("Add Task", self.add_task)
        self.mark_completed_button = self.create_button("Mark Task Completed", self.mark_task_completed)
        self.view_button = self.create_button("View Task", self.view_task)
        self.edit_button = self.create_button("Edit Task", self.edit_task)
        self.delete_button = self.create_button("Delete Task", self.delete_task)
        
        # Load tasks into the listbox
        self.load_tasks_to_listbox()

    def create_button(self, text, command):
        """Create a button with hover effects."""
        button = tk.Button(self.root, text=text, command=command)
        button.pack(pady=5)
        # Bind hover events to change background color to lime on hover
        button.bind("<Enter>", lambda e: e.widget.config(background='lime'))
        button.bind("<Leave>", lambda e: e.widget.config(background='SystemButtonFace'))
        return button

    def load_tasks_to_listbox(self):
        """Load tasks into the listbox."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status_icon = "✓" if task.completed else "✗"
            formatted_string = f"{status_icon} {task.title} ({task.category})"
            self.task_listbox.insert(tk.END, formatted_string)

    def add_task(self):
        """Add a new task."""
        title = simpledialog.askstring("Task Title", "Enter task title:")
        description = simpledialog.askstring("Task Description", "Enter task description:")
        category = simpledialog.askstring("Task Category", "Enter task category:")
        due_date = simpledialog.askstring("Task Due Date", "Enter task due date (optional):")
        
        if title and description and category:
            new_task = Task(title, description, category, due_date)
            self.tasks.append(new_task)
            save_tasks(self.tasks)
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Input Error", "All fields must be filled!")

    def mark_task_completed(self):
        """Mark the selected task as completed."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = int(selected_task_index[0])
            self.tasks[task_index].completed = True
            save_tasks(self.tasks)
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def view_task(self):
        """View details of the selected task."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = int(selected_task_index[0])
            task = self.tasks[task_index]
            details_message = (
                f"Title: {task.title}\n"
                f"Description: {task.description}\n"
                f"Category: {task.category}\n"
                f"Due Date: {task.due_date}\n"
                f"Completed: {'Yes' if task.completed else 'No'}"
            )
            messagebox.showinfo("Task Details", details_message)
        else:
            messagebox.showwarning("Selection Error", "Please select a task to view.")

    def edit_task(self):
        """Edit the selected task."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = int(selected_task_index[0])
            task = self.tasks[task_index]
            # Prompt for new values
            title = simpledialog.askstring("Edit Task Title", "Enter new task title:", initialvalue=task.title)
            description = simpledialog.askstring("Edit Task Description", "Enter new task description:", initialvalue=task.description)
            category = simpledialog.askstring("Edit Task Category", "Enter new task category:", initialvalue=task.category)
            due_date = simpledialog.askstring("Edit Task Due Date", "Enter new task due date (optional):", initialvalue=task.due_date)

            if title and description and category:
                # Update the existing task
                task.title = title
                task.description = description
                task.category = category
                task.due_date = due_date
                save_tasks(self.tasks)
                self.load_tasks_to_listbox()
            else:
                messagebox.showwarning("Input Error", "All fields must be filled!")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")

    def delete_task(self):
        """Delete the selected task."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = int(selected_task_index[0])
            del self.tasks[task_index]
            save_tasks(self.tasks)
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
