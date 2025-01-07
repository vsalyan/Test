import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime

# Global list to store tasks
tasks = []

def load_tasks():
    """
    Load tasks from a JSON file if it exists.
    Returns:
        list: A list of tasks loaded from the file.
    """
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            try:
                loaded_tasks = json.load(file)
                if isinstance(loaded_tasks, list) and all(isinstance(task, dict) for task in loaded_tasks):
                    return loaded_tasks
                else:
                    messagebox.showwarning("Warning", "Invalid tasks format in tasks.json")
                    return []
            except json.JSONDecodeError:
                messagebox.showwarning("Warning", "Error decoding tasks.json")
                return []
    return []

def save_tasks():
    """
    Save the current list of tasks to a JSON file.
    """
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def validate_date_format(date_text):
    """
    Validate the date format to ensure it matches 'YYYY-MM-DD HH:MM'.
    Args:
        date_text (str): The date string to validate.
    Returns:
        bool: True if the date format is valid, False otherwise.
    """
    try:
        datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def add_task(event=None):
    """
    Add a new task to the list and update the display.
    Args:
        event (tk.Event, optional): The event that triggered the function. Defaults to None.
    """
    task = entry_task.get()
    due_date = f"{date_entry.get()} {hour_spinbox.get()}:{minute_spinbox.get()}"
    if task and due_date:
        if validate_date_format(due_date):
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            tasks.append({"task": task, "created_at": created_at, "due_date": due_date})
            listbox_tasks.insert(tk.END, f"{task} (Created: {created_at}, Due: {due_date})")
            entry_task.delete(0, tk.END)
            save_tasks()
        else:
            messagebox.showwarning("Warning", "Due date must be in the format YYYY-MM-DD HH:MM")
    else:
        messagebox.showwarning("Warning", "You must enter both a task and a due date.")

def delete_task():
    """
    Delete the selected task from the list and update the display.
    """
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(selected_task_index)
        tasks.pop(selected_task_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

def view_tasks():
    """
    Display all tasks in the listbox.
    """
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        listbox_tasks.insert(tk.END, f"{task['task']} (Created: {task['created_at']}, Due: {task['due_date']})")

def sort_tasks_by_task():
    """
    Sort tasks alphabetically by task name and update the display.
    """
    tasks.sort(key=lambda x: x['task'])
    save_tasks()
    view_tasks()

def sort_tasks_by_due_date():
    """
    Sort tasks by due date and update the display.
    """
    tasks.sort(key=lambda x: datetime.strptime(x['due_date'], "%Y-%m-%d %H:%M"))
    save_tasks()
    view_tasks()

def sort_tasks_by_created_date():
    """
    Sort tasks by creation date and update the display.
    """
    tasks.sort(key=lambda x: datetime.strptime(x['created_at'], "%Y-%m-%d %H:%M"))
    save_tasks()
    view_tasks()

# Create the main window
window = tk.Tk()
window.title("To-Do List")
window.geometry("600x400")
window.configure(bg="#2e2e2e")

# Configure grid layout
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create a frame for the task input
frame_input = tk.Frame(window, bg="#2e2e2e")
frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Configure grid layout for frame_input
frame_input.grid_columnconfigure(1, weight=1)
frame_input.grid_columnconfigure(2, weight=1)

# Create a label and entry widget to add new tasks
label_task = tk.Label(frame_input, text="Task:", bg="#2e2e2e", fg="white")
label_task.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_task = tk.Entry(frame_input, width=40, bg="#3e3e3e", fg="white", insertbackground="white")
entry_task.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
entry_task.bind("<Return>", add_task)  # Bind the Enter key to the add_task function

# Create a label and date entry widget to add due date
label_due_date = tk.Label(frame_input, text="Due Date:", bg="#2e2e2e", fg="white")
label_due_date.grid(row=1, column=0, padx=5, pady=5, sticky="e")
date_entry = DateEntry(frame_input, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Create spinboxes for hour and minute selection
time_frame = tk.Frame(frame_input, bg="#2e2e2e")
time_frame.grid(row=1, column=2, padx=5, pady=5, sticky="w")

label_time = tk.Label(time_frame, text="Time (HH:MM):", bg="#2e2e2e", fg="white")
label_time.pack(side=tk.LEFT)
hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f", bg="#3e3e3e", fg="white", buttonbackground="#2e2e2e")
hour_spinbox.pack(side=tk.LEFT)
minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f", bg="#3e3e3e", fg="white", buttonbackground="#2e2e2e")
minute_spinbox.pack(side=tk.LEFT)

# Create a frame for the buttons
frame_buttons = tk.Frame(window, bg="#2e2e2e")
frame_buttons.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Configure grid layout for frame_buttons
frame_buttons.grid_columnconfigure(0, weight=1)
frame_buttons.grid_columnconfigure(1, weight=1)

# Create a button to add tasks
button_add_task = tk.Button(frame_buttons, text="Add task", width=20, command=add_task, bg="#4e4e4e", fg="white")
button_add_task.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Create a button to delete tasks
button_delete_task = tk.Button(frame_buttons, text="Delete task", width=20, command=delete_task, bg="#4e4e4e", fg="white")
button_delete_task.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Create a button to view tasks
button_view_tasks = tk.Button(frame_buttons, text="View tasks", width=20, command=view_tasks, bg="#4e4e4e", fg="white")
button_view_tasks.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Create a button to sort tasks by task
button_sort_tasks_by_task = tk.Button(frame_buttons, text="Sort tasks by task", width=20, command=sort_tasks_by_task, bg="#4e4e4e", fg="white")
button_sort_tasks_by_task.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Create a button to sort tasks by due date
button_sort_tasks_by_due_date = tk.Button(frame_buttons, text="Sort tasks by due date", width=20, command=sort_tasks_by_due_date, bg="#4e4e4e", fg="white")
button_sort_tasks_by_due_date.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Create a button to sort tasks by created date
button_sort_tasks_by_created_date = tk.Button(frame_buttons, text="Sort tasks by created date", width=20, command=sort_tasks_by_created_date, bg="#4e4e4e", fg="white")
button_sort_tasks_by_created_date.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Create a frame for the listbox and scrollbar
frame_tasks = tk.Frame(window, bg="#2e2e2e")
frame_tasks.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configure grid layout for frame_tasks
frame_tasks.grid_rowconfigure(0, weight=1)
frame_tasks.grid_columnconfigure(0, weight=1)

# Create a listbox to display tasks
listbox_tasks = tk.Listbox(frame_tasks, height=10, width=80, bg="#3e3e3e", fg="white", selectbackground="#5e5e5e")
listbox_tasks.grid(row=0, column=0, sticky="nsew")

# Create a scrollbar for the listbox
scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.grid(row=0, column=1, sticky="ns")

# Attach the scrollbar to the listbox
listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

# Load tasks from file and display them
tasks = load_tasks()
view_tasks()

# Run the main loop
window.mainloop()