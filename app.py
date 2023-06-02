import tkinter as tk
import datetime


class Task:
    def __init__(self, name, deadline):
        self.name = name
        self.deadline = deadline

    def get_name(self):
        return self.name

    def get_deadline(self):
        return self.deadline


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_index):
        del self.tasks[task_index]

    def get_tasks(self):
        return self.tasks


class GUI:
    def __init__(self, taskManager):
        self.taskManager = taskManager

        self.root = tk.Tk()
        self.root.title("Task Management Tool")

        # Create widgets
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_entry = tk.Entry(self.root)
        self.deadline_label = tk.Label(self.root, text="Deadline (DD/MM/YYYY):")
        self.deadline_entry = tk.Entry(self.root)
        self.add_button = tk.Button(self.root, text="Add", command=self.add_task)
        self.task_listbox = tk.Listbox(self.root)
        self.remove_button = tk.Button(self.root, text="Remove", command=self.remove_task)

        # Layout widgets
        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.deadline_label.grid(row=1, column=0)
        self.deadline_entry.grid(row=1, column=1)
        self.add_button.grid(row=2, column=0, columnspan=2)
        self.task_listbox.grid(row=3, column=0, columnspan=2)
        self.remove_button.grid(row=4, column=0, columnspan=2)

        # Populate task listbox
        self.update_task_listbox()

        # Run GUI mainloop
        self.root.mainloop()

    def add_task(self):
        name = self.name_entry.get()
        deadline_str = self.deadline_entry.get()
        deadline = datetime.datetime.strptime(deadline_str, "%d/%m/%Y")
        task = Task(name, deadline)
        self.taskManager.add_task(task)
        self.update_task_listbox()
        self.name_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

    def remove_task(self):
        selected_task = self.task_listbox.curselection()[0]
        self.taskManager.remove_task(selected_task)
        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.taskManager.get_tasks():
            task_str = f"{task.get_name()} - {task.get_deadline().strftime('%d/%m/%Y')}"
            self.task_listbox.insert(tk.END, task_str)


if __name__ == "__main__":
    taskManager = TaskManager()
    gui = GUI(taskManager)