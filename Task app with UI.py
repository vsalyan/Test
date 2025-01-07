import tkinter as tk
from tkinter import messagebox

tasks = []

def add_task():
    task = entry_task.get()
    if task:
        tasks.append(task)
        listbox_tasks.insert(tk.END, task)
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(selected_task_index)
        tasks.pop(selected_task_index)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

def view_tasks():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        listbox_tasks.insert(tk.END, task)

# Create the main window
window = tk.Tk()
window.title("To-Do List")

# Create a frame for the listbox and scrollbar
frame_tasks = tk.Frame(window)
frame_tasks.pack()

# Create a listbox to display tasks
listbox_tasks = tk.Listbox(frame_tasks, height=10, width=50)
listbox_tasks.pack(side=tk.LEFT)

# Create a scrollbar for the listbox
scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the scrollbar to the listbox
listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

# Create an entry widget to add new tasks
entry_task = tk.Entry(window, width=50)
entry_task.pack()

# Create a button to add tasks
button_add_task = tk.Button(window, text="Add task", width=48, command=add_task)
button_add_task.pack()

# Create a button to delete tasks
button_delete_task = tk.Button(window, text="Delete task", width=48, command=delete_task)
button_delete_task.pack()

# Create a button to view tasks
button_view_tasks = tk.Button(window, text="View tasks", width=48, command=view_tasks)
button_view_tasks.pack()

# Run the main loop
window.mainloop()