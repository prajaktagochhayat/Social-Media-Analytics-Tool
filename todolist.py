# Import the tkinter library for creating the graphical user interface (GUI)
import tkinter as tk

# Define a class for the To-Do List application
class TodoApp:
    def __init__(self, root):
        # Set the title of the window
        root.title("To-Do List App")
        # Set the size of the window
        root.geometry("400x400")
        
        # Create a list to store tasks. Each task is a dictionary with 'text' and 'completed' status
        self.tasks = []
        
        # Create an entry field for users to type new tasks
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)
        
        # Create a button to add the task from the entry field
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()
        
        # Create a listbox to display all tasks
        self.task_listbox = tk.Listbox(root, width=50, height=15)
        self.task_listbox.pack(pady=10)
        
        # Create a frame to hold the buttons for actions
        button_frame = tk.Frame(root)
        button_frame.pack()
        
        # Create a button to mark the selected task as completed
        self.complete_button = tk.Button(button_frame, text="Mark as Completed", command=self.mark_completed)
        self.complete_button.pack(side=tk.LEFT, padx=5)
        
        # Create a button to delete the selected task
        self.delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Create a button to clear all tasks
        self.clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=5)
    
    # Function to add a new task
    def add_task(self):
        # Get the text from the entry field
        task_text = self.task_entry.get()
        # If the text is not empty, add it to the tasks list
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            # Clear the entry field
            self.task_entry.delete(0, tk.END)
            # Update the listbox to show the new task
            self.update_listbox()
    
    # Function to update the listbox with current tasks
    def update_listbox(self):
        # Clear the listbox
        self.task_listbox.delete(0, tk.END)
        # Add each task to the listbox, showing if it's completed
        for task in self.tasks:
            display_text = task["text"]
            if task["completed"]:
                display_text += " (Completed)"
            self.task_listbox.insert(tk.END, display_text)
    
    # Function to mark the selected task as completed
    def mark_completed(self):
        # Get the index of the selected item in the listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            # Mark the task as completed in the tasks list
            self.tasks[selected_index[0]]["completed"] = True
            # Update the listbox
            self.update_listbox()
    
    # Function to delete the selected task
    def delete_task(self):
        # Get the index of the selected item in the listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            # Remove the task from the tasks list
            del self.tasks[selected_index[0]]
            # Update the listbox
            self.update_listbox()
    
    # Function to clear all tasks
    def clear_all(self):
        # Clear the tasks list
        self.tasks = []
        # Update the listbox
        self.update_listbox()

# Main part of the program: create the root window and start the app
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Create an instance of the TodoApp class
    app = TodoApp(root)
    # Start the GUI event loop
    root.mainloop()