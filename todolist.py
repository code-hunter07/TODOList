import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import winsound
import threading
import time
from tkcalendar import Calendar  # Import Calendar widget from tkcalendar library
import plyer
# import re

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List with Reminders")
        self.task_list = []

        self.light_mode_colors = {
            "background": "#f0f0f0",
            "button": "#4CAF50",
            "button_text": "white",
            "label": "#333",
            "tasklist": "#fff",
            "tasklist_font": "#333",
        }

        self.dark_mode_colors = {
            "background": "#333",
            "button": "#555",
            "button_text": "white",
            "label": "#fff",
            "tasklist": "#444",
            "tasklist_font": "#eee",
        }

        self.current_colors = self.light_mode_colors
        self.title_font = ('Arial', 14, 'bold')
        self.normal_font = ('Arial', 12)

        # Frame for the left side
        self.left_frame = tk.Frame(master, bg=self.current_colors["background"])
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for the right side
        self.right_frame = tk.Frame(master, bg=self.current_colors["background"])
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Side
        tk.Label(self.left_frame, text="Title:", font=self.title_font, fg=self.current_colors["label"], bg=self.current_colors["background"]).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.title_entry = tk.Entry(self.left_frame, width=50, font=self.normal_font)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.left_frame, text="Reminder Date:", font=self.title_font, fg=self.current_colors["label"], bg=self.current_colors["background"]).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.date_picker = Calendar(self.left_frame, selectmode="day", date_pattern="yyyy-mm-dd", font=self.normal_font, foreground=self.current_colors["label"], background=self.current_colors["background"])
        self.date_picker.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.left_frame, text="Reminder Time (HH:MM):", font=self.title_font, fg=self.current_colors["label"], bg=self.current_colors["background"]).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.time_entry = tk.Entry(self.left_frame, width=10, font=self.normal_font)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.left_frame, text="Priority:", font=self.title_font, fg=self.current_colors["label"], bg=self.current_colors["background"]).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.priority_combobox = ttk.Combobox(self.left_frame, values=["High", "Medium", "Low"], state="readonly", width=15)
        self.priority_combobox.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.left_frame, text="Category:", font=self.title_font, fg=self.current_colors["label"], bg=self.current_colors["background"]).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.category_combobox = ttk.Combobox(self.left_frame, values=["Work", "Personal", "Shopping"], state="readonly", width=15)
        self.category_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.left_frame, text="Notes:", font=self.title_font, fg=self.current_colors["label"], bg=self.current_colors["background"]).grid(row=5, column=0, padx=10, pady=10, sticky="ne")
        self.notes_text = tk.Text(self.left_frame, height=5, width=50, font=self.normal_font)
        self.notes_text.grid(row=5, column=1, padx=10, pady=10, sticky="nw")

        self.set_reminder_button = tk.Button(self.left_frame, text="Set Reminder", command=self.set_reminder, bg=self.current_colors["button"], fg=self.current_colors["button_text"], font=self.normal_font)
        self.set_reminder_button.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Search Bar
        self.search_entry = tk.Entry(self.right_frame, width=40, font=self.normal_font)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        
        self.search_button = tk.Button(self.right_frame, text="Search", command=self.search_tasks, bg=self.current_colors["background"])
        self.search_button.grid(row=0, column=1, padx=5, pady=10, sticky="e")

        # Back button
        self.back_button = tk.Button(self.right_frame, text="Back", command=self.load_all_tasks, bg=self.current_colors["background"])
        self.back_button.grid(row=0, column=2, padx=5, pady=10, sticky="e")

        # Right Side
        self.task_listbox = tk.Listbox(self.right_frame, width=60, height=20, font=self.normal_font, bg=self.current_colors["tasklist"], fg=self.current_colors["tasklist_font"])
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.task_listbox.config(bg=self.current_colors["tasklist"], bd=2, relief=tk.GROOVE)
        scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        self.edit_button = tk.Button(self.right_frame, text="Edit Task", command=self.edit_task, bg=self.current_colors["button"], fg=self.current_colors["button_text"], font=self.normal_font)
        self.edit_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(self.right_frame, text="Delete Task", command=self.delete_task, bg=self.current_colors["button"], fg=self.current_colors["button_text"], font=self.normal_font)
        self.delete_button.grid(row=2, column=1, padx=10, pady=10)

        self.mode_button = tk.Button(self.right_frame, text="Dark Mode", command=self.toggle_mode, bg=self.current_colors["button"], fg=self.current_colors["button_text"], font=self.normal_font)
        self.mode_button.grid(row=4, column=1, padx=10, pady=10)

        self.clock_label = tk.Label(self.right_frame, text="", font=('Arial', 21, 'bold'), fg=self.current_colors["label"], bg=self.current_colors["background"])
        self.clock_label.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.reminder_thread = threading.Thread(target=self.monitor_reminders)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()

        self.update_clock()

    def set_reminder(self):
        task = self.title_entry.get().strip()
        reminder_date = self.date_picker.get_date()
        reminder_time = self.time_entry.get().strip()
        priority = self.priority_combobox.get().strip()
        category = self.category_combobox.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if task and reminder_date and reminder_time:
            reminder_datetime = f"{reminder_date} {reminder_time}"
            self.task_list.append({"task": task, "datetime": reminder_datetime, "priority": priority, "category": category, "notes": notes})
            self.task_listbox.insert(tk.END, f"{task} - {reminder_datetime} - Priority: {priority} - Category: {category} - Notes: {notes}")
            self.title_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.priority_combobox.set("")
            self.category_combobox.set("")
            self.notes_text.delete("1.0", tk.END)  # Clear the notes text
        else:
            messagebox.showwarning("Warning", "Title, Reminder Date, and Reminder Time cannot be empty!")

    def monitor_reminders(self):
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            for task in self.task_list:
                task_datetime = task["datetime"]
                if current_time == task_datetime:
                    self.show_notification(task)
                    self.play_sound()
                    self.task_list.remove(task)
                    self.task_listbox.delete(0, tk.END)
                    for t in self.task_list:
                        self.task_listbox.insert(tk.END, f"{t['task']} - {t['datetime']} - Priority: {t['priority']} - Category: {t['category']} - Notes: {t['notes']}")
            time.sleep(10)

    def show_notification(self, task):
        notification_title = "Task Reminder"
        notification_message = f"Task: {task['task']}\nReminder Date/Time: {task['datetime']}\nPriority: {task['priority']}\nCategory: {task['category']}\nNotes: {task['notes']}"
        plyer.notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon=None,
            timeout=10
        )

    def play_sound(self):
        winsound.Beep(1000, 2500)

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()
            if selected_task_index:
                self.task_list.pop(selected_task_index[0])
                self.task_listbox.delete(selected_task_index)
            else:
                messagebox.showwarning("Warning", "Please select a task to delete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the task: {str(e)}")

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.clock_label.after(1000, self.update_clock)

    def toggle_mode(self):
        if self.current_colors == self.light_mode_colors:
            self.set_dark_mode()
        else:
            self.set_light_mode()

    def set_dark_mode(self):
        self.current_colors = self.dark_mode_colors
        self.update_colors()

    def set_light_mode(self):
        self.current_colors = self.light_mode_colors
        self.update_colors()

    def update_colors(self):
        self.left_frame.config(bg=self.current_colors["background"])
        self.right_frame.config(bg=self.current_colors["background"])
        self.title_entry.config(bg=self.current_colors["background"], fg=self.current_colors["label"])
        self.date_picker.config(bg=self.current_colors["background"], fg=self.current_colors["label"], selectbackground=self.current_colors["background"], selectforeground=self.current_colors["button_text"])
        self.time_entry.config(bg=self.current_colors["background"], fg=self.current_colors["label"])
        self.priority_combobox.config(background=self.current_colors["background"], foreground=self.current_colors["label"])
        self.category_combobox.config(background=self.current_colors["background"], foreground=self.current_colors["label"])
        self.notes_text.config(bg=self.current_colors["background"], fg=self.current_colors["label"])
        self.set_reminder_button.config(bg=self.current_colors["button"], fg=self.current_colors["button_text"])
        self.task_listbox.config(bg=self.current_colors["tasklist"], fg=self.current_colors["tasklist_font"])
        self.clock_label.config(bg=self.current_colors["background"], fg=self.current_colors["label"])
        self.delete_button.config(bg=self.current_colors["button"], fg=self.current_colors["button_text"])
        self.mode_button.config(bg=self.current_colors["button"], fg=self.current_colors["button_text"])

    def search_tasks(self, event=None):
        search_query = self.search_entry.get().strip().lower()
        searched_tasks = []
        other_tasks = []
        for task in self.task_list:
            if search_query in task["task"].lower():
                searched_tasks.append(task)
            else:
                other_tasks.append(task)
        # Display searched tasks first followed by other tasks
        self.task_listbox.delete(0, tk.END)
        for task in searched_tasks:
            self.task_listbox.insert(tk.END, f"{task['task']} - {task['datetime']} - Priority: {task['priority']} - Category: {task['category']} - Notes: {task['notes']}")
        for task in other_tasks:
            self.task_listbox.insert(tk.END, f"{task['task']} - {task['datetime']} - Priority: {task['priority']} - Category: {task['category']} - Notes: {task['notes']}")

    def load_all_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_list:
            self.task_listbox.insert(tk.END, f"{task['task']} - {task['datetime']} - Priority: {task['priority']} - Category: {task['category']} - Notes: {task['notes']}")

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            try:
                selected_task = self.task_list[selected_task_index[0]]
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(tk.END, selected_task["task"])
                self.date_picker.set_date(selected_task["datetime"].split()[0])
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(tk.END, selected_task["datetime"].split()[1])
                self.priority_combobox.set(selected_task["priority"])
                self.category_combobox.set(selected_task["category"])
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert(tk.END, selected_task["notes"])
                self.set_reminder_button.config(command=lambda: self.update_task(selected_task_index))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while editing the task: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a task to edit!")

    def update_task(self, selected_task_index):
        updated_task = {
            "task": self.title_entry.get().strip(),
            "datetime": f"{self.date_picker.get_date()} {self.time_entry.get().strip()}",
            "priority": self.priority_combobox.get().strip(),
            "category": self.category_combobox.get().strip(),
            "notes": self.notes_text.get('1.0', tk.END).strip()
        }

        self.task_list[selected_task_index[0]] = updated_task
        self.task_listbox.delete(0, tk.END)
        for task in self.task_list:
            self.task_listbox.insert(tk.END, f"{task['task']} - {task['datetime']} - Priority: {task['priority']} - Category: {task['category']} - Notes: {task['notes']}")
        self.set_reminder_button.config(command=self.set_reminder)

def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
