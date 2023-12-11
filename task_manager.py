import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from database import TaskDatabase
from ctypes import windll, byref, sizeof, c_int
import customtkinter as ctk

class TaskManager(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task_db = TaskDatabase()

        #Custom Theme
        self.tk_setPalette(background="#ececec")  
        self.style = ttk.Style()
        self.style.theme_use("default")  

        #Custom Window Bar Color
        HWND = windll.user32.GetParent(self.winfo_id())
        window_bg_color = 0x00FF8800
        window_text_color = 0x00FFFFFF
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(window_bg_color)),
            sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            36,
            byref(c_int(window_text_color)),
            sizeof(c_int))

        self.geometry("750x500")

        # Create GUI
        self.create_widgets()
        self.center_window()  # Center the window on startup

    def create_widgets(self):
        # Create a custom style for the buttons
        self.style.configure("Custom.TButton",
                            background="#3595D7",  # Set your desired background color
                            foreground="white",  # Set your desired text color
                            font=('Outfit', 12),  # Set your desired font
                            borderwidth=0,  # Set border width
                            relief="solid", # Set border style
                            height=2  
                            )
        
        self.style.configure("Custom.TEntry",
                    fieldbackground="white",  # Set the background color
                    height=10  # Set the desired height of the entry
                    )
        
        # Create a custom style for the hover effect
        self.style.map("Custom.TButton",
                   background=[("active", "#2F7CB1")],  # Set the background color on hover
                   )

        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self, textvariable=self.search_var, style="Custom.TEntry", font=('Outfit', 12))
        search_entry.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        # Search Button
        search_button = ttk.Button(self, text="Search", command=self.search, style="Custom.TButton")
        search_button.grid(row=0, column=1, padx=(0, 10), pady=20, sticky="e")

        # Add Task Button
        add_task_button = ttk.Button(self, text="Add Task", command=self.open_add_task_window, style="Custom.TButton")
        add_task_button.grid(row=0, column=2, padx=10, pady=20, sticky="e")


        # Task Table
        columns = ["ID", "Task Name", "Priority", "Due Date", "Status", "Done"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        column_widths = [50, 200, 80, 100, 100, 80]  # Adjust these values as needed

        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        self.tree.grid(row=1, column=0, columnspan=3, pady=5, padx=10, sticky="nsew")

        # Load tasks into the table
        self.load_tasks()

        # Delete Task Button
        delete_task_button = ttk.Button(self, text="Delete Task", command=self.delete_task, style="Custom.TButton")
        delete_task_button.grid(row=2, column=0, padx=10, pady=15, sticky="w")

        # Clear Task Button
        clear_task_button = ttk.Button(self, text="Clear Task", command=self.clear_task, style="Custom.TButton")
        clear_task_button.grid(row=2, column=2, padx=10, pady=15, sticky="e")

        # Configure grid weights to make the table expandable/resizable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def open_add_task_window(self):
        # Add Task Window
        add_task_window = tk.Toplevel(self)
        add_task_window.title("Add Task - Task Management System")

        # Calculate the position to center the window on the main window
        window_width = add_task_window.winfo_reqwidth()
        window_height = add_task_window.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2.2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2.3 - window_height / 2)
        add_task_window.geometry(f"+{position_right}+{position_down}")

        # Configure row and column weights for responsiveness
        add_task_window.grid_rowconfigure(0, weight=1)
        add_task_window.grid_rowconfigure(6, weight=1)
        add_task_window.grid_columnconfigure(0, weight=1)
        add_task_window.grid_columnconfigure(2, weight=1)

        # Labels and Entry widgets
        tk.Label(add_task_window, text="Task Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        task_name_entry = tk.Entry(add_task_window)
        task_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_task_window, text="Priority:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        priority_choices = ["High", "Medium", "Low"]
        priority_var = tk.StringVar()
        priority_var.set(priority_choices[0])
        priority_dropdown = ttk.Combobox(add_task_window, values=priority_choices, textvariable=priority_var)
        priority_dropdown.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_task_window, text="Due Date:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        due_date_entry = DateEntry(add_task_window, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        due_date_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(add_task_window, text="Status:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        status_choices = ["Not Started", "In Progress", "Completed"]
        status_var = tk.StringVar()
        status_var.set(status_choices[0])
        status_dropdown = ttk.Combobox(add_task_window, values=status_choices, textvariable=status_var)
        status_dropdown.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(add_task_window, text="Done:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        done_choices = ["Yes", "No"]
        done_var = tk.StringVar()
        done_var.set(done_choices[1])
        done_dropdown = ttk.Combobox(add_task_window, values=done_choices, textvariable=done_var)
        done_dropdown.grid(row=4, column=1, padx=10, pady=10)

        # Add Task Button with custom style
        ttk.Button(add_task_window, text="Add Task", command=lambda: self.add_task(
            task_name_entry.get(),
            priority_var.get(),
            due_date_entry.get(),
            status_var.get(),
            done_var.get()
        ), style="Custom.TButton").grid(row=5, column=0, columnspan=3, padx=20, pady=20, sticky='nsew')
        
        # Set the width and height of the add task window
        add_task_window.geometry("400x300")  


    def add_task(self, task_name, priority, due_date, status, done):
        try:
            # Add task to the database
            self.task_db.add_task(task_name, priority, due_date, status, done)

            # Refresh the task table
            self.load_tasks()

            # Close the add task window
            self.focus_set()
            self.grab_set()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_tasks(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch tasks from the database
        tasks = self.task_db.get_all_tasks()

        # Insert tasks into the table
        for task in tasks:
            self.tree.insert("", "end", values=task)

    def delete_task(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected task?")
        if confirm:
            # Delete selected task from the database
            task_id = self.tree.item(selected_item)['values'][0]
            self.task_db.delete_task(task_id)

            # Refresh the task table
            self.load_tasks()

    def clear_task(self):
        # Confirm clearing all tasks
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all tasks?")
        if confirm:
            # Clear all tasks from the database
            self.task_db.clear_tasks()

            # Refresh the task table
            self.load_tasks()

    def center_window(self):
        # Center the window on the screen
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2.6 - window_width / 1)
        position_down = int(self.winfo_screenheight() / 2.6 - window_height / 1)
        self.geometry(f"+{position_right}+{position_down}")

    def search(self):
        # Get the search keyword
        keyword = self.search_var.get().lower()

        # Iterate through the rows in the table
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            
            # Check if the keyword is present in any cell
            if any(keyword in str(value).lower() for value in values):
                self.tree.tag_configure("highlight", background="#3595D7", foreground="white")
                self.tree.item(item, tags=("highlight",))
            else:
                # Remove highlighting if keyword is not found
                self.tree.item(item, tags=())

if __name__ == "__main__":
    app = TaskManager(fg_color='#FFFFFF')
    app.title("Tasks - Task Management System")
    app.mainloop()