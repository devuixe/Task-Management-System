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
        ), style="Custom.TButton").grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')
        
        # Set the width and height of the add task window
        add_task_window.geometry("400x300")