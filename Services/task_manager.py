from Models.task import Task
import json
import os



class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
    
    def get_all_tasks(self):
        """
        Retrieve all tasks from the task list.
        
        Returns:
            list: List of Task objects
        """
        return self.tasks
    
    def add_task(self, title, completed=False):
        """Add a new task with error handling"""
        try:
            # Validate input
            if not title or not isinstance(title, str):
                raise ValueError("Task title must be a non-empty string")
            
            # Create and add task
            task = Task(id=self.next_id, title=title, completed=completed)
            self.tasks.append(task)
            self.next_id += 1
            self.save_tasks()
            
            return task
            
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
    
    def get_task_by_id(self, task_id):
        """
        Get a specific task by its ID.
        
        Args:
            task_id (int): The ID of the task to retrieve
            
        Returns:
            Task or None: The task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id, title=None, completed=None):
        """
        Update a task's properties.
        
        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            completed (bool, optional): New completion status
            
        Returns:
            Task or None: Updated task object if found, None otherwise
        """
        task = self.get_task_by_id(task_id)
        if task:
            if title is not None:
                task.title = title
            if completed is not None:
                task.completed = completed
            self.save_tasks()
            return task
        return None
    
    def delete_task(self, task_id):
        """
        Delete a task by its ID.
        
        Args:
            task_id (int): The ID of the task to delete
            
        Returns:
            bool: True if task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
    
    def get_completed_tasks(self):
        """
        Get all completed tasks.
        
        Returns:
            list: List of completed Task objects
        """
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self):
        """
        Get all pending (incomplete) tasks.
        
        Returns:
            list: List of pending Task objects
        """
        return [task for task in self.tasks if not task.completed]
    
    def mark_task_complete(self, task_id):
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The ID of the task to mark as complete
            
        Returns:
            Task or None: Updated task object if found, None otherwise
        """
        return self.update_task(task_id, completed=True)
    
    def mark_task_incomplete(self, task_id):
        """
        Mark a task as incomplete.
        
        Args:
            task_id (int): The ID of the task to mark as incomplete
            
        Returns:
            Task or None: Updated task object if found, None otherwise
        """
        return self.update_task(task_id, completed=False)
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    # Convert dictionary data back to Task objects
                    self.tasks = []
                    for task_data in data:
                        task = task(
                            id=task_data['id'],
                            title=task_data['title'],
                            completed=task_data.get('completed', False)
                        )
                        self.tasks.append(task)
                        # Update next_id to avoid conflicts
                        if task.id >= self.next_id:
                            self.next_id = task.id + 1
            else:
                self.tasks = []
                self.save_tasks()
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Error loading tasks from {self.filename}. Starting with empty task list.")
            self.tasks = []
            self.save_tasks()
        except Exception as e:
            print(f"Unexpected error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            # Convert Task objects to dictionaries for JSON serialization
            tasks_data = [Task.to_dict() for task in self.tasks]
            with open(self.filename, 'w') as f:
                json.dump(tasks_data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def get_task_count(self):
        """
        Get the total number of tasks.
        
        Returns:
            int: Total number of tasks
        """
        return len(self.tasks)
    
    def get_completed_count(self):
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
        """
        return len(self.get_completed_tasks())
    
    def get_pending_count(self):
        """
        Get the number of pending tasks.
        
        Returns:
            int: Number of pending tasks
        """
        return len(self.get_pending_tasks())